from thefuck.shells import shell
from thefuck.utils import for_app


@for_app('vagrant')
def match(command):
    return 'run `vagrant up`' in command.output.lower()


def get_new_command(command):
    cmds = command.script_parts
    machine = cmds[2] if len(cmds) >= 3 else None
    start_all_instances = shell.and_(u"vagrant up", command.script)
    if machine is None:
        return start_all_instances
    else:
        return [
            shell.and_(f"vagrant up {machine}", command.script),
            start_all_instances,
        ]
