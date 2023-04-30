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
privateKey = 3

# initialize TCP socket
with socket.socket() as s:
    # connect to the server
    s.connect((SERVER_HOST, SERVER_PORT))
    connectionSuccesful = True
    print("[+] Connected.")

    time.sleep(5)

    # calculating Bob's public value
    publicValue = (g**privateKey) % p

    # sending Bob's public value to Alice
    s.send(publicValue.to_bytes(2, 'big'))

    # receving Alice's public key
    alicePublicValue = s.recv(1024)
    publicKey = int.from_bytes(alicePublicValue, 'big')
    print(f' ')
    print(f'***New message from Alice***')
    print(f'- My key is {publicKey}')

    # for nice printing purposes
    print(f' ')
    print(f'...Calculating secret key...')
    print(f' ')

    # calculating the secret key
    secretKey = (publicKey**privateKey) % p
    print(f'Your shared secret key with Alice is {secretKey}')