# HP Warranty Getter
Automatically get the warranty for HP and Dell products in bulk.

### How To Use:
- Create a file called `Products.csv` formatted Type (**Dell** or **HP**), Serial Number, Product Number (Optional)
- Run `pip install -r requirements.txt`
- Run `main.py`
- Warranty information should show in WarrantyInfo.csv, and failed devices will show in `{Type}-FailedProducts.csv`

### How To Easily Create `Products.csv`:
- Create a file called `ProductsIn.txt` where each line is 1 serial number,
- Run `CSVWriter.py`
- `Products.csv` should be created.