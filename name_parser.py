import re

formatList = ['avi', 'rmvb', 'rm', 'mp4', 'mkv', 'wmv', 'mov', 'vob', 'wm']
def isVedio(name):
    for f in formatList:
        if match('.*.' + f + '$', name):
            return True
    return False

def match(expression, name):
    return re.match(r'' + expression, name)

def parse(name):
    return match('.*[A-Za-z]{3,5}(\W|_){0,2}\d{3,5}.*', name)
