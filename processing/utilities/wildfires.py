import pandas as pd
from openpyxl import Workbook


def burned_area():
    basedir = "/home/tcarrasco/result/data/wildfires/"
    filename = "resumen_nacional_ocurrencia_dano_1964_2022.xlsx"
    filepath = basedir + filename
    df = Workbook.read_excel(filepath)
    return df
