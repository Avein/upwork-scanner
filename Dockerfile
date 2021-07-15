#Dockerfile to build an image for running Selenium tests
#Pull ubuntu 16.04 base image
#Image based on  Qxf2’s open sourced GUI automation framework https://github.com/qxf2/qxf2-page-object-model
FROM ubuntu

# Essential tools and xvfb
RUN apt-get update && apt-get install -y \
    software-properties-common \
    unzip \
    wget \
    xvfb

# Chrome browser to run the tests
ARG CHROME_VERSION=latest
RUN if [ ${CHROME_VERSION} = "latest" ]; then wget -qO /tmp/google.pub https://dl-ssl.google.com/linux/linux_signing_key.pub && cat /tmp/google.pub | apt-key add -; rm /tmp/google.pub  && echo 'deb http://dl.google.com/linux/chrome/deb/ stable main' > /etc/apt/sources.list.d/google.list  && mkdir -p /usr/share/desktop-directories  && apt-get -y update && apt-get install -y google-chrome-stable; else wget -qO- https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && wget https://www.slimjet.com/chrome/download-chrome.php?file=lnx%2Fchrome64_$CHROME_VERSION.deb && dpkg -i download-chrome*.deb || true && apt-get install -y -f && rm -rf /var/lib/apt/lists/*;fi

# Disable the SUID sandbox so that chrome can launch without being in a privileged container
RUN dpkg-divert --add --rename --divert /opt/google/chrome/google-chrome.real /opt/google/chrome/google-chrome \
        && echo "#!/bin/bash\nexec /opt/google/chrome/google-chrome.real --no-sandbox --disable-setuid-sandbox \"\$@\"" > /opt/google/chrome/google-chrome \
        && chmod 755 /opt/google/chrome/google-chrome

# Chrome Driver
ARG CHROME_DRIVER_VERSION=latest
RUN CD_VERSION=$(if [ ${CHROME_DRIVER_VERSION:-latest} = "latest" ]; then echo $(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE); else echo $CHROME_DRIVER_VERSION; fi) \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CD_VERSION/chromedriver_linux64.zip \
  && rm -rf /opt/selenium/chromedriver \
  && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
  && rm /tmp/chromedriver_linux64.zip \
  && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-$CD_VERSION \
  && chmod 755 /opt/selenium/chromedriver-$CD_VERSION \
  && ln -fs /opt/selenium/chromedriver-$CD_VERSION /usr/bin/chromedriver

RUN if [ ${CHROME_DRIVER_VERSION} != "latest" ]; then mkdir -p /opt/selenium && wget -qO /opt/selenium/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && cd /opt/selenium; unzip /opt/selenium/chromedriver_linux64.zip; rm -rf chromedriver_linux64.zip; ln -fs /opt/selenium/chromedriver /usr/local/bin/chromedriver;fi

# Python 3.5 and Python Pip
RUN apt-get update
RUN apt-get install -y \
    python3.8 \
    python3-setuptools \
    python3-pip


# set display port to avoid crash
ENV DISPLAY=:20
RUN Xvfb :20 -screen 0 1366x768x16 &

WORKDIR /code

# upgrade pip
RUN python3 -m pip install --upgrade pip

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src .

#Make sure that undetected_chromedriver download correct version or chromedriver
RUN rm -rf chromedriver

CMD [ "python3", "./job.py" ]