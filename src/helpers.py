import random
import time
from typing import List

from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from undetected_chromedriver import Chrome

from config import TimeoutsEnum
from page_objects.login import Selector


def click_with_move(_driver: Chrome, web_element: WebElement) -> None:
    actions = ActionChains(_driver)
    actions.move_to_element(web_element)
    actions.click()
    actions.perform()


def send_keys_with_delay(
    web_element: WebElement, text: str, start: float = 0.0, stop: float = 0.3
) -> None:
    for char in text:
        n = random.uniform(start, stop)
        time.sleep(n)
        web_element.send_keys(char)


def find_element_by(_driver: Chrome, selector: Selector) -> WebElement:
    return _driver.find_element(by=selector.type, value=selector.value)


def find_elements_by(_driver: Chrome, selector: Selector) -> List[WebElement]:
    return _driver.find_elements(by=selector.type, value=selector.value)


def wait_to_load(
    _driver: Chrome, selector: Selector, timeout: int = TimeoutsEnum.LONG
) -> WebElement:
    wait = WebDriverWait(_driver, timeout)
    web_element = wait.until(
        ec.visibility_of_element_located((selector.type, selector.value))
    )
    return web_element
