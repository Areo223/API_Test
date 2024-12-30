from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
class ExcelHandler():

    def __init__(self, file):
        self.file = file


    def open_sheet(self, name) -> Worksheet:
        wb = load_workbook(self.file)
        sheet = wb[name]
        wb.close()
        return sheet

    def header(self, sheet_name="Sheet1"):
        sheet = self.open_sheet(sheet_name)
        headers = []
        for i in sheet[1]:
            headers.append(i.value)
        return headers

    def read(self, sheet_name='Sheet1'):
        sheet = self.open_sheet(sheet_name)
        rows = list(sheet.rows)
        data = []
        for row in rows[1:]:
            row_data = []
            for cell in row:
                cell_value = cell.value
                if isinstance(cell_value, str):
                    # 数据清洗：将 _x000D_ 替换为空字符串，以修正换行符问题
                    cell_value = cell_value.replace('_x000D_', '')
                row_data.append(cell_value)
                data_dict = dict(zip(self.header(sheet_name), row_data))
            data.append(data_dict)
        return data

    def read_scene(self, case_name,sheet_name='Sheet1'):
        data = self.read(sheet_name)
        scene_data = []
        for i in range(len(data)):
            if data[i]['case_name'] == case_name:
                scene_data.append(data[i])
        return scene_data


if __name__ == '__main__':
    excel = ExcelHandler('../cases.xlsx')
    data = excel.read('Sheet1')
    print(data)
