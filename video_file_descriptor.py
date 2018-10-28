#!/usr/bin/python
import name_parser

class VideoFileDescriptor:
    def __init__(self, name, fullPath, JAVTag, size):
        self.name = name
        self.fullPath = fullPath
        self.JAVTag = JAVTag
        self.size = size
        self.JAVNum = ''
        self.similarFileList = [] # don't know why this can't be put out side this func, will cause it turn to global member
        self.innocentSimilarFileList = []

    def analyzeJAVTag(self, force = False):
        oldTag = self.JAVTag
        if name_parser.isVOB(self.name):
            self.JAVTag = name_parser.getJAVTag(self.fullPath, force)
            self.JAVNum = name_parser.getJAVSerialNumber(self.fullPath, self.JAVTag)
        else:
            self.JAVTag = name_parser.getJAVTag(self.name, force)
            self.JAVNum = name_parser.getJAVSerialNumber(self.name, self.JAVTag)
        return self.JAVTag != oldTag

    def readableSizeStr(self):
        if self.size < 1024:
            return '' + self.size + 'Bytes'
        if self.size >= 1024 and self.size < 1048576:
            return '' + str(round(self.size / 1024, 2)) + 'KB'
        elif self.size >= 1048576 and self.size < 1073741824:
            return '' + str(round(self.size / 1048576, 2)) + 'MB'
        elif self.size > 1073741824:
            return '' + str(round(self.size / 1073741824, 2)) + 'GB'

    def initInnocentList(self):
        self.innocentSimilarFileList = [False] * len(self.similarFileList)
        #if (len(self.similarFileList)) > 0:
        #    print('_______ initInnocentList  ' + self.name + ' ' + str(len(self.innocentSimilarFileList)))
    
    def innocentNum(self):
        ret = 0
        if self.innocentSimilarFileList:
            for i in self.innocentSimilarFileList:
                if i == True:
                    ret += 1
        return ret

