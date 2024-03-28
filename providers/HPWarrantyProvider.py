from dataclasses import dataclass
from time import sleep
from urllib.parse import parse_qs

from selenium.webdriver.common.by import By

from lib.SeleniumHelper import clickElement, inputText
from providers.WarrantyProvider import WarrantyProvider


@dataclass(slots=True)
class HPWarrantyProvider(WarrantyProvider):
    # Constants
    MaxCapacity: int = 15
    URL: str = "https://support.hp.com/us-en/checkwarranty/multipleproducts"
    SINGLE_URL: str = "https://support.hp.com/us-en/checkwarranty"

    def openPage(self, isMultiple: bool = False) -> None:
        if isMultiple:
            self.driver.get(self.URL)
        else:
            self.driver.get(self.SINGLE_URL)

    def submitEntry(self, previousFailure: bool = False) -> None:
        if previousFailure:
            elementName = "FindMyProductNumber"
        else:
            elementName = "FindMyProduct"

        submitButton = self.driver.find_element(By.ID, elementName)
        clickElement(self.driver, submitButton)

    def checkForFailure(self, products: dict[str, str]) -> tuple[bool, list]:
        needToResubmit = False
        failureList = []

        try:
            elements = self.driver.find_elements(By.CLASS_NAME, f"input-product")
            for element in elements:
                elementId = element.get_attribute("id")
                product = elementId.split("product-number inputtextPN")[1]
                serialNumber = self.driver.find_element(By.ID, f'inputtextpfinder{product}')
                serialNumber = serialNumber.get_attribute("value")

                if products[serialNumber] != "":
                    element.send_keys(products[serialNumber])
                    needToResubmit = True
                else:
                    closeButton = element.find_element(By.XPATH, "..").find_element(By.XPATH, "..").find_element(
                        By.CLASS_NAME, "common-svg")
                    clickElement(closeButton)

                    failureList.append(serialNumber)
                    needToResubmit = True
        except:
            pass

        if len(failureList) > 0:
            print(f"Failed on: {failureList}")

        return needToResubmit, failureList

    def processEntries(self, products: dict[str, str]) -> tuple[list, list]:
        self.submitEntry(False)
        sleep(10)

        successList = []
        deviceFailed, failList = self.checkForFailure(products)
        if deviceFailed:
            self.submitEntry(True)
            sleep(10)

        isSingle = len(products) == 1

        if not isSingle:
            elements = self.driver.find_elements(By.CLASS_NAME, 'view-details-btn')
            originalTab = self.driver.current_window_handle
        else:
            elements = [""]

        for elem in elements:
            if not isSingle:
                url = elem.get_attribute("href")
                self.driver.switch_to.new_window('tab')
                self.driver.get(url)
            sleep(5)

            urlParams = parse_qs(self.driver.current_url.split("?")[1])
            serialNumber = urlParams["serialnumber"][0]
            productNumber = urlParams["sku"][0]

            expireDate = None
            for label in self.driver.find_elements(By.CLASS_NAME, "label"):
                if label.text == "End date":
                    expireDate = label.find_element(By.XPATH, "..").find_element(By.CLASS_NAME, "text").text

            if not expireDate:
                failList.append(serialNumber)
                continue

            successList.append("{},{},{}\n".format(serialNumber, productNumber, expireDate))
            if not isSingle:
                self.driver.close()
                self.driver.switch_to.window(originalTab)

        return successList, failList

    def addSerialNumbersToPage(self, products: dict[str, str]):
        self.openPage()
        sleep(5)

        for index, serialNumber in enumerate(products):
            indexString = ""
            if index > 0:
                indexString = str(index)
                try:
                    addItemElement = self.driver.find_element(By.ID, "AddItem")
                    clickElement(self.driver, addItemElement)
                except:
                    pass

            serialElement = self.driver.find_element(By.ID, "inputtextpfinder" + indexString)
            inputText(serialElement, serialNumber)
