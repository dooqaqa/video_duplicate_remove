#!/usr/bin/python
import os, name_parser
from video_file_descriptor import VideoFileDescriptor
name_parser.initCheckPointList()

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
                    javTag = ''
                    if name_parser.isVOB(name):
                        javTag = name_parser.getJAVTag(root)
                    elif 'pornhub' not in full_name.lower():
                        javTag = name_parser.getJAVTag(name)
                    fileList.append(VideoFileDescriptor(name, full_name, javTag, os.path.getsize(full_name)))
                    if javTag != '':
                        JAVNum += 1
                        printColorMessage(str(JAVNum) + ': ' + full_name, 32)
                        #printColorMessage(str(result[0]), 36)
                    else:
                        nonJAVNum += 1
                        printColorMessage(str(nonJAVNum) + ': ' + full_name, 31)
            '''for name in dirs:
                print(os.path.join(root, name))'''
    for i in range(0, 8):
        successCount = 0
        for f in fileList:
            if f.analyzeJAVTag(i < 7):
                successCount += 1
        print('analyzing JAV tag, round ' + str(i) + ': ' + str(successCount) + ' results adjusted')
    return fileList

def analyzeDuplicate(fileList):
    dupFileCount = 0
    dupFileSize = 0
    for i in range(0, len(fileList)):
        if len(fileList[i].similarFileList) == 0:
            for j in range(0, len(fileList)):
                if i == j or name_parser.siblingVOB(fileList[i], fileList[j]):
                    continue
                if name_parser.isDuplicated(fileList[i], fileList[j]):
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