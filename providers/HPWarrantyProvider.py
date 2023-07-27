from dataclasses import dataclass
from time import sleep

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from lib.SeleniumHelper import clickElement, inputText


@dataclass
class HPWarrantyProvider:
    driver: WebDriver

    # Constants
    MaxCapacity: int = 15
    URL: str = "https://support.hp.com/us-en/checkwarranty/multipleproducts"

    def openPage(self) -> None:
        self.driver.get(self.URL)

    def submitEntry(self, previousFailure: bool) -> None:
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
            print("Failed on: ")
            print(failureList)

        return needToResubmit, failureList

    def processEntries(self, products: dict[str, str]) -> tuple[list, list]:
        self.submitEntry(False)
        sleep(10)

        successList = []
        deviceFailed, failList = self.checkForFailure(products)
        if deviceFailed:
            self.submitEntry(True)
            sleep(10)

        elements = self.driver.find_elements(By.CLASS_NAME, 'product-warranty')
        for elem in elements:
            serial = elem.find_element(By.CLASS_NAME, "serial-no")
            serialNumber = serial.find_element(By.TAG_NAME, "span").get_attribute("innerText")

            product = elem.find_element(By.CLASS_NAME, "product-no")
            productNumber = product.find_element(By.TAG_NAME, "span").get_attribute("innerText")

            expireDate = elem.find_element(By.CLASS_NAME, "expiry-date")
            expireDate = expireDate.get_attribute("innerText")
            expireDate = expireDate.split("End date:")[1].strip()

            successList.append("{},{},{}\n".format(serialNumber, productNumber, expireDate))

        return successList, failList

    def addSerialNumbersToPage(self, products: dict[str, str]):
        self.openPage()

        index = 0
        for serialNumber in products:
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

            index += 1

