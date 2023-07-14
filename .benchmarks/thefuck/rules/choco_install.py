from thefuck.utils import for_app, which


@for_app("choco", "cinst")
def match(command):
    return ((command.script.startswith('choco install') or 'cinst' in command.script_parts)
            and 'Installing the following packages' in command.output)


def get_new_command(command):
    return next(
        (
            command.script.replace(script_part, f"{script_part}.install")
            for script_part in command.script_parts
            if (
                script_part not in ["choco", "cinst", "install"]
                # Need exact match (bc chocolatey is a package)
                and not script_part.startswith('-')
                # Leading hyphens are parameters; some packages contain them though
                and '=' not in script_part
                and '/' not in script_part
                # These are certainly parameters
            )
        ),
        [],
    )


enabled_by_default = bool(which("choco")) or bool(which("cinst"))
