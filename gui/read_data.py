import pandas as pd

def read_data(filename = 'norm.xlsx'):
    xl_file = pd.ExcelFile(filename)
    dfs = xl_file.parse(xl_file.sheet_names[0])
    dfd = dfs.as_matrix()
    return dfd
