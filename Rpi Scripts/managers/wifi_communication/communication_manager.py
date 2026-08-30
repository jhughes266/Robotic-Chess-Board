import socket
from secrets import HOST, PORT


class CommunicationManager:
    def __init__(self):
        pass

    def connectToPico(self):
        print("Connected to the Pico!")

    def sendDataToPico(self, data):
        print("Data sent to the Pico!")
        print(f"The Data is:\n {data}")

    def recieveDataFromPico(self):
        data = '1'
        print("Data received from Pico!")
        return data

    def disconnectFromPico(self):
        print("Disconnected from Pico!")

    def sendCommandToPico(self, command, maxCommandSize):
        self.sendDataToPico(command)
        self.recieveDataFromPico()

class PicoCommunicationManager(CommunicationManager):
    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connectToPico(self):
        print("Attempting to connect to Pico!")
        self.__socket.connect((HOST, PORT))
        print("Connected to the Pico!")

    def sendCommandToPico(self, command, maxCommandSize):
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
        print("Data sent to the Pico!")
        print(f"The Data is:\n {data}")

    def recieveDataFromPico(self):
        incoming = self.__socket.recv(1024).decode('utf-8')
        print("Data received from Pico!")

    def disconnectFromPico(self):
        self.__socket.send("END".encode('utf-8'))
        self.__socket.close()
        print("Disconnected from Pico!")
