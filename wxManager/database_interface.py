# wxManager/database_interface.py
class DataBaseInterface:
    def getContacts(self):
        """Return list of contact dicts: {id, username, nickname, remark}"""
        raise NotImplementedError


    def getMessages(self, contact_id=None, limit=None):
        """Return list of message dicts: {id, talker, create_time, content, type}"""
        raise NotImplementedError