#!/usr/bin/python
import name_parser

class VideoFileDescriptor:
    def __init__(self, name, fullPath, isJAV, JAVTag, size):
        self.name = name
        self.fullPath = fullPath
        self.isJAV = isJAV
        self.JAVTag = JAVTag
        self.size = size
        self.JAVNum = ''
        self.sameSizeFileList = [] # don't know why this can't be put out side this func, will cause it turn to global member

    def reAnalyzeJAVTag(self):
        self.JAVTag = name_parser.getJAVTag(self.name)
        self.JAVNum = name_parser.getJAVSerialNumber(self.name, self.JAVTag)

