# HP Warranty Getter
Automatically get the warranty for HP products in bulk.

### How To Use:
- Create a file called products.csv formatted Type, Serial Number, Product Number (Optional) - Type is always "HP"
- Run "pip install -r requirements.txt"
- Run main.py
- Warranty information should show in WarrantyInfo.csv, and failed devices will show in HP-FailedProducts.csv

### Easily create Products.csv
- Download [ChromeDriver](https://chromedriver.storage.googleapis.com/index.html) and extract it in this folder
- Run main.py
- Warranty information should show in WarrantyInfo.csv, and failed devices will show in HP-FailedProducts.csv

### How To Easily Create `Products.csv`:
- Create a file called "ProductsIn.txt" where each line is 1 serial number,
- Run CSVWriter.py
- Products.csv should be created.

### To-Do:
- Add support for checking Dell warranties 