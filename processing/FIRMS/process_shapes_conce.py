import fiona
import glob
import pandas as pd

basedir = '/home/tcarrasco/result/data/FIRMS/info_added_conce/'

# 2017

filepaths = glob.glob(basedir+'FIRMS_2017-*_info.shp')

dr = pd.date_range('2017-01-01', '2017-02-28', freq='1D')

df = pd.DataFrame(columns=['time', 'burned_area'])
df['time'] = dr

for filepath, date in zip(filepaths, dr):

    if date.month == 1 and date.day == 24:
        total_area = 62241046.14821604
        df.loc[df['time'] == date, 'burned_area'] = total_area
        continue

    if date.month == 1 and date.day == 26:
        total_area = 892719830.33829749
        df.loc[df['time'] == date, 'burned_area'] = total_area
        continue

    # print(filepath, date)
    total_area = 0
    with fiona.open(filepath) as shapefile:
        for record in shapefile:
            dn = record['properties']['value']
            area = record['properties']['area']
            if dn == 1:
                total_area = total_area + area
    df.loc[df['time'] == date, 'burned_area'] = total_area

df.to_csv('/home/tcarrasco/result/data/FIRMS/tables/FIRMS_2017_conce.csv')
