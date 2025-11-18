# wxManager/manager_v4.py
import sqlite3
from .database_interface import DataBaseInterface

class ManagerV4(DataBaseInterface):
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def getContacts(self):
        sql = "SELECT rowid AS id, UserName, NickName, Remark FROM Contact"
        try:
            cur = self.conn.execute(sql)
            return [dict(r) for r in cur.fetchall()]
        except Exception as e:
            print("Error getContacts:", e)
            return []

    def getMessages(self, contact_id=None, limit=None):
        sql = "SELECT rowid AS id, CreateTime, Talker, Content, Type FROM Message"
        params = []
        if contact_id:
            sql += " WHERE Talker=?"
            params.append(contact_id)
        sql += " ORDER BY CreateTime"
        if limit:
            sql += " LIMIT ?"
            params.append(limit)
        try:
            cur = self.conn.execute(sql, params)
            rows = [dict(r) for r in cur.fetchall()]
            # Normalize keys
            msgs = []
            for r in rows:
                msgs.append({
                    'id': r.get('id'),
                    'create_time': r.get('CreateTime'),
                    'talker': r.get('Talker'),
                    'content': r.get('Content'),
                    'type': r.get('Type')
                })
            return msgs
        except Exception as e:
            print("Error getMessages:", e)
            return []