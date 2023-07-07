import inspect
import traceback
import json
import re
import readline

class CLI:

    def __init__(self):
        self._command_map = {}
        self.register_command(self._command_help, "help", "Display usage instructions of CLI")
        pass

    def register_command(self, function, name=None, description=None):

        if not callable(function):
            raise TypeError(f"Specified command {function} is not a callable function")

        if not name:
            name = function.__name__

        name = name.lower()

        if name in self._command_map:
            raise ValueError(f"Command with name {name} is already registered!")

        self._command_map[name] = {
            'function' : function,
            'args' : inspect.getargspec(function),
            'description' : description
        }

    def unregister_command(self, name):
        name = name.lower()

        if name in self._command_map:
            del self._command_map[name]

    def run(self, commands = None):
        # If commands are given, execute those commands and return out
        if commands and isinstance(commands, list):
            for command_str in commands:
                (command, params) = self._split_command_str(command_str)
                output = self._process_command(command, params)

                if isinstance(output, dict):
                    print(json.dumps(output, indent=4, sort_keys = True))
                elif output:
                    print(output)
        else:
            # No commands specified, start CLI loop
            print(">>> 'help' to see list of commands")
            while(True):
                try:
                    # Read and parse user input into a command with parameters
                    (command, params) = self._split_command_str(input("$: "))

                    # Attempt to process the user's command
                    output = self._process_command(command, params)

                    if isinstance(output, dict):
                        print(json.dumps(output, indent=4, sort_keys = True))
                    elif output:
                        print(output)

                except KeyboardInterrupt:
                    print()
                    continue
                except EOFError:
                    break

            print("")

    def _command_ls(self):
        print("\tRequests:")
        for command, info in self._command_map.items():
            args = info["args"].args
            print("\t\t{} ({})".format(command, ', '.join(args)))

    def _command_help(self):
        print("\tCMD PARAM1=VALUE PARAM2=VALUE ...\t: Execute the specified command with the given parameters")
        print("\t<ctrl>+c\t\t\t\t: Clear line")
        print("\t<ctrl>+d\t\t\t\t: Quit")

        # Print all command
        print()
        print("Registered Commands:")
        for command, info in self._command_map.items():
            args = info["args"].args
            desc = info["description"]

            # Filter out class arg when displaying help
            args = list(filter(lambda x: x != 'self', args))

            print("\t{} {}".format(command, "({})".format(', '.join(args)) if len(args) > 0 else ""))
            if desc:
                print("\t{}".format(desc))
                print()

    def _process_command(self, command, params):
        try:
            cmd = self._command_map[command]
            result = cmd["function"](**params)

            return result
        except TypeError as param_error:
            print("\t{}".format(param_error))

        # Invalid command or request specified
        except KeyError:
            print("Invalid command [{}]. Type 'help' for list of commands".format(command))

        # Unhandled exception triggered within the command itself
        except Exception as e:
            error = "Uncaught Exception:\n({}) {}\n".format(type(e), e)
            error = "{}\n{}".format(error, traceback.format_exc())
            return error

    def _split_command_str(self, user_input):
        user_input = user_input.strip().split(' ')
        command = user_input[0].lower()
        params = {k:v.strip('"') for k,v in re.findall(r'(\S+)=(".*?"|\S+)', ' '.join(user_input[1:]))}
        for key,value in params.items():
            if value.lower() == 'true':
                params[key] = True
            elif value.lower() == 'false':
                params[key] = False

        return command, params
