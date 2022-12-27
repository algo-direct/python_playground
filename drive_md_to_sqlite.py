#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pytz
import zipfile
import os
import sys
import sqlite3
from zipfile import ZipFile
import csv
from io import StringIO
from datetime import datetime
from line_profiler import LineProfiler

# In[3]:


con = sqlite3.connect("drive_md.sqlite.db")
cur = con.cursor()
try:
    cur.execute(
        "CREATE TABLE drive_md_oneminute(Symbol TEXT, Timestamp DATETIME, Open REAL, Low REAL, High REAL, Close REAL, Volumne INT, OI INT, PRIMARY KEY (Symbol, Timestamp));"
    )
except:
    pass
con.commit()


# In[4]:


def zip_to_sqlite(filename, year, month):
    rows_inserted = 0
    with ZipFile(filename) as zf:
        cur = con.cursor()
        for file in zf.namelist():
            # print(f"file:{file}, year:{year}, month:{month}")
            if file.endswith(".zip"):
                continue
            with zf.open(file, "r") as myfile:
                csv_reader = csv.reader(StringIO(myfile.read().decode("utf-8")))
                for row in csv_reader:
                    try:
                        cur.execute(
                            "INSERT INTO drive_md_oneminute(Symbol, Timestamp, Open, Low, High, Close, Volumne, OI) values (?, ?, ?, ?, ?, ?, ?, ?)",
                            (
                                row[0],
                                datetime(
                                    int(row[1][0:4]),
                                    int(row[1][4:6]),
                                    int(row[1][6:8]),
                                    hour=int(row[2][0:2]),
                                    minute=int(row[2][3:5]),
                                    second=0,
                                    microsecond=0,
                                )
                                # datetime.strptime(
                                #     row[1] + " " + row[2] + " IST", "%Y%m%d %H:%M %Z"
                                # )
                                ,
                                row[3],
                                row[4],
                                row[5],
                                row[6],
                                row[7],
                                row[8] if len(row) > 8 else 0,
                            ),
                        )
                        rows_inserted += 1
                    except Exception as ex:
                        if not str(ex).startswith("UNIQUE"):
                            print(
                                f"zip file:{filename}, file:{file}, year:{year}, month:{month}, exception:{ex}"
                            )
            # break
            # sys.exit(0)

    con.commit()
    return rows_inserted


# In[8]:


total_rows_inserted = 0
for year in range(2017, 2097):
    for month in [
        "JAN",
        "FEB",
        "MAR",
        "APR",
        "MAY",
        "JUN",
        "JUL",
        "AUG",
        "SEP",
        "OCT",
        "NOV",
        "DEC",
    ]:
        path = os.path.join("data", str(year), month)
        if not os.path.exists(path):
            continue
        print(path)
        onlyfiles = [
            f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))
        ]
        nifty_file_name_conv1 = f"NIFTY50_{month}{year}.zip"
        nifty_file_name_conv2 = f"NIFTY50_{month}{year}(with_OI).zip"
        monthly_data_file = ""
        for file_name in onlyfiles:
            if file_name == nifty_file_name_conv1:
                monthly_data_file = file_name
                break
            if file_name == nifty_file_name_conv2:
                monthly_data_file = file_name
                break
            if file_name.find("Intraday") != -1:
                if file_name.find(f"{month}{year}.zip") != -1:
                    monthly_data_file = file_name
                    break
        if monthly_data_file != "":
            continue
            monthly_data_file = os.path.join(path, monthly_data_file)
            print(f"monthly_data_file:{monthly_data_file}")
            lp = LineProfiler()
            lp_wrapper = lp(zip_to_sqlite)
            lp_wrapper(monthly_data_file, year, month)
            lp.print_stats()
            break
            # rows_inserted = zip_to_sqlite(monthly_data_file, year, month)
            total_rows_inserted += rows_inserted
            print(
                f"year:{year}, month:{month}, rows_inserted:{rows_inserted}, total_rows_inserted:{total_rows_inserted}"
            )
        else:
            print(
                f"year:{year}, month:{month} monthly_data_file not found !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            )
            for day_of_month in list(range(1, 32)):
                daily_file_name = f"{day_of_month:02}{month}.zip"
                daily_file_name = os.path.join(path, daily_file_name)
                if not os.path.exists(daily_file_name):
                    continue
                print(f"daily_file_name:{daily_file_name}")
                lp = LineProfiler()
                lp_wrapper = lp(zip_to_sqlite)
                rows_inserted = lp_wrapper(daily_file_name, year, month)
                lp.print_stats()
                # rows_inserted = zip_to_sqlite(daily_file_name, year, month)
                total_rows_inserted += rows_inserted
                print(
                    f"year:{year}, month:{month}, rows_inserted:{rows_inserted}, total_rows_inserted:{total_rows_inserted}"
                )
