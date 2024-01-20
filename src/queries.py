import sqlite3


class Query:
    def __init__(self, db="sources.db") -> None:
        self.con = sqlite3.connect(db)
        self.cur = self.con.cursor()

    def get_sources(self):
        res = self.cur.execute("Select * FROM sources").fetchall()
        self.close()
        return res
    
    def get_one_source(self, id):
        res = self.cur.execute("Select * FROM sources WHERE id=?", (id,)).fetchone()
        self.close()
        return res
    
    def get_source_extensions(self, id):
        res = self.cur.execute("SELECT * FROM extensions WHERE sourceId=?", (id,)).fetchall()
        self.close()
        return res

    def close(self):
        self.con.close()
