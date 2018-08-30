import os, name_parser
def set_run_key(key, value):
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
    for path in pathList:
        for root, dirs, files in os.walk(path, followlinks=True):
            for name in files:
                if name_parser.isVedio(name):
                    if (name_parser.parse(name)):
                        total_num += 1
                        printColorMessage(str(total_num) + ':' + os.path.join(root, name), 32)
                    else:
                        failed_num += 1
                        printColorMessage(str(failed_num) + os.path.join(root, name), 31)
            '''for name in dirs:
                print(os.path.join(root, name))'''



if __name__ == '__main__':
    if os.name == 'nt':
        set_run_key('VirtualTerminalLevel', '1')
    getFileList(['F:\\sn'])
    # if os.name == 'nt':
    #     set_run_key('VirtualTerminalLevel', None)