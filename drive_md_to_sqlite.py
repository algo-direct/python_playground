#!/usr/bin/env python
# coding: utf-8

import sys
from datetime import datetime
import logging
import os

logfile = f"logs/{sys.argv[0]}_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
logging.basicConfig(
    filename=logfile,
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s:%(threadName)s [%(filename)s:%(lineno)s - %(funcName)20s() ] - %(levelname)s - %(message)s",
)
# if os.isatty(sys.stdout.fileno()):
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

import sqlite3
import threading
from zipfile import ZipFile
import csv
import time
from io import StringIO
from line_profiler import LineProfiler
import cProfile, pstats
from pstats import SortKey
import psutil

ONE_GB = 1024**3

process = psutil.Process(os.getpid())


class SymbolDBWriter:  # writes one and only one symbol
    def __init__(self, symbol) -> None:
        self.symbol = symbol
        self.pending_rows = []
        self.connection = None

    def connect_to_DB(self):
        if self.connection:
            return
        symbol = self.symbol
        db_file = f"db/drive_md_{symbol}.sqlite.db"
        logging.info(f"Opening connection for symbol: {symbol}, DB file:{db_file}")
        self.connection = sqlite3.connect(db_file)
        cursor = self.connection.cursor()
        try:
            cursor.execute(
                "CREATE TABLE drive_md_oneminute(Timestamp DATETIME PRIMARY KEY, Open REAL, Low REAL, High REAL, Close REAL, Volumne INT, OI INT);"
            )
        except:
            pass
        self.connection.commit()
        self.cursor = self.connection.cursor()

    def write(self, rows):
        self.connect_to_DB()
        # is_executemany_failed = False
        # try:
        #     self.cursor.executemany(
        #         "INSERT INTO drive_md_oneminute(Timestamp, Open, Low, High, Close, Volumne, OI) values (?, ?, ?, ?, ?, ?, ?)",
        #         [
        #             (
        #                 datetime(
        #                     int(row[1][0:4]),
        #                     int(row[1][4:6]),
        #                     int(row[1][6:8]),
        #                     hour=int(row[2][0:2]),
        #                     minute=int(row[2][3:5]),
        #                     second=0,
        #                     microsecond=0,
        #                 ),
        #                 row[3],
        #                 row[4],
        #                 row[5],
        #                 row[6],
        #                 row[7],
        #                 row[8] if len(row) > 8 else 0,
        #             )
        #             for row in rows
        #         ],
        #     )
        # except Exception as ex:
        #     if not str(ex).startswith("UNIQUE"):
        #         logging.exception(
        #             "--"  # f"zip file:{filename}, file:{file}, year:{year}, month:{month}"
        #         )
        #         is_executemany_failed = True
        #         sys.exit(0)
        # if not is_executemany_failed:
        #     self.connection.commit()
        #     self.cursor = self.connection.cursor()
        #     return
        for row in rows:
            try:
                self.cursor.execute(
                    "INSERT INTO drive_md_oneminute(Timestamp, Open, Low, High, Close, Volumne, OI) values (?, ?, ?, ?, ?, ?, ?)",
                    (
                        datetime(
                            int(row[1][0:4]),
                            int(row[1][4:6]),
                            int(row[1][6:8]),
                            hour=int(row[2][0:2]),
                            minute=int(row[2][3:5]),
                            second=0,
                            microsecond=0,
                        ),
                        row[3],
                        row[4],
                        row[5],
                        row[6],
                        row[7],
                        row[8] if len(row) > 8 else 0,
                    ),
                )
                # rows_inserted += 1
            except Exception as ex:
                if not str(ex).startswith("UNIQUE"):
                    logging.exception(
                        "--"  # f"zip file:{filename}, file:{file}, year:{year}, month:{month}"
                    )
                    # sys.exit(0)
        self.connection.commit()
        self.cursor = self.connection.cursor()


class DBWriter:  # Writes rows for multiple thread but one one thread should call member function after construction
    def __init__(self, id) -> None:
        logging.info(f"Creating {id}")
        self.id = id
        self.symbolDBWriters = {}
        self.total_pending_rows = 0
        self.lock = threading.RLock()
        self.condition = threading.Condition(lock=self.lock)
        self.stop_flag = False
        self.thread = threading.Thread(target=self.thread_loop)
        self.thread.name = id
        self.thread.start()

    def stop(self):
        self.stop_flag = True
        self.condition.notify()

    def stop_and_wait(self):
        self.stop()
        self.thread.join()

    def get_total_pending_rows(self):
        total_pending_rows_tmp = 0
        with self.lock:
            total_pending_rows_tmp = self.total_pending_rows
        return total_pending_rows_tmp

    def add_rows(self, symbol, rows) -> None:
        with self.lock:
            self.total_pending_rows += len(rows)
            logging.info(f"self.total_pending_rows: {self.total_pending_rows}")
            symbolDBWriter = self.symbolDBWriters.get(symbol)
            if not symbolDBWriter:
                symbolDBWriter = SymbolDBWriter(symbol)
                self.symbolDBWriters[symbol] = symbolDBWriter
                logging.info(
                    f"Added symbol: {symbol} in DBwriter: {self.id}, SymbolDBWriters so far is: {len(self.symbolDBWriters)}"
                )
            symbolDBWriter.pending_rows.extend(rows)
            self.condition.notify()

    def thread_loop(self):
        MAX_ROWS_PER_INSERT = 10000
        while True:
            db_writers_with_pending_rows = []
            with self.condition:
                # self.lock is locked now
                for _, symbolDBWriter in self.symbolDBWriters.items():
                    rows_to_add = len(symbolDBWriter.pending_rows)
                    if rows_to_add:
                        if (rows_to_add + len(db_writers_with_pending_rows)) > MAX_ROWS_PER_INSERT:
                            rows_to_add = MAX_ROWS_PER_INSERT - len(db_writers_with_pending_rows)
                        db_writers_with_pending_rows.append(
                            {
                                "symbolDBWriter": symbolDBWriter,
                                "pending_rows": symbolDBWriter.pending_rows[:rows_to_add],
                            }
                        )
                        symbolDBWriter.pending_rows = symbolDBWriter.pending_rows[rows_to_add:]
                if len(db_writers_with_pending_rows) == 0:
                    if self.stop_flag:
                        break
                    else:
                        logging.info("Wating for condition")
                        # wait to be notified
                        self.condition.wait()
                        logging.info("Wating for condition DONE")
                        continue
            # now self.lock is unlocked
            rows_inserted = 0
            for next_job in db_writers_with_pending_rows:
                logging.info(
                    f"Added {len(next_job['pending_rows'])} rows for symbol: {next_job['symbolDBWriter'].symbol} by DBwriter: {self.id}"
                )
                rows_inserted = len(next_job["pending_rows"])
                next_job["symbolDBWriter"].write(next_job["pending_rows"])
            with self.lock:
                self.total_pending_rows -= rows_inserted
                if self.total_pending_rows < 0:
                    logging.error(f"self.total_pending_rows ({self.total_pending_rows}) become negative")
                else:
                    logging.info(f"self.total_pending_rows: {self.total_pending_rows}")


class GDriveSyncManager:
    def __init__(self) -> None:
        self.number_of_DB_writers = int(os.cpu_count() * 0.75)
        if len(sys.argv) > 1:
            self.number_of_DB_writers = int(sys.argv[1])
        self.next_DB_writer_index = 0
        self.DBWriters = [DBWriter(f"DBWriters_{id + 1}") for id in range(0, self.number_of_DB_writers)]
        self.symbolToDBWriter = {}

    def get_DB_writer(self, symbol):
        dbWriter = self.symbolToDBWriter.get(symbol)
        if not dbWriter:
            # symbol appered for the fisrt time
            dbWriter = self.DBWriters[self.next_DB_writer_index]
            self.symbolToDBWriter[symbol] = dbWriter
            logging.info(f"Mapped symbol:{symbol} to :{self.symbolToDBWriter[symbol].id}")
            self.next_DB_writer_index += 1
            if self.next_DB_writer_index >= self.number_of_DB_writers:
                self.next_DB_writer_index = 0
        return dbWriter

    def stop_all_DB_writers(self):
        for dbWriter in self.DBWriters:
            dbWriter.stop()
        for dbWriter in self.DBWriters:
            dbWriter.stop_and_wait()
        self.DBWriters = []

    def wait_until_RAM_usage_is_less_then(self, gb):
        while True:
            cgb = process.memory_info().rss / ONE_GB
            if cgb < gb:
                return
            logging.info(f"RAM usage is {cgb} GB, not less than {gb} GB, sleeping..")
            time.sleep(1)

    def wait_until_total_pending_rows_is_less_then(self, count):
        while True:
            total_pending_rows = 0
            for dbWriter in self.DBWriters:
                total_pending_rows += dbWriter.get_total_pending_rows()
            if total_pending_rows < count:
                return
            logging.info(f"total_pending_rows:{total_pending_rows} is not less than {count}, sleeping..")
            time.sleep(1)

    def zip_to_sqlite(self, filename, year, month):
        if len(sys.argv) > 2:
            self.wait_until_RAM_usage_is_less_then(int(sys.argv[2]))
        else:
            self.wait_until_RAM_usage_is_less_then(2)

        rows_inserted = 0
        with ZipFile(filename) as zf:
            for file in zf.namelist():
                # self.wait_until_total_pending_rows_is_less_then(14800000)
                symbol_to_rows_dict = {}
                # logging.info(f"file:{file}, year:{year}, month:{month}")
                if file.endswith(".zip"):
                    continue
                with zf.open(file, "r") as myfile:
                    csv_reader = csv.reader(StringIO(myfile.read().decode("utf-8")))
                    for row in csv_reader:
                        symbol = row[0]
                        symbol_to_rows = symbol_to_rows_dict.get(symbol)
                        if not symbol_to_rows:
                            symbol_to_rows = []
                            symbol_to_rows_dict[symbol] = symbol_to_rows
                        symbol_to_rows.append(row)
                for symbol, rows in symbol_to_rows_dict.items():
                    rows_inserted += len(rows)
                    dbWriter = self.get_DB_writer(symbol)
                    dbWriter.add_rows(symbol, rows)

            # break
            # sys.exit(0)
        return rows_inserted

    def sync_from_gdrive_data(self):
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
                logging.info(path)
                onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
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
                    monthly_data_file = os.path.join(path, monthly_data_file)
                    logging.info(f"monthly_data_file:{monthly_data_file}")
                    pr = cProfile.Profile()
                    pr.enable()
                    rows_inserted = self.zip_to_sqlite(monthly_data_file, year, month)
                    pr.disable()
                    s = StringIO()
                    sortby = SortKey.CUMULATIVE
                    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
                    ps.print_stats()
                    # lp = LineProfiler()
                    # lp_wrapper = lp(self.zip_to_sqlite)
                    # rows_inserted = lp_wrapper(monthly_data_file, year, month)
                    total_rows_inserted += rows_inserted
                    logging.info(
                        f"year:{year}, month:{month}, rows_inserted:{rows_inserted}, total_rows_inserted:{total_rows_inserted}"
                    )
                    logging.info(f"Profile Stats:{s.getvalue()}")
                else:
                    logging.info(
                        f"year:{year}, month:{month} monthly_data_file not found !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                    )
                    for day_of_month in list(range(1, 32)):
                        daily_file_name = f"{day_of_month:02}{month}.zip"
                        daily_file_name = os.path.join(path, daily_file_name)
                        if not os.path.exists(daily_file_name):
                            continue
                        logging.info(f"daily_file_name:{daily_file_name}")

                        pr = cProfile.Profile()
                        pr.enable()
                        rows_inserted = self.zip_to_sqlite(daily_file_name, year, month)
                        pr.disable()
                        s = StringIO()
                        sortby = SortKey.CUMULATIVE
                        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
                        ps.print_stats()
                        # lp = LineProfiler()
                        # lp_wrapper = lp(self.zip_to_sqlite)
                        # rows_inserted = lp_wrapper(daily_file_name, year, month)
                        # rows_inserted = zip_to_sqlite(daily_file_name, year, month)
                        total_rows_inserted += rows_inserted
                        logging.info(
                            f"year:{year}, month:{month}, rows_inserted:{rows_inserted}, total_rows_inserted:{total_rows_inserted}"
                        )
                        # stringIO = StringIO()
                        # lp.print_stats(stream=stringIO)
                        logging.info(f"Stats:{s.getvalue()}")
        self.stop_all_DB_writers()
        logging.info("*********************** DONE ***********************")


gDriveSyncManager = GDriveSyncManager()
gDriveSyncManager.sync_from_gdrive_data()
