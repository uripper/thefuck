import re
from subprocess import Popen, PIPE
from thefuck.utils import memoize, which
from thefuck.shells import shell

enabled_by_default = bool(which('lsof'))

patterns = [r"bind on address \('.*', (?P<port>\d+)\)",
            r'Unable to bind [^ ]*:(?P<port>\d+)',
            r"can't listen on port (?P<port>\d+)",
            r'listen EADDRINUSE [^ ]*:(?P<port>\d+)']


@memoize
def _get_pid_by_port(port):
    proc = Popen(['lsof', '-i', f':{port}'], stdout=PIPE)
    lines = proc.stdout.read().decode().split('\n')
    return lines[1].split()[1] if len(lines) > 1 else None


@memoize
def _get_used_port(command):
    for pattern in patterns:
        if matched := re.search(pattern, command.output):
            return matched['port']


def match(command):
    port = _get_used_port(command)
    return port and _get_pid_by_port(port)


def get_new_command(command):
    port = _get_used_port(command)
    pid = _get_pid_by_port(port)
    return shell.and_(f'kill {pid}', command.script)
