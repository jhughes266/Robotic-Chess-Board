import socket
from console_debug_info import ConsoleDebugInfo
from secrets import HOST, PORT


class CommunicationManager:
    def __init__(self):
        pass

    def connectToPico(self):
        ConsoleDebugInfo.printToConsole("Connected to the Pico!")

    def sendDataToPico(self, data):
        ConsoleDebugInfo.printToConsole("Data sent to the Pico!")
        ConsoleDebugInfo.printToConsole(f"The Data is:\n {data}")

    def recieveDataFromPico(self):
        data = '1'
        ConsoleDebugInfo.printToConsole("Data received from Pico!")
        return data

    def disconnectFromPico(self):
        ConsoleDebugInfo.printToConsole("Disconnected from Pico!")

    def executeCommand(self, command, maxCommandSize):
        self.sendDataToPico(command)
        self.recieveDataFromPico()

class PicoCommunicationManager(CommunicationManager):
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectToPico(self):
        ConsoleDebugInfo.printToConsole("Attempting to connect to Pico!")
        self.__socket.connect((HOST, PORT))
        ConsoleDebugInfo.printToConsole("Connected to the Pico!")

    def executeCommand(self, command, maxCommandSize):
        subCommand = ''
        for char in command:
            subCommand += char
            if len(subCommand) > maxCommandSize and char == ']':
                self.sendDataToPico(subCommand)
                self.recieveDataFromPico()
                subCommand = ''
        # Send remaining data to pico
        self.sendDataToPico(subCommand)
        self.recieveDataFromPico()



    def sendDataToPico(self, data):
        self.__socket.send(data.encode('utf-8'))
        ConsoleDebugInfo.printToConsole("Data sent to the Pico!")
        ConsoleDebugInfo.printToConsole(f"The Data is:\n {data}")

    def recieveDataFromPico(self):
        incoming = self.__socket.recv(1024).decode('utf-8')
        ConsoleDebugInfo.printToConsole("Data received from Pico!")

    def disconnectFromPico(self):
        self.__socket.send("END".encode('utf-8'))
        self.__socket.close()
        ConsoleDebugInfo.printToConsole("Disconnected from Pico!")
