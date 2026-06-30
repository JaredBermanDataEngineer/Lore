import sqlite3

from .db.init_db import init_db
from .load_bronze import load_bronze
from .load_gold import load_gold


def etl():
    ############ INIT DB ###############################
    # For POC purposes only. In production never couple DDLs with ETLs. Use a proper migration system.

    conn = sqlite3.connect("output/warehouse.db")
    init_db(conn)

    ############ LOAD RAW DATA INTO BRONZE LAYER DB ####
    load_bronze(conn)

    ############ LOAD GOLD TABLES ######################
    load_gold(conn)

    conn.close()
