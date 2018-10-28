import re, os
smallFileSize = 1024 * 1024 * 10

formatList = ['avi', 'rmvb', 'rm', 'mp4', 'mkv', 'wmv', 'mov', 'vob', 'wm']
detectedJAVTags = set(['snis', 'ssni', 'ipx', 'fc2', 'yrh', 'shkd', 'ppv', 'Tokyo-Hot', 'juc', 'abs', 'svdvd', 'ekdv', 'ipz'])
falseJAVTags = set(['vl', 'vip', 'japan', 'dv', 'hd', 'com', 'net', 'cc'])
nonJAVTags = set(['pornhub'])
checkPointList = []

def isVedio(name):
    for f in formatList:
        if match('.*.' + f + '$', name):
            return True
    return False

def isVOB(name):
    if match('.*vob$', name.lower()):
        return True
    return False

def match(expression, name):
    return re.match(r'' + expression, name, flags=re.IGNORECASE)

def search(expression, name):
    return re.search(r'' + expression, name, flags=re.IGNORECASE)

def findall(expression, name):
    return re.findall(r'' + expression, name, flags=re.IGNORECASE)

def removeFormat(name):
    for f in formatList:
        if '.' + f in name:
            name = name.replace('.' + f, '')
    return name

def checkNonJAV(name):
    for t in nonJAVTags:
        if t in name.lower():
            return True

def matchDetectedJAVTag(name):
    for t in detectedJAVTags:
        if t in name:
            return t
        elif t.upper() in name:
            return t.upper()
    return ''

def checkFalseJAVTag(name):
    return name.lower() in falseJAVTags

def getJAVTag(name, force = False):
    if checkNonJAV(name):
        return ''
    name = removeFormat(name)
    candidats = findall('[A-Za-z]{2,5}[^A-Za-z0-9]{0,2}\d{3,6}(?!\d|.com|.cc|.net)', name)
    for c in candidats:
        m = search('[A-Za-z]{2,5}', c)
        if not m :
            continue
        tag = m.group()
        if checkFalseJAVTag(tag):
            continue
        if '' != matchDetectedJAVTag(tag):
            return tag
        if len(candidats) == 1 and not checkFalseJAVTag(tag):
            detectedJAVTags.add(tag.lower())
            return tag
        if force:
            return tag
    return ''

def getJAVTagDeprecated(name, force = False):
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
    if len(m) == 1 and not m[0] in falseJAVTags:
        detectedJAVTags.add(m[0])
    else:
        for tag in m:
            if tag.lower() in detectedJAVTags:
                return tag
    if force:
        for tag in m:
            if tag.lower() not in falseJAVTags:
                return tag
    return ''

def getJAVSerialNumber(name, tag):
    if name != '' and tag != '':
        #m = match('\d{1,}', name[name.find(tag):])
        m = re.search('\d+', name[name.find(tag):])
        if m:
            return m.group(0)
    return ''

def couldBeAdvertisement(fullPath, name, fileList):
    return os.path.getsize(fullPath) < smallFileSize or name in fileList

def siblingVOB(file1, file2):
    return isVOB(file1.name) and isVOB(file2.name) and (file1.fullPath[:-5] == file2.fullPath[:-5])

def duplicatedJAV(file1, file2):
    return file1.JAVTag != '' and file1.JAVTag == file2.JAVTag and file1.JAVNum == file2.JAVNum

def duplicatedFile(file1, file2):
    return not isVOB(file1.name) and not isVOB(file2.name) and file1.size == file2.size

def initCheckPointList():
    checkPointList.append(duplicatedJAV)
    checkPointList.append(duplicatedFile)

def isDuplicated(file1, file2):
    for p in checkPointList:
        if p(file1, file2):
            return True
    return False
