from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement


def clickElement(driver: WebDriver, element: WebElement) -> None:
    driver.execute_script("arguments[0].click();", element)


def inputText(element: WebElement, text: str) -> None:
    element.send_keys(text)
