# gui/main_window.py
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QListWidget, QPushButton, QTextEdit, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('WeChatChatExporter - Demo')
        self.resize(900, 600)

        h = QHBoxLayout(self)
        left_v = QVBoxLayout()
        right_v = QVBoxLayout()

        self.contact_list = QListWidget()
        self.contact_list.itemClicked.connect(self.on_contact_click)
        left_v.addWidget(self.contact_list)

        self.btn_refresh = QPushButton('Load Contacts')
        self.btn_refresh.clicked.connect(self.load_contacts)
        left_v.addWidget(self.btn_refresh)

        self.btn_export_html = QPushButton('Export HTML')
        self.btn_export_html.clicked.connect(self.export_html)
        left_v.addWidget(self.btn_export_html)

        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)
        right_v.addWidget(self.chat_view)

        h.addLayout(left_v, 3)
        h.addLayout(right_v, 7)

        self.setLayout(h)

    def load_contacts(self):
        self.contact_list.clear()
        contacts = self.manager.getContacts()
        for c in contacts:
            display = c.get('NickName') or c.get('Remark') or c.get('UserName')
            # store full dict in QListWidgetItem's data
            item = self.contact_list.addItem(display)
        QMessageBox.information(self, 'Loaded', f'Loaded {len(contacts)} contacts')

    def on_contact_click(self, item):
        # find contact by display text (simple demo)
        text = item.text()
        contacts = self.manager.getContacts()
        sel = None
        for c in contacts:
            display = c.get('NickName') or c.get('Remark') or c.get('UserName')
            if display == text:
                sel = c
                break
        if not sel:
            return
        messages = self.manager.getMessages(contact_id=sel.get('UserName'))
        self.chat_view.clear()
        for m in messages:
            line = f"{m.get('CreateTime')}\t{m.get('Talker')}\t{m.get('Content')}\n"
            self.chat_view.append(line)