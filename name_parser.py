import re, os
smallFileSize = 1024 * 1024 * 10

formatList = ['avi', 'rmvb', 'rm', 'mp4', 'mkv', 'wmv', 'mov', 'vob', 'wm']
detectedJAVTags = set(['snis', 'ssni', 'ipx', 'fc2', 'yrh', 'shkd', 'ppv'])

def isVedio(name):
    for f in formatList:
        if match('.*.' + f + '$', name):
            return True
    return False

def match(expression, name):
    return re.match(r'' + expression, name, flags=re.IGNORECASE)

def search(expression, name):
    return re.search(r'' + expression, name, flags=re.IGNORECASE)

def findall(expression, name):
    return re.findall(r'' + expression, name, flags=re.IGNORECASE)

def parseJAV(name):
    #return search('[A-Za-z]{3,5}(\W|_){0,2}\d{3,5}', name)
    return findall('[A-Za-z]{2,5}(\W|_){0,2}\d{3,6}(?!\d|.com)', name)

def getJAVTag(name):
    for f in formatList:
        if '.' + f in name:
            name = name.replace('.' + f, '')

    for t in detectedJAVTags:
        if t in name:
            return t
        elif t.upper() in name:
            return t.upper()

    #m = match('.*[A-Za-z]{3,5}.*', name)
    m = findall('[A-Za-z]{2,5}', name)
    if not m or len(m) == 0:
        return ''
    if len(m) == 1:
        detectedJAVTags.add(m[0])
    else:
        for tag in m:
            if tag.lower() in detectedJAVTags:
                return tag
    return m[0]

def getJAVSerialNumber(name, tag):
    #m = match('\d{1,}', name[name.find(tag):])
    m = re.search('\d+', name[name.find(tag):])
    if m:
        return m.group(0)
    return ''


def couldBeAdvertisement(fullPath, name, fileList):
    return os.path.getsize(fullPath) < smallFileSize or name in fileList