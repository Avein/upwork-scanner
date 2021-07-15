from typing import Optional

import undetected_chromedriver as uc
from selenium.common.exceptions import TimeoutException

from helpers import wait_to_load
from page_objects.utils import ip_selector


def whats_my_ip() -> Optional[str]:
    options = uc.ChromeOptions()
    options.headless = True
    try:
        driver = uc.Chrome(options=options)
        driver.get("https://www.whatsmyip.org/")
        web_element = wait_to_load(driver, selector=ip_selector)
        return web_element.text
    except TimeoutException:
        return None
