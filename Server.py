import socket, asyncio, time
from bleak import BleakClient
from bleak import BleakScanner
from bleak import BleakError
address = ""
uuid = ""

def Connect():
    global s
    global conn
    HOST = ''
    PORT = 8080
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ('Socket created')
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print ('Socket now listening')

    conn, addr = s.accept()
    print ('Connected to: ' + addr[0] + ':' + str(addr[1]))


async def scan():
    global address

    devices = await BleakScanner.discover()
    i = 1
    available = []

    for d in devices:
        if d.metadata.get("uuids") != []:
            available.append(d)
            print(str(i) + ") " + str(d))
            print(" ")
            i = i + 1

    
    choice = input("Please Enter The Number of the Bluetooth Device you want to connect to: ")
    choice = int(choice) - 1

    address = available[choice].address

    print("Establishing Connection to " + str(available[choice].name))


async def changeColour(red, green, blue):
    global client

    hRed = hex(int(red)).split('x')[-1]
    if len(hRed) == 1: hRed = "0" + hRed

    hGreen = hex(int(green)).split('x')[-1]
    if len(hGreen) == 1: hGreen = "0" + hGreen

    hBlue = hex(int(blue)).split('x')[-1]
    if len(hBlue) == 1: hBlue = "0" + hBlue

    code = str("03" + hRed + hGreen + hBlue)
    bcode = bytearray.fromhex(code)
    print(uuid + " : " + str(bcode))

    await client.write_gatt_char(str(uuid), bcode)



async def changeState():
    global client
    power = "\04"
    b = power.encode('utf-8')
    await client.write_gatt_char(uuid, b)
        

async def main():
    global uuid
    global client
    connected = False
    i = 0

    



    while True:
        try:
            if connected == False:
                data = conn.recv(255)
                data = str(data)[2:-5]
                print (data)
                Connection = await scan()

            try:
                async with BleakClient(address) as client:
                    connected = True
                    conn.send(b"Connected\r\n")
                    
                    services = await client.get_services()
                    for i in services:
                        for k in i.characteristics:
                            uuid = str(k)[0:-14]
                            
                    while connected == True:
                        data = conn.recv(255)
                        data = str(data)[2:-5]
                        print (data)

                        if data.split(",")[0] == "changeColour":
                            await changeColour(data.split(",")[1],data.split(",")[2],data.split(",")[3])
                            conn.send(b"Changed\r\n")
                
            except BleakError:
                print("Connection Failed\nTrying Again")


        except (ConnectionResetError,NameError):
            Connect()
            if connected == True:
                connected = False
                await client.disconnect()
asyncio.run(main())



