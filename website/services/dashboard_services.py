from db.conn import get_connection
from db.repo import load_query

def get_dashboard_stats():

    stats = {}
    
    conn = get_connection()
    try:
        with conn.cursor() as cur:

            cur.execute(load_query("check_db_disk_space"))
            stats["db_usage"] = cur.fetchall()
            
            cur.execute(load_query("check_rows_length"))
            stats["rows_length"] = cur.fetchall()
    finally:
        conn.close()

    return stats