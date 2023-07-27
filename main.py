from selenium.webdriver import Chrome

from providers.HPWarrantyProvider import HPWarrantyProvider

# from providers.DellWarrantyProvider import DellWarrantyProvider

DoneList = []
# DellProductDict = {}

ProviderType = {
    "HP": HPWarrantyProvider,
    # "Dell": DellWarrantyProvider
}

ProviderList = {
    "HP": {},
    # "Dell": {}
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
    # driverManager = ChromeDriverManager(path="./drivers")
    # driverPath = driverManager.install()
    #
    # driverService = Service(path=driverPath)
    driver = Chrome()  # service=driverService)
    return driver


def Main():
    ReadCSVs()
    driver = SetupDriver()

    for Type in ProviderList:
        ProductList = ProviderList[Type]

        Provider: HPWarrantyProvider = ProviderType[Type](driver)
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
