import os
import sys

# Always force project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from sb_client.db_client import fetch_table

rows = fetch_table("raw_data")
print("ROWS FETCHED:", len(rows))

if len(rows) > 0:
    print("Sample:", rows[0])
