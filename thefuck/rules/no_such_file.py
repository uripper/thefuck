import re
from thefuck.shells import shell


patterns = (
    r"mv: cannot move '[^']*' to '([^']*)': No such file or directory",
    r"mv: cannot move '[^']*' to '([^']*)': Not a directory",
    r"cp: cannot create regular file '([^']*)': No such file or directory",
    r"cp: cannot create regular file '([^']*)': Not a directory",
)


def match(command):
    return any(re.search(pattern, command.output) for pattern in patterns)


def get_new_command(command):
    for pattern in patterns:
        if file := re.findall(pattern, command.output):
            file = file[0]
            dir = file[:file.rfind('/')]

            formatme = shell.and_('mkdir -p {}', '{}')
            return formatme.format(dir, command.script)
