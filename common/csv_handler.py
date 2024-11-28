import csv


class CsvHandler():

    def __init__(self, file):
        self.file = file

    def read(self):
        with open(self.file, 'r', newline='',encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            list_data = []
            for r in reader:
                k_data = []
                v_data = []
                for k, v in r.items():
                    k_data.append(k)
                    v_data.append(v.replace("\r",""))
                data_dict = dict(zip(k_data, v_data))
                list_data.append(data_dict)
        return list_data

if __name__ == '__main__':
    csv1 = CsvHandler('../cases.csv')
    data = csv1.read()
    print(data,type(data))




