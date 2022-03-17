#!/usr/bin/env python
# -*- coding: utf-8 -*-
import zipfile
import os

class Archiver:
    def __init__(self, name, mode='zip'):
        self.name = name
        self.mode = mode
        self.files = dict()
        
    def __str__(self):
        return (
            f'Имя файла: {self.name} Формат файла: {self.mode}'
                )
                
    def createArc(self):
        # ~ print('Создание архива')
        with zipfile.ZipFile(self.name, 'a') as zf:
            for elem, arcname in self.files.items():
                print(elem, arcname)
                zf.write(elem, arcname=arcname)
        
    def unpackArc(self, path, filelist=None):
        # ~ print('Распаковка архива')
        if zipfile.is_zipfile(self.name):
            with zipfile.ZipFile(self.name, 'r') as zf:
                if filelist == None:
                    filelist = zf.namelist()
                zf.extractall(path=path, members=filelist, pwd=None)
        
        
    def infoArc(self):
        # ~ print('Информация по архиву')
        with zipfile.ZipFile(self.name, 'r') as zf:
            info = zf.namelist()
        # ~ print(info)
        return info
