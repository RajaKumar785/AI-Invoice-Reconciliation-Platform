import os
import sqlite3
from datetime import datetime

# --------------------------------------------------
# Database Path
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(BASE_DIR, "invoice_data.db")


# --------------------------------------------------
# Database Connection
# --------------------------------------------------

def get_connection():
    return sqlite3.connect(DATABASE)


# --------------------------------------------------
# Create Tables
# --------------------------------------------------

def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS invoices(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        po_number TEXT,

        invoice_number TEXT,

        vendor TEXT,

        amount REAL,

        gst TEXT,

        status TEXT,

        match_score REAL,

        processed_time TEXT

    )
    """)

    conn.commit()
    conn.close()


# --------------------------------------------------
# Save Invoice
# --------------------------------------------------

def save_invoice(po_json, invoice_json, result):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        amount = invoice_json.get("Amount", 0)

        try:
            amount = float(
                str(amount)
                .replace(",", "")
                .replace("₹", "")
                .replace("INR", "")
                .strip()
            )
        except ValueError:
            amount = 0.0

        cursor.execute("""
        INSERT INTO invoices(

            po_number,
            invoice_number,
            vendor,
            amount,
            gst,
            status,
            match_score,
            processed_time

        )

        VALUES(?,?,?,?,?,?,?,?)

        """, (

            po_json.get("PO Number", ""),
            invoice_json.get("Invoice Number", ""),
            invoice_json.get("Vendor", ""),
            amount,
            invoice_json.get("GST", ""),
            result.get("status", "HOLD"),
            result.get("score", 0),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        ))

        conn.commit()

    finally:

        conn.close()


# --------------------------------------------------
# Invoice History
# --------------------------------------------------

def get_invoice_history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT

        po_number,
        invoice_number,
        vendor,
        amount,
        gst,
        status,
        match_score,
        processed_time

    FROM invoices

    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# --------------------------------------------------
# Duplicate Invoice Check
# --------------------------------------------------

def invoice_exists(invoice_number):

    if not invoice_number:
        return False

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT invoice_number
    FROM invoices
    WHERE invoice_number = ?
    """, (invoice_number,))

    data = cursor.fetchone()

    conn.close()

    return data is not None


# --------------------------------------------------
# Initialize Database
# --------------------------------------------------

create_tables()