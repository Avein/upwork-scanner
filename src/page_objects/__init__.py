from dataclasses import dataclass

from selenium.webdriver.common.by import By


@dataclass
class Selector:
    value: str
    type: By = By.CSS_SELECTOR
