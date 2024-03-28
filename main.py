from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from providers.DellWarrantyProvider import DellWarrantyProvider
from providers.HPWarrantyProvider import HPWarrantyProvider
from providers.WarrantyProvider import WarrantyProvider

DoneList = []

ProviderType = {
    "HP": HPWarrantyProvider,
    "Dell": DellWarrantyProvider
}

ProviderList = {
    "HP": {},
    "Dell": {}
}


def ReadCSVs():
    with open("Products.csv", "r") as productsIn:
        # Type, Serial Number, (Optional) Product Number
        for line in productsIn:
            TypeIn, SerialIn, ProductIn = line.split(",")
            ProductIn.strip()

            ProductDict = ProviderList[TypeIn]
            ProductDict[SerialIn] = {ProductIn}

    with open("WarrantyInfo.csv", "r") as doneIn:
        for line in doneIn:
            Parts = line.split(",")
            DoneList.append(Parts[0])


def WriteCSV(fileName: str, toWrite: list[str]):
    with open(fileName, "a") as CSVOut:
        CSVOut.writelines(toWrite)


def SetupDriver() -> Chrome:
    driverManager = ChromeDriverManager()
    driverPath = driverManager.install()
    driver = Chrome(service=ChromeService(driverPath))
    return driver


def Main():
    ReadCSVs()
    driver = SetupDriver()

    for Type in ProviderList:
        ProductList = ProviderList[Type]

        Provider: WarrantyProvider = ProviderType[Type](driver)
        SplitLists = []

        productList = list(ProductList.items())
        for i, item in enumerate(productList):
            if item in DoneList:
                continue
            listIndex = int(i / Provider.MaxCapacity)

            if listIndex + 1 > len(SplitLists):
                SplitLists.append([])
            SplitLists[listIndex].append(item)

        for splitList in SplitLists:
            productsOut = dict(splitList)
            Provider.addSerialNumbersToPage(productsOut)
            warranties, failed = Provider.processEntries(productsOut)

            WriteCSV("WarrantyInfo.csv", warranties)
            WriteCSV(Type + "-FailedProducts.csv", failed)


if __name__ == "__main__":
    Main()
