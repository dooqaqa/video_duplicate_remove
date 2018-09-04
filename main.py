import os, name_parser, gui
import subprocess
#subprocess.Popen(r'explorer /select, "F:\dev\projects\python\video_duplicate_remove\新建文本文档.txt"')
def setWinConsoleKey(key, value):
    """
    Set/Remove Run Key in windows registry.

    :param key: Run Key Name
    :param value: Program to Run
    :return: None
    """
    # This is for the system run variable
    reg_key = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r'Console',
        0, winreg.KEY_SET_VALUE)

    with reg_key:
        if value is None:
            winreg.DeleteValue(reg_key, key)
        else:
            if '%' in value:
                var_type = winreg.REG_EXPAND_SZ
            else:
                var_type = winreg.REG_SZ
            winreg.SetValueEx(reg_key, key, 0, var_type, value)

if os.name == 'nt':
    import winreg

class TimeLogger:
    def __init__(self):
        print('')


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
                    if (result):
                        printColorMessage(str(result.group(0)), 36)
                        total_num += 1
                        fileList.append([name, result.group(0), name_parser.getJAVTag(result.group(0)), os.path.getsize(full_name), full_name])
                        printColorMessage(str(total_num) + ':' + full_name, 32)
                    else:
                        failed_num += 1
                        fileList.append([name, '', '', os.path.getsize(full_name), full_name])
                        printColorMessage(str(failed_num) + full_name, 31)
            '''for name in dirs:
                print(os.path.join(root, name))'''



if __name__ == '__main__':
    if os.name == 'nt':
        setWinConsoleKey('VirtualTerminalLevel', '1')
    getFileList(['F:\\sn'])
    # if os.name == 'nt':
    #     setWinConsoleKey('VirtualTerminalLevel', None)