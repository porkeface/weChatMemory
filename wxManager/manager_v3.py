# wxManager/manager_v3.py
import sqlite3
from .database_interface import DataBaseInterface

class ManagerV3(DataBaseInterface):
    def __init__(self, micro_msg_db_path, msg_db_path=None):
        self.micro_msg_db = micro_msg_db_path
        self.msg_db_path = msg_db_path or micro_msg_db_path
        self.conn = sqlite3.connect(self.micro_msg_db)
        self.conn.row_factory = sqlite3.Row

    def getContacts(self):
        # Example: MicroMsg usually stores contact in "Friends" or similar table
        possible = [
            "SELECT rowid AS id, UserName, NickName, Remark FROM Friend",
            "SELECT rowid AS id, UserName, NickName, Remark FROM Contact"
        ]
        for sql in possible:
            try:
                cur = self.conn.execute(sql)
                rows = cur.fetchall()
                if rows:
                    return [dict(r) for r in rows]
            except Exception:
                continue
        return []

    def getMessages(self, contact_id=None, limit=None):
        # Msg table may be called "message" or "Msg"; try common names
        possible = [
            "SELECT rowid AS id, CreateTime, Talker, Content, Type FROM Message",
            "SELECT rowid AS id, CreateTime, Talker, Content, Type FROM Msg",
            "SELECT rowid AS id, CreateTime, Talker, Content, Type FROM message"
        ]
        for sql in possible:
            try:
                q = sql
                params = []
                if contact_id:
                    q += " WHERE Talker=?"
                    params.append(contact_id)
                q += " ORDER BY CreateTime"
                if limit:
                    q += " LIMIT ?"
                    params.append(limit)
                cur = self.conn.execute(q, params)
                rows = [dict(r) for r in cur.fetchall()]
                return rows
            except Exception:
                continue
        return []