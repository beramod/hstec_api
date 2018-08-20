import atexit
import os
import sys
import time
from signal import SIGTERM


# --------------------------------------------------------------------------------------------------
class Daemon(object):
    """
    A generic daemon class.
    Usage: subclass the Daemon class and override the run() method
    """

    def __init__(self, pidPath, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidPath = pidPath

    def _set_redirects(self):
        # redirect standard file descriptors
        if self.stdin is not None:
            si = open(self.stdin, 'r')
            os.dup2(si.fileno(), sys.stdin.fileno())
        if self.stdout is not None and self.stdout != 'stdout':
            sys.stdout.flush()
            so = open(self.stdout, 'a+')
            os.dup2(so.fileno(), sys.stdout.fileno())
        if self.stderr is not None and self.stderr != 'stderr':
            sys.stderr.flush()
            se = open(self.stderr, 'a+')
            os.dup2(se.fileno(), sys.stderr.fileno())

    def daemonize(self):
        """
        do the UNIX double-fork magic, see Stevens' "Advanced
        Programming in the UNIX Environment" for details (ISBN 0201563177)
        http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
        """
        try:
            pid = os.fork()
            if pid > 0:
                # exit first parent
                sys.exit(0)
        except OSError as ex:
            sys.stderr.write("fork #1 failed: %d (%s)\n" % (ex.errno, ex.strerror))
            sys.exit(1)

        # decouple from parent environment
        os.chdir("/")
        os.setsid()
        os.umask(0)

        # do second fork
        try:
            pid = os.fork()
            if pid > 0:
                # exit from second parent
                sys.exit(0)
        except OSError as ex:
            sys.stderr.write("fork #2 failed: %d (%s)\n" % (ex.errno, ex.strerror))
            sys.exit(1)

        self._set_redirects()

        # write pidPath
        atexit.register(self.delete_pid)
        if self.pidPath:
            pid = str(os.getpid())
            open(self.pidPath, 'w+').write("%s\n" % pid)

    def delete_pid(self):
        if self.pidPath and os.path.exists(self.pidPath):
            os.remove(self.pidPath)

    def start(self):
        """
        Start the daemon
        """
        # Check for a pidPath to see if the daemon already runs
        try:
            pf = open(self.pidPath, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except Exception:
            pid = None

        if pid:
            try:
                os.kill(pid, 0)
                message = "pid='%s' already exist. Daemon already running?\n"
                sys.stderr.write(message % pid)
                sys.exit(1)
            except Exception:
                self.delete_pid()
                pass

        # Start the daemon
        self.daemonize()
        self.run()

    def stop(self):
        """
        Stop the daemon
        """
        # Get the pid from the pidPath
        try:
            pf = open(self.pidPath, 'r')
            pid = int(pf.read().strip())
            pf.close()
        except IOError:
            pid = None

        if not pid:
            message = "pidPath %s does not exist. Daemon not running?\n"
            sys.stderr.write(message % self.pidPath)
            return  # not an error in a restart

        # Try killing the daemon process
        try:
            while 1:
                os.kill(pid, SIGTERM)
                time.sleep(0.1)
        except OSError as ex:
            err = str(ex)
            if err.find("No such process") > 0:
                if os.path.exists(self.pidPath):
                    os.remove(self.pidPath)
            else:
                print(err)
                sys.exit(1)

    def restart(self):
        """
        Restart the daemon
        """
        self.stop()
        self.start()

    def run(self):
        """
        You should override this method when you subclass Daemon. It will be called after the process has been
        daemonized by start() or restart().
        """