#!/usr/bin/env python3.6
# -*- coding:utf-8 -*-
__author__ = '共勉之'
__date__ = '2020.05.09'
__email__ = '768577220@qq.com'
__description__ = ''


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Demo(QDialog):
    def __init__(self):
        super(Demo, self).__init__()

        self.search_tree = QTreeWidget(self)
        self.search_tree.setColumnCount(1)

        for i in range(5):
            item = QTreeWidgetItem()
            item.setText(0, 'test{}'.format(i))
            child = QTreeWidgetItem(item)
            child.setText(0, 'child{}'.format(i))
            item.addChild(child)
            self.search_tree.addTopLevelItem(item)

        self.initLineeditView()
        self.searchHightLight()

    def initLineeditView(self):
        self.lineedit = QLineEdit()
        self.lineedit.setPlaceholderText("请输入搜索内容")  # 设置lineedit背景提示词
        layout = QVBoxLayout(self)
        layout.addWidget(self.search_tree)
        layout.addWidget(self.lineedit)

    def searchHightLight(self):
        self.completer = QCompleter(self)
        string_list_model = QStringListModel()
        search_list = []
        for i in range(self.search_tree.model().rowCount()):
            index = self.search_tree.model().index(i, 0)
            item = self.search_tree.itemFromIndex(index)
            search_list.append(item.text(0))
            for i in range(item.childCount()):
                search_list.append(item.child(i).text(0))

        string_list_model.setStringList(search_list)
        self.completer.setModel(string_list_model)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)
        self.lineedit.setCompleter(self.completer)
        self.completer.highlighted.connect(self.highlight)

    def highlight(self, toolString):
        items = self.search_tree.findItems(toolString, Qt.MatchRecursive)
        if len(items) == 0:
            return
        index = self.search_tree.indexFromItem(items[0])
        self.search_tree.selectionModel().select(index, QItemSelectionModel.ClearAndSelect |
                                                 QItemSelectionModel.Rows)
        self.search_tree.scrollTo(index)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Demo()
    window.resize(500, 300)
    window.show()
    sys.exit(app.exec_())
