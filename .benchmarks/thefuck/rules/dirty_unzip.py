import contextlib
import os
import zipfile
from thefuck.utils import for_app
from thefuck.shells import shell


def _is_bad_zip(file):
    try:
        with zipfile.ZipFile(file, 'r') as archive:
            return len(archive.namelist()) > 1
    except Exception:
        return False


def _zip_file(command):
    # unzip works that way:
    # unzip [-flags] file[.zip] [file(s) ...] [-x file(s) ...]
    #                ^          ^ files to unzip from the archive
    #                archive to unzip
    for c in command.script_parts[1:]:
        if not c.startswith('-'):
            return c if c.endswith('.zip') else f'{c}.zip'


@for_app('unzip')
def match(command):
    if '-d' in command.script:
        return False

    return _is_bad_zip(zip_file) if (zip_file := _zip_file(command)) else False


def get_new_command(command):
    return f'{command.script} -d {shell.quote(_zip_file(command)[:-4])}'


def side_effect(old_cmd, command):
    with zipfile.ZipFile(_zip_file(old_cmd), 'r') as archive:
        for file in archive.namelist():
            if not os.path.abspath(file).startswith(os.getcwd()):
                # it's unsafe to overwrite files outside of the current directory
                continue

            with contextlib.suppress(OSError):
                os.remove(file)


requires_output = False
