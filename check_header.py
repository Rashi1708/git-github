import csv
with open('sales.csv') as csvfile:
    csvfile.seek(0)
    sniffer = csv.Sniffer()
    has_header = sniffer.has_header(csvfile.read())
    print(has_header)
    # ...

