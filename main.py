#%%
"""
Generator danych do zadania 2 z ZBD
"""
import random
import datetime
import string
import numpy as np
import pandas as pd
from datetime import date, timedelta
import os
import glob

CLASSES = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','T','Q','U','V','W','X','Y','Z']
DATES = []
CLASSES_COUNT = 26
MEAN = 100
VAR = 20
DATE_FROM = datetime.date(2016, 1, 1)

def clean(path):
    files = glob.glob(path)
    for f in files:
        try:
            f.unlink()
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

def clean_all():
    clean('/data/*')
    clean('/scripts/*')

COLUMNS_COUNT = 1
DAYS_NUMBER = 30 ##((DATE_TO-DATE_FROM).days) + 1
ROWS_NUMBER = CLASSES_COUNT* DAYS_NUMBER

def normal_random_values(ROWS_NUMBER, COLUMNS_COUNT):
    return np.random.normal(MEAN, VAR, size=(ROWS_NUMBER, COLUMNS_COUNT)).astype(int)

def dates_and_classes(DAYS_NUMBER):
    dates = []
    classes = []
    for i in range(DAYS_NUMBER):
        for j in range(CLASSES_COUNT):
            dates.append(DATE_FROM + timedelta(days=i))
            classes.append(CLASSES[j])
    df_dates = pd.DataFrame(dates)
    df_classes = pd.DataFrame(classes)
    return pd.concat([df_dates, df_classes], axis=1)

def data(ROWS_NUMBER, COLUMNS_COUNT, DAYS_NUMBER):
    datas = normal_random_values(ROWS_NUMBER, COLUMNS_COUNT)
    df = pd.DataFrame(data=datas[0:, 0:], index = [i for i in range(datas.shape[0])],)
    final_df = pd.concat([dates_and_classes(DAYS_NUMBER), df], axis=1)
    columns = []
    columns.append('day')
    columns.append('class')
    for i in range(COLUMNS_COUNT):
        columns.append('value_' + str(i))
    final_df.columns = columns
    return final_df

def gen_data(COLUMNS_COUNT, DAYS_NUMBER):
    ROWS_NUMBER = CLASSES_COUNT * DAYS_NUMBER
    CNAME = str(COLUMNS_COUNT)
    DNAME = str(DAYS_NUMBER)
    while len(CNAME) < 4:
        CNAME = '0' + CNAME
    while len(DNAME) < 4:
        DNAME = '0' + DNAME
    data(ROWS_NUMBER, COLUMNS_COUNT, DAYS_NUMBER).to_csv('data/data-' + CNAME + '_columns-' + DNAME + '_days' + '.csv', index=False, header=False)
    sql_script(COLUMNS_COUNT, CNAME, DNAME)

columns_counts = [1,4,16,64,256, 512, 1024, 2048]
days_counts = [30, 90, 182, 365, 730, 1460, 2920]

#%%
def sql_script(COLUMNS_COUNT, CNAME, DNAME):
    text_file = open('scripts/script-' + CNAME + '_columns-' + DNAME + '_days' + '.sql', "w")
    text_file.write('DROP FOREIGN TABLE data;\n')
    text_file.write('CREATE FOREIGN TABLE data (\n')
    text_file.write('        day date,\n')
    text_file.write('        class text,\n')
    for i in range(COLUMNS_COUNT - 1):
        text_file.write('       value_' + (str(i)) + ' integer,\n')
    text_file.write('       value_' + (str(COLUMNS_COUNT-1)) + ' integer\n')
    text_file.write(') SERVER data_csv\n')
    text_file.write("OPTIONS( filename '/home/stach/zad2/" + 'data/data-' + CNAME + '_columns-' + DNAME + '_days' + '.csv' + "', format 'csv');\n")

    text_file.write('DROP FOREIGN TABLE data_cstore;\n')
    text_file.write('CREATE FOREIGN TABLE data_cstore (\n')
    text_file.write('        day date,\n')
    text_file.write('        class text,\n')
    for i in range(COLUMNS_COUNT - 1):
        text_file.write('       value_' + (str(i)) + ' integer,\n')
    text_file.write('       value_' + (str(COLUMNS_COUNT-1)) + ' integer\n')
    text_file.write(') SERVER cstore_server;\n')
    text_file.write("\\COPY data_cstore FROM /home/stach/zad2/" + 'data/data-' + CNAME + '_columns-' + DNAME + '_days' + '.csv WITH CSV;\n')

    text_file.write('DROP TABLE data_local;\n')
    text_file.write('CREATE TABLE data_local as select * from data;\n')
    text_file.write('\o out.txt\n')
    text_file.write('\\timing\n')


    for days_number in days_counts:
        for k in CLASSES:
            text_file.write(gen_query_big(COLUMNS_COUNT, DATE_FROM, DATE_FROM + timedelta(days_number)))
    for days_number in days_counts:
        for k in CLASSES:
            text_file.write(gen_query(COLUMNS_COUNT, k, DATE_FROM, DATE_FROM + timedelta(days_number)))

    for days_number in days_counts:
        for k in CLASSES:
            text_file.write(gen_query_big(COLUMNS_COUNT, DATE_FROM, DATE_FROM + timedelta(days_number), 'data_local'))
    for days_number in days_counts:
        for k in CLASSES:
            text_file.write(gen_query(COLUMNS_COUNT, k, DATE_FROM, DATE_FROM + timedelta(days_number), 'data_local'))

    for days_number in days_counts:
        for k in CLASSES:
            text_file.write(gen_query_big(COLUMNS_COUNT, DATE_FROM, DATE_FROM + timedelta(days_number), 'data_cstore'))
    for days_number in days_counts:
        for k in CLASSES:
            text_file.write(gen_query(COLUMNS_COUNT, k, DATE_FROM, DATE_FROM + timedelta(days_number), 'data_cstore'))

    text_file.write('\q')
    text_file.close()


def gen_query(value, klass, date_start, date_finish, table='data'):
    date_s = '20' + date_start.strftime("%y-%m-%d")
    date_f = '20' + date_finish.strftime("%y-%m-%d")
    return "SELECT SUM(value_" + str(value-1) + ") FROM " + table + " where day BETWEEN '" + date_s + "' AND '" + date_f + "' AND class = '" + klass + "';\n"

def gen_query_big(value, date_start, date_finish, table='data'):
    date_s = '20' + date_start.strftime("%y-%m-%d")
    date_f = '20' + date_finish.strftime("%y-%m-%d")
    return "SELECT SUM(value_" + str(value-1) + ") FROM " + table + " where day BETWEEN '" + date_s + "' AND '" + date_f + "';\n"

clean_all()
for ccount in columns_counts:
    for dcount in days_counts:
        gen_data(ccount, dcount)