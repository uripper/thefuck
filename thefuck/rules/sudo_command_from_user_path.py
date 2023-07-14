import re
from thefuck.utils import for_app, which, replace_argument


def _get_command_name(command):
    if found := re.findall(r'sudo: (.*): command not found', command.output):
        return found[0]


@for_app('sudo')
def match(command):
    if 'command not found' in command.output:
        command_name = _get_command_name(command)
        return which(command_name)


def get_new_command(command):
    command_name = _get_command_name(command)
    return replace_argument(
        command.script, command_name, f'env "PATH=$PATH" {command_name}'
    )
