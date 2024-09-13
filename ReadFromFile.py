import openpyxl


def arrayFromFile():
    data = openpyxl.load_workbook("testList.xlsx")
    sheet = data.worksheets[0]
    return sheet




