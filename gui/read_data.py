import pandas as pd

def read_data(filename = 'norm.xlsx'):
    """
    read data and labels for tablewidget
    :param filename: filename to read
    :return: t -labels for header column;
            dft - data for tablewidget
    """
    xl_file = pd.ExcelFile(filename)
    dfs = xl_file.parse(xl_file.sheet_names[0])
    dfd = dfs.as_matrix()
    t = dfs.columns.values.tolist()
    return t, dfd
