import os
import sys
import subprocess

from src.core.daemon import Daemon


# ===================================================================================================
# ManageDaemon
# ===================================================================================================
class ManageDaemon(Daemon):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    PID_PATH = os.path.join(BASE_DIR, "var/pid/hstec.pid")
    LOG_PATH = os.path.join(BASE_DIR, "var/logs/hstec.log")

    def __init__(self):
        subprocess.call('mkdir -p ' + os.path.join(self.BASE_DIR, "var/logs"), shell=True)
        super().__init__(self.PID_PATH, stdout=self.LOG_PATH, stderr=self.LOG_PATH)

    def run(self):
        # rewrite pid
        with open(self.PID_PATH, 'w') as pidFile:
            pidFile.write("{}".format(os.getpid()))
        # run django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "src.core.settings")
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)


# __main__ -----------------------------------------------------------------------------------------
if __name__ == "__main__":
    background = False
    for arg in sys.argv:
        if arg == 'background':
            background = True
            sys.argv.remove('background')
            break

    if background:
        ManageDaemon().start()
    else:
        ManageDaemon().run()