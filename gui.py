#!/usr/bin/python
import sys
if sys.version_info < (3, 0):
    from Tkinter import *
    import ttk
else:
    from tkinter import *
    from tkinter import ttk

import os
import tempfile
import subprocess
import utils

#TODO: tagging logic
#TODO: rename button
#TODO: pic process and grouping
#TODO: ads identify
#TODO: categorize to tag folder
#TODO: highlight color
#TODO: tag cache
#TODO: path comparasion
#TODO: bug: sometimes ShowInExplorer doesn't work
#TODO: time span report
#TODO: UI and algorithm performance optimization

class UI:
    
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
        columns = ['name', 'duplicate', 'tag', 'ID', 'size (bytes)', 'readableSize']
        self.treeViewFiles = ttk.Treeview(self.frameList, height = 30, columns = columns)#show = 'headings'
        self.vbar = ttk.Scrollbar(self.frameList, orient = VERTICAL, command = self.treeViewFiles.yview)
        self.treeViewFiles.configure(yscrollcommand = self.vbar.set)
        
        self.treeViewFiles.column('#0', width=100, anchor='w')
        self.treeViewFiles.column('name', width=500, anchor='w')
        self.treeViewFiles.column('duplicate', width=100, anchor='w')
        self.treeViewFiles.column('tag', width=100, anchor='w')
        self.treeViewFiles.column('ID', width=100, anchor='w')
        self.treeViewFiles.column('size (bytes)', width=150, anchor='w')
        self.treeViewFiles.column('readableSize', width=150, anchor='w')
        self.treeViewFiles.heading('name', text='name')
        self.treeViewFiles.heading('duplicate', text='duplicate')
        self.treeViewFiles.heading('tag', text='tag')
        self.treeViewFiles.heading('ID', text='ID')
        self.treeViewFiles.heading('size (bytes)', text='size (bytes)') 
        self.treeViewFiles.heading('readableSize', text='readable size') 
        for col in columns:
            self.treeViewFiles.heading(col, text=col, command=lambda _col=col: self.treeviewSortColumn(self.treeViewFiles, _col, False))
        self.treeViewFiles.pack(side=LEFT)
        self.vbar.pack(side=LEFT, fill=Y)
        self.frameList.pack()

    def initSearchArea(self):
        self.frameSearch = Frame(self.root, height = self.kWidgetHeight, width = self.kWidgetWidth)
        self.labelPromptPaths = Label(self.frameSearch, text = 'Input multiple paths devided by space, e.g., c:\path1 d:\path2 f:\path3')
        self.txtPaths = Text(self.frameSearch, width = 100, height = 1)
        self.btnSearch = Button(self.frameSearch, text = 'Search', width = 10, height = 1, command = self.onSearch)
        self.labelPromptPaths.grid(row = 0, column = 0)
        self.txtPaths.grid(row = 1, column = 0, padx = 10)
        self.btnSearch.grid(row = 1, column = 1, padx = 10)
        #self.labelPromptPaths.pack()
        #self.txtPaths.pack(side=LEFT)
        #self.btnSearch.pack(side=RIGHT)
        self.frameSearch.pack()

    def initControlArea(self):
        self.frameFileOperation = Frame(self.root, height = self.kWidgetHeight, width = self.kWidgetWidth)
        self.btnOpenInExplorer = Button(self.frameFileOperation, text = 'Show selections in explorer', width = 30, height = 1, command = self.onShowInExplorer)
        self.btnOpenInExplorer.grid(row = 0, column = 0, padx = 10)
        #self.btnMoveToTrash = Button(self.frameFileOperation, text = 'Move to trash', width = 20, height = 1, command = self.onMoveToTrash)
        self.btnMarkAsInnocent = Button(self.frameFileOperation, text = 'Mark as Innocent', width = 30, height = 1, command = self.onMarkAsInnocent)
        self.btnMarkAsInnocent.grid(row = 0, column = 1, padx = 10)
        #self.btnOpenInExplorer.pack(side=LEFT)
        #self.btnMarkAsInnocent.pack(side=LEFT)
        #self.btnMoveToTrash.pack(side=RIGHT)
        self.frameFileOperation.pack()

    def initInfoArea(self):
        self.frameInfo = Frame(self.root, height = self.kWidgetHeight, width = self.kWidgetWidth)
        self.labelPromptTrash = Label(self.frameInfo, text = 'There\'s no beautiful way to send files to trash, please do it manually, check below link for more info')
        self.labelPromptTrashLink = Text(self.frameInfo, height=1, borderwidth=0)
        self.labelPromptTrashLink.insert(1.0, 'https://www.hardcoded.net/articles/send-files-to-trash-on-all-platforms.htm')
        self.labelPromptTrashLink.configure(state = "disabled")
        self.labelPromptTrashLink.configure(inactiveselectbackground = self.labelPromptTrashLink.cget("selectbackground"))
        self.labelPromptShowInExplorer = Label(self.frameInfo, text = 'Also ShowInExplorer sometimes doesn\' work, try more if so, and try closing other explorer windows if still so')
        self.labelDupInfo = Label(self.frameInfo, text = '', fg = 'red')
        self.labelPromptTrash.pack()
        self.labelPromptTrashLink.pack()
        self.labelPromptShowInExplorer.pack()
        self.labelDupInfo.pack()
        self.frameInfo.pack()

    def initWidgets(self):
        self.forePlay()
        self.initSearchArea()
        self.initControlArea()
        self.initInfoArea()

        self.initListArea()

    def run(self):
        self.root.mainloop()

    def onSearch(self):
        rawPaths = self.txtPaths.get("0.0", "end")
        paths = rawPaths.split()
        #self.searchResult = utils.getFileList(['g:\\av', 'f:\\sn', 'e:\\sn'])
        self.searchResult = utils.getFileList(paths)
        self.refreshList()

    def onShowInExplorer(self):
        for item in self.treeViewFiles.selection():
            #print(r'explorer /select, ' + self.treeViewFiles.item(item,"values")[6])
            subprocess.Popen(r'explorer /select, ' + self.treeViewFiles.item(item,"values")[6])

    def onMoveToTrash(self):
        for item in self.treeViewFiles.selection():
            cmd = r'recycle ' + self.treeViewFiles.item(item,"values")[6]
            print(cmd)
            subprocess.Popen(cmd)

    def onMarkAsInnocent(self):
        for item in self.treeViewFiles.selection():
            #print(r'explorer /select, ' + self.treeViewFiles.item(item,"values")[6])
            if len(self.treeViewFiles.item(item,"values")) > 8:
                i = self.treeViewFiles.item(item,"values")[7]
                j = self.treeViewFiles.item(item,"values")[8]
                self.searchResult[int(i)].innocentSimilarFileList[int(j)] = True
            #subprocess.Popen(r'explorer /select, ' + self.treeViewFiles.item(item,"values")[6])
        self.refreshList()
        return

    def refreshList(self):
        children = self.treeViewFiles.get_children()
        for item in children:
            self.treeViewFiles.delete(item)
        dupCount, dupSize = utils.analyzeDuplicate(self.searchResult)
        i = 0
        totalSize = 0
        for f in self.searchResult:
            totalSize += f.size
            suffix = ' dup'
            if len(f.similarFileList) - f.innocentNum() > 1:
                suffix = ' dups'
            item = self.treeViewFiles.insert('', 'end', text=str(len(f.similarFileList)) + suffix, values=[f.name, len(f.similarFileList) - f.innocentNum(), \
            f.JAVTag, f.JAVTag + ' ' + f.JAVNum, f.size, f.readableSizeStr(), f.fullPath])
            if (len(f.similarFileList) > 0):
                j = 0
                displayDumIndex = 0
                for child in f.similarFileList:
                    if f.innocentSimilarFileList[j] == False:
                        obj = self.searchResult[child]
                        self.treeViewFiles.insert(item, 'end', text='dup ' + str(displayDumIndex), values=[obj.name, '-', obj.JAVTag, obj.JAVTag \
                        + ' ' + obj.JAVNum, obj.size, obj.readableSizeStr(), obj.fullPath, i, j])
                        displayDumIndex += 1
                    j += 1
            i += 1
        self.labelDupInfo.config(text = 'potential duplicated files: ' + str(dupCount) + ', their size: ' + utils.readableSizeStr(dupSize) \
        + ', total file count: ' + str(len(self.searchResult)) + ', total size: ' + utils.readableSizeStr(totalSize) + ', dup rate: ' + str(round(dupSize / totalSize, 3) * 100) + '%')




if __name__ == '__main__':
    ui = UI()
    ui.initWidgets()
    ui.run()