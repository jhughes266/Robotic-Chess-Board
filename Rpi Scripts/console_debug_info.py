
class ConsoleDebugInfo:
    __enableConsoleOutput = True

    @classmethod
    def consoleOutputEnabled(cls, enable):
        cls.__enableConsoleOutput = enable

    @classmethod
    def printToConsole(cls, msg):
        if cls.__enableConsoleOutput:
            print(msg)

