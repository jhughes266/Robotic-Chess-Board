import network
import usocket as socket
import time
from secrets import SSID, PASSWORD, STATIC_IP, SUBNET, GATEWAY, DNS, PORT
# This import calls a config script which inits all the objects responsible for
# moving the robotic assembly and then provides us with PieceMover object stored
# in the pieceMover variable.
from robot_object_config import pieceMover
from command_executer import excuteCommand

pieceMover.disengageGripper()
# Turn on the wifi on the picos chip
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Force the pico to have the preset network settings
wlan.ifconfig((STATIC_IP, SUBNET, GATEWAY, DNS))

# Trying to connect to the WIFI
wlan.connect(SSID, PASSWORD)

# Store chars for printing loading wheel
loadingWheelList = ["|", "/", "-", "\\"]
# Waiting until a connection has been made
while wlan.isconnected() == False:
    for symbol in loadingWheelList:
        print(f"Connecting to Wi-Fi: {symbol}", end="\r")
        time.sleep(0.125)

# The Connection has been established
print(f"Connected to Wi-Fi. The Pico W's IP adress is: {wlan.ifconfig()[0]}")

# Make a TCP socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Force the PICO to open the port and bypass cooldown
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Allow any device on the right port to connect
serverSocket.bind(("0.0.0.0", PORT))
# Listen for incoming connections
serverSocket.listen(1)
print("The server is listening for incoming connections.")

# Getting a connection to the client
connection, address = serverSocket.accept()
print(f"A device with the IP address {address} has connected to the pico!")

# This is the main program loop the pico will sit here waiting for commands and
# and communicate back to the client.
while True:
   
    try:
        # Get the command from the client
        clientCommand = connection.recv(4096)
        # If there is no data restart the loop
        if not clientCommand:
            continue
        # decode the client command
        decodedClientCommand = clientCommand.decode("utf-8")
        if decodedClientCommand == "END":
            break
    
        excuteCommand(decodedClientCommand, pieceMover)
        print("command executed!")
        
        connection.sendall("1")
        print("confirmation sent")    
    
    # Handle any exceptions
    except Exception as e:
        print(f"Exception {e} occured!")
        break

connection.close()
print("Finished")
    



