import re, os
smallFileSize = 1024 * 1024 * 10

formatList = ['avi', 'rmvb', 'rm', 'mp4', 'mkv', 'wmv', 'mov', 'vob', 'wm']
detectedJAVTags = set(['snis', 'ssni', 'ipx', 'fc2', 'yrh', 'shkd', 'ppv', 'Tokyo-Hot', 'juc', 'abs'])
falseJAVTags = set(['vl', 'vip', 'japan', 'dv', 'hd'])
nonJAVTags = set(['pornhub'])

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

def parseJAV(name):
    for f in formatList:
        if '.' + f in name:
            name = name.replace('.' + f, '')
    for t in nonJAVTags:
        if t in name.lower():
            return []
    ret = []
    candidats = findall('[A-Za-z]{2,5}[^A-Za-z0-9]{0,2}\d{3,6}(?!\d|.com|.cc|.net)', name)
    for c in candidats:
        if len(c) <= 0:
            continue
        hit = False
        for t in falseJAVTags:
            if t in c.lower():
                hit = True
                break
        if not hit:
            ret.append(c)
    return ret

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
    if len(m) == 1 and not m[0] in falseJAVTags:
        detectedJAVTags.add(m[0])
    else:
        for tag in m:
            if tag.lower() in detectedJAVTags:
                return tag
    for tag in m:
        if tag.lower() not in falseJAVTags:
            return tag
    return ''

def getJAVSerialNumber(name, tag):
    #m = match('\d{1,}', name[name.find(tag):])
    m = re.search('\d+', name[name.find(tag):])
    if m:
        return m.group(0)
    return ''


def couldBeAdvertisement(fullPath, name, fileList):
    return os.path.getsize(fullPath) < smallFileSize or name in fileList