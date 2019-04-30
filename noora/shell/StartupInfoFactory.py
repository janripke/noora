import os
import subprocess


class StartupInfoFactory(object):
    """Factory for creating startup info instances"""
    @staticmethod
    def new_startup_info():
        startup_info = None
        if os.name == 'nt':
            startup_info = subprocess.STARTUPINFO()
            # USESHOWWINDOW
            startup_info.dwFlags |= 1
            # SW_HIDE
            startup_info.wShowWindow = 0
        return startup_info
