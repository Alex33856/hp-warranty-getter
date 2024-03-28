from dataclasses import dataclass
from time import sleep

from selenium.webdriver.common.by import By

from lib.SeleniumHelper import clickElement, inputText, findElement, waitForElement
from providers.WarrantyProvider import WarrantyProvider


@dataclass(slots=True)
class DellWarrantyProvider(WarrantyProvider):
    MaxCapacity: int = 1
    URL: str = "https://www.dell.com/support/home/en-us/"

    def submitEntry(self):
        submitButton = waitForElement(self.driver, By.ID, "btnSubmit")
        clickElement(self.driver, submitButton)

    def closePopup(self):
        closeButton = findElement(self.driver, By.CLASS_NAME, "dds__popover__close")
        if closeButton:
            clickElement(self.driver, closeButton)

    def processEntries(self, products: dict[str]) -> tuple[list, list]:
        self.closePopup()
        for i in range(1, 4):
            # Wait for verification to complete.
            if findElement(self.driver, By.ID, "homemfe-dropdown-input"):
                sleep(10*i)
            else:
                break
            self.submitEntry()
        waitForElement(self.driver, By.ID, "service-tag")

        try:
            serialNumber = findElement(self.driver, By.CLASS_NAME, "service-tag")
            serialNumber = serialNumber.text.split("Service Tag: ")[1]

            warrantyStatus = findElement(self.driver, By.ID, "ps-inlineWarranty")
            warrantyStatus = warrantyStatus.find_element(By.CLASS_NAME, "warrantyExpiringLabel")
            warrantyStatus = warrantyStatus.text

            result = ["{},{},{}".format(serialNumber, "N/A", warrantyStatus)]
            return result, []
        except Exception as ex:
            print(ex)
            return [], [list(products.keys())[0]]

    def addSerialNumbersToPage(self, products: dict[str, str]):
        self.openPage()
        sleep(5)

        for product in products:
            inputBox = waitForElement(self.driver, By.ID, "homemfe-dropdown-input")
            inputText(inputBox, product)
