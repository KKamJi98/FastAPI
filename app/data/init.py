# TODO Review


"""SQLite 데이터베이스를 초기화"""
import os
from pathlib import Path
from sqlite3 import connect, Connection, Cursor, IntegrityError

conn: Connection | None = None
curs: Cursor | None = None


def get_db(name: str | None = None, reset: bool = False):
    """SQLite 데이터베이스 파일에 연결"""
    global conn, curs

    if conn:
        return conn

    if conn is None:
        if not name:
            name = os.getenv("CRYPTID_SQLITE_DB")
            if not name:
                top_dir = Path(__file__).resolve().parents[1]
                db_dir = top_dir / "db"
                db_dir.mkdir(exist_ok=True)
                db_name = "cryptid.db"
                name = str(object=db_dir / db_name)

        conn = connect(name, check_same_thread=False)
        curs = conn.cursor()

    if reset:
        curs.execute("DROP TABLE IF EXISTS explorer")
        curs.execute("DROP TABLE IF EXISTS creature")
        curs.execute("DROP TABLE IF EXISTS user")
        curs.execute("DROP TABLE IF EXISTS xuser")
        conn.commit()

    return conn


get_db()
# get_db(reset=True)
