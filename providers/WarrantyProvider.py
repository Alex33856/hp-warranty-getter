from dataclasses import dataclass

from selenium.webdriver.chrome.webdriver import WebDriver


@dataclass(slots=True)
class WarrantyProvider:
    driver: WebDriver = None

    MaxCapacity: int = -1
    URL: str = ""

    def openPage(self):
        return self.driver.get(self.URL)

    def submitEntry(self):
        pass

    def processEntries(self, products: dict[str, str]) -> tuple[list, list]:
        pass

    def addSerialNumbersToPage(self, products: dict[str, str]) -> None:
        pass
