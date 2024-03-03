import socket
import picar_4wd as fc

HOST = "192.168.50.213" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

def handle(d, s):
    s = int(s)
    if d == "f":
        fc.stop()
        fc.forward(s)
    elif d == "l":
        fc.stop()
        fc.turn_left(s)
    elif d == "r":
        fc.stop()
        fc.turn_right(s)
    else:
        raise Exception("Invalid direction")
    return s

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while 1:
            client, clientInfo = s.accept()
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format
            if data != b"":
                print(data)
                i = data.decode('ascii')
                speed = handle(i[0], i[1:-2])
                temp = fc.cpu_temperature()
                pwr = fc.power_read()
                output = "CPU Temperature: " + str(temp) + "\nVoltage: " + str(pwr) + "\nCar Speed: " + str(speed)
                print("server recv from: ", clientInfo)
                print(data)     
                client.sendall(output.encode('ascii')) # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()    
