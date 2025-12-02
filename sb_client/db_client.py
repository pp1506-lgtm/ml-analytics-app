import os
import sys
from dotenv import load_dotenv
from supabase import create_client

# Ensure project root is in sys.path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Load .env
load_dotenv(os.path.join(ROOT, ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ ENV ERROR: Supabase URL/KEY not loaded")
else:
    print("✅ ENV LOADED")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_table(table):
    return supabase.table(table).select("*").execute().data

def insert_table(table, rows):
    return supabase.table(table).insert(rows).execute()

