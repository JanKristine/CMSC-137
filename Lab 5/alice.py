import socket
import time

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 5002 # server's port

print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")

p = 23
g = 9
privateKey = 4

# initialize TCP socket
with socket.socket() as s:
    # connect to the server
    s.connect((SERVER_HOST, SERVER_PORT))
    connectionSuccesful = True
    print("[+] Connected.")

    time.sleep(5)
    
    # calculating Alice's public value
    publicValue = (g**privateKey) % p

    # sending Alice's public value to Bob
    s.send(publicValue.to_bytes(2, 'big'))

    # receving Bob's public key
    bobPublicValue = s.recv(1024)
    publicKey = int.from_bytes(bobPublicValue, 'big')
    print(f' ')
    print(f'***New message from Bob***')
    print(f'- My key is {publicKey}')

    # for nice printing purposes
    print(f' ')
    print(f'...Calculating secret key...')
    print(f' ')

    # calculating the secret key
    secretKey = (publicKey**privateKey) % p
    print(f'Your shared secret key with Bob is {secretKey}')