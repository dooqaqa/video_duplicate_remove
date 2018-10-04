#!/usr/bin/python
import os, name_parser, video_file_descriptor
from video_file_descriptor import VideoFileDescriptor

def printColorMessage(message, color):
    print('\033[1;' + str(color) + ';40m' + message + '\033[0m')

def getFileList(pathList):
    ls = []
    total_num = 0
    failed_num = 0
    fileList = []
    for path in pathList:
        for root, dirs, files in os.walk(path, followlinks=True):
            for name in files:
                full_name = os.path.join(root, name)
                if name_parser.isVedio(name):
                    result = name_parser.parseJAV(name)
                    javTag = ''
                    if (len(result)) > 0:
                        printColorMessage(str(result[0]), 36)
                        total_num += 1
                        fileList.append(VideoFileDescriptor(name, full_name, True, name_parser.getJAVTag(name), os.path.getsize(full_name)))
                        printColorMessage(str(total_num) + ':' + full_name, 32)
                    else:
                        failed_num += 1
                        fileList.append(VideoFileDescriptor(name, full_name, False, '', os.path.getsize(full_name)))
                        printColorMessage(str(failed_num) + full_name, 31)
            '''for name in dirs:
                print(os.path.join(root, name))'''
    for f in fileList:
        if f.isJAV:
            f.reAnalyzeJAVTag()
    return fileList

def analyzeDuplicate(fileList):
    for i in range(0, len(fileList)):
        for j in range(0, len(fileList)):
            if i == j:
                continue
            if (fileList[i].isJAV and fileList[j].isJAV and fileList[i].JAVTag == fileList[j].JAVTag and fileList[i].JAVNum == fileList[j].JAVNum) or fileList[i].size == fileList[j].size:
                fileList[i].sameSizeFileList.append(j)