import os, name_parser, gui, sys
if os.name == 'nt':
    if sys.version_info < (3, 0):
        import _winreg as winreg
    else:
        import winreg
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


class TimeLogger:
    def __init__(self):
        print('')


if __name__ == '__main__':
    if os.name == 'nt':
        setWinConsoleKey('VirtualTerminalLevel', '1')
    ui = gui.UI()
    ui.initWidgets()
    ui.run()
    #getFileList(['F:\\sn'])
    # if os.name == 'nt':
    #     setWinConsoleKey('VirtualTerminalLevel', None)