import csv


class createCSV:

    def __init__(self):
        createCSV.fileName = "apartments.csv"

    def write(self, data):
        createCSV.fileName = "apartments.csv"
        with open(createCSV.fileName, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
