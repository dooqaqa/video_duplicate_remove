#!/usr/bin/python
import os, name_parser, video_file_descriptor
from video_file_descriptor import VideoFileDescriptor

def printColorMessage(message, color):
    print('\033[1;' + str(color) + ';40m' + message + '\033[0m')

def getFileList(pathList):
    ls = []
    JAVNum = 0
    nonJAVNum = 0
    fileList = []
    for path in pathList:
        for root, dirs, files in os.walk(path, followlinks=True):
            for name in files:
                full_name = os.path.join(root, name)
                if name_parser.isVedio(name):
                    result = name_parser.parseJAV(name)
                    javTag = ''
                    if (len(result)) > 0 and not name_parser.isVOB(name):
                        #printColorMessage(str(result[0]), 36)
                        JAVNum += 1
                        fileList.append(VideoFileDescriptor(name, full_name, True, name_parser.getJAVTag(name), os.path.getsize(full_name)))
                        printColorMessage(str(JAVNum) + ': ' + full_name, 32)
                    elif name_parser.isVOB(name) and name_parser.parseJAV(root):
                        fileList.append(VideoFileDescriptor(name, full_name, True, name_parser.getJAVTag(root), os.path.getsize(full_name)))
                        JAVNum += 1
                        printColorMessage(str(JAVNum) + ': ' + full_name, 32)
                    else:
                        nonJAVNum += 1
                        fileList.append(VideoFileDescriptor(name, full_name, False, '', os.path.getsize(full_name)))
                        printColorMessage(str(nonJAVNum) + ': ' + full_name, 31)
            '''for name in dirs:
                print(os.path.join(root, name))'''
    for f in fileList:
        if f.isJAV:
            f.reAnalyzeJAVTag()
    return fileList

def analyzeDuplicate(fileList):
    dupFileCount = 0
    dupFileSize = 0
    #logic needs to be simplified
    for i in range(0, len(fileList)):
        if len(fileList[i].similarFileList) == 0:
            for j in range(0, len(fileList)):
                if i == j:
                    continue
                if name_parser.isVOB(fileList[i].name) and name_parser.isVOB(fileList[j].name) and (fileList[i].fullPath[:-5] == fileList[j].fullPath[:-5]):
                    continue
                if (fileList[i].isJAV and fileList[j].isJAV and fileList[i].JAVTag == fileList[j].JAVTag \
                and fileList[i].JAVNum == fileList[j].JAVNum) \
                or (not name_parser.isVOB(fileList[i].name) and not name_parser.isVOB(fileList[j].name) and fileList[i].size == fileList[j].size):
                    fileList[i].similarFileList.append(j)
            fileList[i].initInnocentList()
        if len(fileList[i].similarFileList) - fileList[i].innocentNum() > 0:
            dupFileCount += 1
            dupFileSize += fileList[i].size
    return dupFileCount, dupFileSize

def readableSizeStr(size):
    if size < 1024:
        return '' + size + 'Bytes'
    if size >= 1024 and size < 1048576:
        return '' + str(round(size / 1024, 2)) + 'KB'
    elif size >= 1048576 and size < 1073741824:
        return '' + str(round(size / 1048576, 2)) + 'MB'
    elif size > 1073741824:
        return '' + str(round(size / 1073741824, 2)) + 'GB'