from db.conn import get_connection
from db.repo import load_query

def get_dashboard_stats():

    
    
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(load_query("get_dashboard_stats"))
            return cur.fetchone()
    finally:
        conn.close()