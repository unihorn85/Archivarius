#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QFileDialog

from archive import *
from Core import *

class MyForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.lw = self.ui.listWidget
        self.close_Archive()
        self.ui.create_archive.triggered.connect(self.createArcDialog)
        self.ui.open_archive.triggered.connect(self.openArcDialog)
        self.ui.Exit.triggered.connect(self.quit)
        self.ui.button_create.clicked.connect(self.create_Archive)
        self.ui.button_add.clicked.connect(self.add_to_Archive)
        self.ui.button_unpack.clicked.connect(self.unpack_Archive)
        self.ui.button_unpack_all.clicked.connect(self.unpackall_Archive)
        self.ui.button_close.clicked.connect(self.close_Archive)
        self.show()

    def createArcDialog(self):
        """Получаем имя нового файла"""
        fname, ok = QFileDialog.getSaveFileName(self,"Создаём архив","","Zip Files (*.zip)")
        if ok:
            if os.path.exists(fname):
                os.remove(fname)
            self.arc = Archiver(fname, 'zip')
            self.ui.label_info.setText("Текущий файл %s" % fname)
            self.ui.statusbar.showMessage("Добавьте файлы в архив")
            self.button_access(True, True, False)
            
    def openArcDialog(self):
        """Получаем и отображаем архивный файл"""
        fname, ok = QFileDialog.getOpenFileName(self, 'Открыть архив', os.getcwd(), "Zip Files (*.zip)")
        if ok:
            self.arc = Archiver(fname, 'zip')
            self.ui.label_info.setText("Текущий файл %s" % fname)
            self.ui.statusbar.showMessage("Можете распаковать файлы или добавить новые")
            self.lw.clear()
            self.lw.addItems(self.arc.infoArc())
            self.button_access(True, True, True)
            
    def quit(self):
        QApplication.quit()
            
    def create_Archive(self):
        """Сохраняем архив"""
        self.arc.createArc()
        self.lw.clear()
        self.lw.addItems(self.arc.infoArc())
        self.arc.files = dict()
        self.ui.statusbar.showMessage("Можете распаковать файлы или добавить новые")
        
        
    def add_to_Archive(self):
        """Добавляем файлы в список для архивации"""
        dialog = QFileDialog(self)
        dialog.setFileMode(dialog.ExistingFiles)
        dialog.setOption(dialog.DontUseNativeDialog, True)
        dialog.accept = lambda: QtWidgets.QDialog.accept(dialog)
        dialog.setDirectory(os.getcwd())
        dialog.exec_()
        сhoice = []
        choice = dialog.selectedFiles()
        for elem in choice:
            if os.path.isfile(elem):
                self.lw.addItem(elem)
                self.arc.files.update({elem: os.path.basename(elem)})
            if os.path.isdir(elem):
                base = os.path.basename(elem)
                for root, dirs, files in os.walk(elem):
                    self.lw.addItem(elem)
                    for file in files:
                        tmp = os.path.join(root,file)
                        self.lw.addItem(tmp)
                        tmp_ac = base + tmp.split(os.path.basename(base))[-1]
                        self.arc.files.update({tmp: tmp_ac})
            self.button_access(True, True, True)
            
            
    def unpack_Archive(self):
        """Распаковываем выделенные элементы"""
        path = None
        path = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        items = [x.text() for x in self.lw.selectedItems()]
        if path:
            self.arc.unpackArc(path, items)
        
    def unpackall_Archive(self):
        """Распаковываем весь архив"""
        path = None
        path = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения")
        if path:
            self.arc.unpackArc(path)

    def close_Archive(self):
        """Закрытие архива"""
        self.arc = None
        self.lw.clear()
        self.ui.label_info.setText("Текущий файл отсутствует")
        self.ui.statusbar.showMessage("Откройте или создайте архив")
        self.button_access(False, False, False)
            
    def button_access(self, save, add, unpack):
        """Изменение доступности кнопок в зависимости от режима работы приложения"""
        self.ui.button_create.setEnabled(save)
        self.ui.button_add.setEnabled(add)
        self.ui.button_unpack.setEnabled(unpack)
        self.ui.button_unpack_all.setEnabled(unpack)
        self.ui.button_close.setEnabled(add)

if __name__=="__main__":    
    app = QApplication(sys.argv)
    w = MyForm()
    w.show()
    sys.exit(app.exec_())
