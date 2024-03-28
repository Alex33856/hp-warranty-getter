import time
from typing import Union

from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


def clickElement(driver: WebDriver, element: WebElement) -> None:
    return element.click()


def inputText(element: WebElement, text: str) -> None:
    element.send_keys(text)


def findElement(driver: WebDriver, by: By, val: str) -> Union[WebElement, None]:
    try:
        return driver.find_element(by, val)
    except NoSuchElementException:
        return None


def waitForElement(driver: WebDriver, by: By, val: str) -> Union[WebElement, None]:
    for i in range(5):
        found = findElement(driver, by, val)
        if found:
            return found
        time.sleep(1)
    return None
