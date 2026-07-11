import sqlite3

conn = sqlite3.connect(
    "invoice_data.db",
    check_same_thread=False
)

cursor = conn.cursor()