from thefuck.utils import for_app
from thefuck.specific.sudo import sudo_support


@sudo_support
@for_app('pip')
def match(command):
    return ('pip install' in command.script and 'Permission denied' in command.output)


def get_new_command(command):
    if '--user' not in command.script:  # add --user (attempt 1)
        return command.script.replace(' install ', ' install --user ')

    return f"sudo {command.script.replace(' --user', '')}"
