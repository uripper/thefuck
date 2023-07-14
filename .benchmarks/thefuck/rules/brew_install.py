import re
from thefuck.utils import for_app
from thefuck.specific.brew import brew_available

enabled_by_default = brew_available


def _get_suggestions(str):
    return str.replace(" or ", ", ").split(", ")


@for_app('brew', at_least=2)
def match(command):
    return (
        'install' in command.script
        and 'No available formula' in command.output
        and 'Did you mean' in command.output
    )


def get_new_command(command):
    matcher = re.search('Warning: No available formula with the name "(?:[^"]+)". Did you mean (.+)\\?', command.output)
    suggestions = _get_suggestions(matcher[1])
    return [f"brew install {formula}" for formula in suggestions]
