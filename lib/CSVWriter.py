import csv

# fields = ["type", "serialNumber", "productNumber"]
if __name__ == "__main__":
    with open("../ProductsIn.txt", "r") as rowsIn:
        rows = rowsIn.readlines()
    print(rows)

    csvRows = []
    for sN in rows:
        # deviceType = "Dell"
        # if "5CD" in sN:
        deviceType = "HP"
        csvRows.append([deviceType, sN.strip(), ""])
    print(csvRows)

    with open("../Products.csv", "w", newline='', encoding='utf-8') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(csvRows)
