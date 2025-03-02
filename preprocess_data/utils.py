import csv

def save(filename, data):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if len(data) == 0:
            empty = {"ID": "", "brand": "", "NIC": "", "owner": "", "image": ""}
            writer.writerow(empty.keys())
            return
        writer.writerow(data[0].keys())
        for entry in data:
            writer.writerow(entry.values())