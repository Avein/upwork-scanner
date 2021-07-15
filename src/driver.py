from typing import Any

import undetected_chromedriver as uc


class UpWorkDriver:
    def __init__(self, download_path: str) -> None:
        self.download_path = download_path
        options = uc.ChromeOptions()
        # options.headless = True

        self.upwork_url = "https://www.upwork.com/ab/find-work/"
        self.driver = uc.Chrome(options=options)
        self.driver.maximize_window()

        self.driver.implicitly_wait(1.47)

    def __enter__(self) -> uc.Chrome:
        return self.driver

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.driver.quit()
