import sys
import json
import argparse

from .cli import CLI

class CLITool:
    def __init__(self, description=None):
        self.cli = CLI()

        class DynamicObject():
            pass

        self.credentials = DynamicObject()

        # Parse out Host for backend and login credentials when connecting
        parser = argparse.ArgumentParser(description = description)
        parser.add_argument("commands", nargs="*", help="Execute each command specified in order.  Use quotes (\") to seperate commands", 
                type=str)

        self.args = parser.parse_args()

        self.register_command(lambda : quit(), name='q', description="Exit the program")

    def register_command(self, function, name=None, description=None):
        self.cli.register_command(function, name=name, description=description)

    def unregister_command(self, name):
        self.cli.unregister_command(name)

    def run(self):
        self.cli.run(commands=self.args.commands)
        pass


