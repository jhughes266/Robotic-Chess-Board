
class BasicCommunicationManager:
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

class PicoCommunicationManager(BasicCommunicationManager):
    pass
