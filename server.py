import socket
import time
from threading import Thread

# server's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5002 # port we want to use
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize list/set of all connected client's sockets
client_sockets = set()
# create a TCP socket
s = socket.socket()
# make the port as reusable port
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the socket to the address we specified
s.bind((SERVER_HOST, SERVER_PORT))
# listen for upcoming connections
s.listen(5)
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")
msg_list = []



def listen_for_client(cs):
    player1_counter = 0
    player2_counter = 0
    """
    This function keep listening for a message from `cs` socket
    Whenever a message is received, broadcast it to all other connected clients
    """
    while True:
        try:
            # keep listening for a message from `cs` socket
            msg = cs.recv(1024).decode()
        except Exception as e:
            # client no longer connected
            # remove it from the set
            print(f"[!] Error: {e}")
            client_sockets.remove(cs)
        else:
            # if we received a message, replace the <SEP> 
            # token with ": " for nice printing
            msg = msg.replace(separator_token, ": ")
            # checks if any element is present in the list
            if len(msg_list) == 2:
                del msg_list[:2]
            msg_list.append(msg)
            print("msglist: ", msg_list)

        # iterate over all connected sockets
        for client_socket in client_sockets:
            # and send the message
            client_socket.send(msg.encode())

        # trying to split the list into dictionary to know which player wins 
        if len(msg_list) == 2:
            name_list, value_list = zip(*(s.split(": ") for s in msg_list))
            players_dict = dict(zip(name_list,value_list))
            player_values = []
            for k,v in players_dict.items():
                player_values.append(players_dict[k])
            print(player_values)    # ['R\x1b[39m', 'S\x1b[39m']

            slicing = slice(1)
            for i in range(len(player_values)):
                val = player_values[i]
                player_values[i] = val[slicing]
            print(player_values) # ['R', 'S']
            
            for i in range(len(player_values)-1):
                if ((player_values[i] == "R") and (player_values[i+1] == "S")) or ((player_values[i] == "S") and (player_values[i+1] == "P")) or ((player_values[i] == "P") and (player_values[i+1] == "R")):
                    msg = b"PLAYER 1 receives 1 point.\nPLAYER 2 receives no points.\n\nPLAYER 1's turn"
                    # shows the message in both client sides
                    player1_counter += 1
                    for client_socket in client_sockets:
                        client_socket.send(msg)
                
                elif ((player_values[i] == "S") and (player_values[i+1] == "R")) or ((player_values[i] == "P") and (player_values[i+1] == "S")) or ((player_values[i] == "R") and (player_values[i+1] == "P")):
                    msg = b"PLAYER 1 receives no points.\nPLAYER 2 receives 1 point.\n\nPLAYER 1's turn"
                    player2_counter += 1
                    # shows the message in both client sides
                    for client_socket in client_sockets:
                        client_socket.send(msg)

                elif ((player_values[i] == "S") and (player_values[i+1] == "S")) or ((player_values[i] == "P") and (player_values[i+1] == "P")) or ((player_values[i] == "R") and (player_values[i+1] == "R")):
                    msg = b"Both players receive 0.5 points.\n\nPLAYER 1's turn"
                    player1_counter += 0.5
                    player2_counter += 0.5
                    # shows the message in both client sides
                    for client_socket in client_sockets:
                        client_socket.send(msg)
            
            # checks the score of each player
            if (player1_counter >= 3):
                msg = b"PLAYER 1 WINS!"
                for client_socket in client_sockets:
                        client_socket.send(msg)
            elif (player2_counter >= 3):
                msg = b"PLAYER 2 WINS!"
                for client_socket in client_sockets:
                        client_socket.send(msg)


while True:
    # we keep listening for new connections all the time
    client_socket, client_address = s.accept()
    print(f"[+] {client_address} connected.")
    # add the new connected client to connected sockets
    client_sockets.add(client_socket)
    # finds the length of the set client_socket
    set_length = len(client_sockets)
    if set_length < 2:
        msg = b"You are PLAYER 1.\nPlease wait for the next player to join."
        client_socket.send(msg)
        # wait for the second player to connect
        time.sleep(10)
    elif set_length == 2:
        msg = b"You are PLAYER 2.\n"     
        client_socket.send(msg)
        msg = b"**Two players connected**\n\nPlayers must type one one of the input keys [R], [P], [S].\n"
        # shows the message in both client sides
        for cs in client_sockets:
            cs.send(msg)
    else:
        msg = b"INVALID. THERE SHOULD ONLY BE TWO PLAYERS."
        client_socket.send(msg)
        client_socket.close()

    # start a new thread that listens for each client's messages
    t = Thread(target=listen_for_client, args=(client_socket,))
    # make the thread daemon so it ends whenever the main thread ends
    t.daemon = True
    # start the thread
    t.start()


# close client sockets
for cs in client_sockets:
    cs.close()
# close server socket
s.close()



