#!/usr/bin/python
from tkinter import *
from tkinter import ttk
import os
import tempfile
import subprocess
import utils

#TODO: tagging logic △
#TODO: trash button(red)
#TODO: rename button
#TODO: pic process and grouping
#TODO: dvd files process △
#TODO: ads
#TODO: categorize to tag folder
#TODO: highlight color
#TODO: tag cache
#TODO: show dup √
#TODO: dup statistics

class UI:
    root = None
    btnStart = None
    ICON_PATH = None
    btnSearch = None
    btnMoveToTrash = None
    btnOpenInExplorer = None
    listboxFiles = None
    txtPaths = None
    frameSearch = None
    frameFileOperation = None
    frameList = None
    kWidgetWidth = 800
    kWidgetHeight = 100

    def replaceLogo(self):
        ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
                b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
                b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
                b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64
        _, self.ICON_PATH = tempfile.mkstemp()
        with open(self.ICON_PATH, 'wb') as icon_file:
            icon_file.write(ICON)
 
    def treeviewSortColumn(self, tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        #print(tv.get_children(''))
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
            #print(k)
        tv.heading(col, command=lambda: self.treeviewSortColumn(tv, col, not reverse))
    
    def forePlay(self):
        self.replaceLogo()
        self.root = Tk()
        self.root.iconbitmap(default=self.ICON_PATH)
        self.root.wm_title("video duplicate removal")

    def initListArea(self):
        self.frameList = Frame(self.root, height = self.kWidgetHeight, width = self.kWidgetWidth)
        #self.listboxFiles = Listbox(self.frameList, width = 50, height = 100, selectmode = EXTENDED)
        #self.listboxTags = Listbox(self.frameList, width = 50, height = 100, selectmode = EXTENDED)
        #self.listboxSizes = Listbox(self.frameList, width = 50, height = 100, selectmode = EXTENDED)
        columns = ['name', 'duplicate', 'tag', 'ID', 'size']
        self.treeViewFiles = ttk.Treeview(self.frameList, height = 30, columns = columns)#show = 'headings'
        self.vbar = ttk.Scrollbar(self.frameList, orient = VERTICAL, command = self.treeViewFiles.yview)
        self.treeViewFiles.configure(yscrollcommand = self.vbar.set)
        
        self.treeViewFiles.column('#0', width=100, anchor='w')
        self.treeViewFiles.column('name', width=500, anchor='w')
        self.treeViewFiles.column('duplicate', width=100, anchor='w')
        self.treeViewFiles.column('tag', width=100, anchor='w')
        self.treeViewFiles.column('ID', width=100, anchor='w')
        self.treeViewFiles.column('size', width=150, anchor='w')
        self.treeViewFiles.heading('name', text='name')
        self.treeViewFiles.heading('duplicate', text='duplicate')
        self.treeViewFiles.heading('tag', text='tag')
        self.treeViewFiles.heading('ID', text='ID')
        self.treeViewFiles.heading('size', text='size') 
        for col in columns:
            self.treeViewFiles.heading(col, text=col, command=lambda _col=col: self.treeviewSortColumn(self.treeViewFiles, _col, False))
        self.treeViewFiles.pack(side=LEFT)
        self.vbar.pack(side=LEFT, fill=Y)
        self.frameList.pack()

    def initSearchArea(self):
        self.frameSearch = Frame(self.root, height = self.kWidgetHeight, width = self.kWidgetWidth)
        self.txtPaths = Text(self.frameSearch, width = 100, height = 1)
        self.btnSearch = Button(self.frameSearch, text = 'Search', width = 10, height = 1, command = self.onSearch)
        self.txtPaths.pack(side=LEFT)
        self.btnSearch.pack(side=RIGHT)
        self.frameSearch.pack()

    def initControlArea(self):
        self.frameFileOperation = Frame(self.root, height = self.kWidgetHeight, width = self.kWidgetWidth)
        self.btnOpenInExplorer = Button(self.frameFileOperation, text = 'Show in explorer', width = 20, height = 1, command = self.onShowInExplorer)
        self.btnMoveToTrash = Button(self.frameFileOperation, text = 'Move to trash', width = 20, height = 1, command = self.onMoveToTrash)
        self.btnOpenInExplorer.pack(side=LEFT)
        self.btnMoveToTrash.pack(side=RIGHT)
        self.frameFileOperation.pack()

    def initWidgets(self):
        self.forePlay()
        self.initSearchArea()
        self.initControlArea()

        self.initListArea()

    def run(self):
        self.root.mainloop()
    
    def onSearch(self):
        children = self.treeViewFiles.get_children()
        for item in children:
            self.treeViewFiles.delete(item)
        self.searchResult = utils.getFileList(['F:\\sn'])
        utils.analyzeDuplicate(self.searchResult)
        for f in self.searchResult:
            suffix = ' dup'
            if len(f.sameSizeFileList) > 1:
                suffix = ' dups'
            item = self.treeViewFiles.insert('', 'end', text=str(len(f.sameSizeFileList)) + suffix, values=[f.name, len(f.sameSizeFileList), f.JAVTag, f.JAVTag + '-' + f.JAVNum, f.size, f.fullPath])
            if (len(f.sameSizeFileList) > 0):
                i = 0
                for child in f.sameSizeFileList:
                    obj = self.searchResult[child]
                    self.treeViewFiles.insert(item, 'end', text='dup ' + str(i), values=[obj.name, len(obj.sameSizeFileList), obj.JAVTag, obj.JAVTag + '-' + obj.JAVNum, obj.size, obj.fullPath])
                    i += 1
                print('___________123 ' + f.name + '__' + str(f.sameSizeFileList))

    def onShowInExplorer(self):
        for item in self.treeViewFiles.selection():
            subprocess.Popen(r'explorer /select, ' + self.treeViewFiles.item(item,"values")[5])

    def onMoveToTrash(self):
        print('onMoveToTrash')



if __name__ == '__main__':
    ui = UI()
    ui.initWidgets()
    ui.run()