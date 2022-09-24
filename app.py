#!/usr/bin/env python
# coding: utf-8
import re
import socket
import sys

from PySide6.QtGui import QIcon, Qt, QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QStyle, QTableView, QHeaderView,
)
from ping3 import ping


def get_host_ip():
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    return ip


class PingAll(QMainWindow):
    __version__ = '20220924'
    appname = 'PingAll'
    pattern_cidr = re.compile('(\d{1,3}\.\d{1,3}\.\d{1,3}\.)\d{1,3}')

    def __init__(self):
        super().__init__()
        ip_host = get_host_ip()
        self.setWindowTitle('%s - %s' % (self.appname, ip_host))
        self.setWindowIcon(
            QIcon(self.style().standardIcon(QStyle.SP_TitleBarMenuButton))
        )
        list_addr_live = self.get_live_address(ip_host)
        print(list_addr_live)
        list_header = ['IP ADDRESS', 'HOSTNAME']

        self.init_ui(list_addr_live, list_header)

    def init_ui(self, list_address, list_header):
        # table
        table = QTableView()
        self.setCentralWidget(table)
        table.setWordWrap(False)
        table.setCornerButtonEnabled(True)
        table.setStyleSheet(
            'QTableCornerButton::section {border:1px outset #ccc;}'
        )
        table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        table.verticalHeader().setDefaultAlignment(Qt.AlignRight)
        table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        # model for table
        model = QStandardItemModel()
        table.setModel(model)
        model.setHorizontalHeaderLabels(list_header)
        for addr in list_address:
            list_row = list()
            for info in addr:
                item = QStandardItem(info)
                item.setEditable(False)
                list_row.append(item)
            #list_row = [QStandardItem(addr)]
            model.appendRow(list_row)

    def get_live_address(self, ip):
        m = self.pattern_cidr.match(ip)
        if not m:
            return list()
        body = m.group(1)
        list_addr_all = [body + str(x) for x in range(1, 255)]
        list_addr_live = [[addr, ''] for addr in list_addr_all if ping(addr, timeout=1) is not None]
        return list_addr_live


def main():
    app = QApplication(sys.argv)
    ex = PingAll()
    ex.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
