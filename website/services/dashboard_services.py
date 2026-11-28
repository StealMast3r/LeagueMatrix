from db.conn import get_connection
from db.repo import load_query

def get_dashboard_stats():

    stats = {}
    
    conn = get_connection()
    try:
        with conn.cursor() as cur:

            cur.execute("""
                SELECT TABLE_NAME
                FROM information_schema.TABLES
                WHERE TABLE_SCHEMA = DATABASE()
                AND TABLE_TYPE = 'BASE TABLE'
            """)
            tables = cur.fetchall()
            for row in tables:
                table_name = row["TABLE_NAME"]
                cur.execute(f"ANALYZE TABLE `{table_name}`")
                cur.fetchall()

            cur.execute(load_query("check_db_disk_space"))
            stats["db_usage"] = cur.fetchall()
            
            cur.execute(load_query("check_rows_length"))
            stats["rows_length"] = cur.fetchall()
    finally:
        conn.close()

    return stats