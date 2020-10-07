import socket
import select

HEADER_LENGTH = 10

# Declare IP and port number
IP = "127.0.0.1"
PORT = 1234
rating = 0
high_risk_counter = 0
male_counter = 0
female_counter = 0
other_counter = 0
age25 = 0
age60 = 0
age100 = 0

message_age = ''
message_ph = ''
message_gen = ''
message_uhc = ''
message_loc = ''
message_cov = ''
message_smoker = ''
message_cough = ''
message_fever = ''
message_fatigue = ''
message_breath = ''
msg_age = ''
msg_ph = ''
msg_gen = ''
msg_uhc = ''
msg_loc = ''
msg_cov = ''
msg_smoker = ''
msg_cough = ''
msg_fever = ''
msg_fatigue = ''
msg_breath = ''

# Get server name and then encode in different variable for safe keeping, and also header of variable
Server_Name = input("Server Name: ")
ServerName = Server_Name.encode('utf-8')
ServerName_header = f"{len(ServerName):<{HEADER_LENGTH}}".encode('utf-8')

# Create a Server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP, PORT))
server_socket.listen()

sockets_list = [server_socket]  # List of sockets for select.select()
clients = {}  # List of connected clients - socket as a key, user header and name as data
user_details = {}  # list of all the user's details

print("listening on: ", (IP, PORT))


# Handles message receiving from a given client socket
def receive_message(sock):
    try:
        # Receive our "header" containing message length, it's size is defined and constant
        message_header = sock.recv(HEADER_LENGTH)
        # If received no data, client closed a connection, e.g using socket.close() or socket.shutdown(socket.SHUT_RDWR)
        if not len(message_header):
            return False

        # Convert header to int value
        message_length = int(message_header.decode('utf-8').strip())
        message = sock.recv(message_length)

        # Return an object of message header and message data
        return {'header': message_header, 'data': message}

    except:
        # if error with receiving message return false
        return False


# handles if quit message and initial reply
def handle_message(sock):
    global msg_age, msg_ph, msg_gen, msg_uhc, msg_loc, msg_cov, msg_smoker, msg_cough, msg_fever, msg_fatigue, msg_breath, rating
    msg_age = message_age["data"].decode("utf-8")
    if msg_age != "quit":
        msg_ph = message_ph["data"].decode("utf-8")
        msg_gen = message_gen["data"].decode("utf-8")
        msg_uhc = message_uhc["data"].decode("utf-8")
        msg_loc = message_loc["data"].decode("utf-8")
        msg_cov = message_cov["data"].decode("utf-8")
        msg_smoker = message_smoker["data"].decode("utf-8")
        msg_cough = message_cough["data"].decode("utf-8")
        msg_fever = message_fever["data"].decode("utf-8")
        msg_fatigue = message_fatigue["data"].decode("utf-8")
        msg_breath = message_breath["data"].decode("utf-8")
        # Get user by notified socket, so we will know who sent the message
        user_num = clients[sock]

        # Print out that we have received a message from this user
        print(f'Received message from User {user_num["data"].decode("utf-8")}: '
              f'{msg_age + msg_ph + msg_gen + msg_uhc + msg_loc + msg_cov + msg_smoker + msg_cough + msg_fever + msg_fatigue + msg_breath}')
        # Reply immediately to inform their message has been received
        init_response = "Your data has been received.\n"
        init_response = init_response.encode('utf-8')
        init_response_header = f"{len(init_response):<{HEADER_LENGTH}}".encode('utf-8')
        sock.send(ServerName_header + ServerName + init_response_header + init_response)

        # store the above data in the hashtable at their user_id
        temp_dict = {'Age': msg_age, 'Phone Num': msg_ph, 'Gender': msg_gen, 'UHC Status': msg_uhc, 'Location': msg_loc,
                     'Covid-19 Tested Positive': msg_cov, 'Smoker': msg_smoker, 'Cough Present': msg_cough,
                     'Fever Present': msg_fever, 'Fatigued': msg_fatigue, 'Shortness of breath': msg_breath}
        user_details[user_num["data"].decode("utf-8")] = temp_dict

        # Used arbitrary values for the purpose of the demo. Would consult HSE on true values
        if msg_uhc == 'Yes':
            rating = rating + 100
        if msg_smoker == 'Yes':
            rating = rating + 25
        if msg_cough == 'Yes':
            rating = rating + 50
        if msg_fever == 'Yes':
            rating = rating + 50
        if msg_fatigue == 'Yes':
            rating = rating + 25
        if msg_breath == 'Yes':
            rating = rating + 100

    else:
        print('\nClosed connection from User: {}'.format(clients[sock]['data'].decode('utf-8')))
        # Remove from list for socket.socket()
        sockets_list.remove(sock)
        # Remove from our list of users
        del clients[sock]


# Handle automated response
def automated_response(sock):
    global high_risk_counter
    # so based on their risk later, an appropriate message is sent
    if 100 <= rating < 200:
        response = "You are at high risk!\nWe will be in contact soon.\nPlease Self Isolate at home."
        response = response.encode('utf-8')
        response_header = f"{len(response):<{HEADER_LENGTH}}".encode('utf-8')
        sock.send(ServerName_header + ServerName + response_header + response)
        high_risk_counter = high_risk_counter + 1

    if rating >= 200:
        response = "You are at high risk!\nDo not interact with anyone\nContact a doctor immediately\n"
        response = response.encode('utf-8')
        response_header = f"{len(response):<{HEADER_LENGTH}}".encode('utf-8')
        sock.send(ServerName_header + ServerName + response_header + response)
        high_risk_counter = high_risk_counter + 1

    if 50 <= rating < 100:
        response = "You are at low risk!\nFollow HSE guidelines\nContact your the HSE helpline if" \
                   "\nsymptoms worsen"
        response = response.encode('utf-8')
        response_header = f"{len(response):<{HEADER_LENGTH}}".encode('utf-8')
        sock.send(ServerName_header + ServerName + response_header + response)

    if rating < 50:
        response = "You are at low risk\nFollow HSE prevention guidelines." \
                   "\nFollow government lock-down regulations"
        response = response.encode('utf-8')
        response_header = f"{len(response):<{HEADER_LENGTH}}".encode('utf-8')
        sock.send(ServerName_header + ServerName + response_header + response)

    else:
        response = "Follow government lock-down regulations\nDistance yourself from individuals with Covid-19." \
                   "\nFollow government lock-down regulations"
        response = response.encode('utf-8')
        response_header = f"{len(response):<{HEADER_LENGTH}}".encode('utf-8')
        sock.send(ServerName_header + ServerName + response_header + response)


# create statistics based on inputs
def stat_calc():
    global male_counter, female_counter, other_counter, age25, age60, age100
    if msg_gen == 'male':
        male_counter = male_counter + 1

    if msg_gen == 'female':
        female_counter = female_counter + 1

    if msg_gen == 'other':
        other_counter = other_counter + 1

    if int(msg_age) < int('25'):
        age25 = age25 + 1

    if int('25') < int(msg_age) <= int('60'):
        age60 = age60 + 1

    if int(msg_age) > int('60'):
        age100 = age100 + 1

    print("The following statistics are know through though the information inputted by app users")
    print("Gender   Males: {}   Females: {}     Other: {}\n".format(male_counter, female_counter, other_counter))
    print("Age Categories   Under 25s: {}   25-60: {}   Over 60: {}\n".format(age25, age60, age100))
    print("Number of people at high risk {}\n".format(high_risk_counter))


while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    # Iterate over notified sockets
    for notified_socket in read_sockets:
        # If notified socket is a server socket - new connection, accept it
        if notified_socket == server_socket:
            # Accept new connection
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user['data'].decode('utf-8') == 'quit':
                break

            # Add accepted socket to select.select() list
            sockets_list.append(client_socket)
            # Also save username and username header
            clients[client_socket] = user
            print(
                'Accepted new connection from {}:{}, UserID: {}'.format(*client_address, user['data'].decode('utf-8')))
            # Let the client know that a connection has been made
            greeting_msg = "Welcome, you are now connected"
            greeting_msg = greeting_msg.encode('utf-8')
            greeting_msg_header = f"{len(greeting_msg):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(ServerName_header + ServerName + greeting_msg_header + greeting_msg)
        else:
            # receive message, handle message and then respond to message
            message_age = receive_message(notified_socket)
            message_ph = receive_message(notified_socket)
            message_gen = receive_message(notified_socket)
            message_uhc = receive_message(notified_socket)
            message_loc = receive_message(notified_socket)
            message_cov = receive_message(notified_socket)
            message_smoker = receive_message(notified_socket)
            message_cough = receive_message(notified_socket)
            message_fever = receive_message(notified_socket)
            message_fatigue = receive_message(notified_socket)
            message_breath = receive_message(notified_socket)
            handle_message(notified_socket)
            automated_response(notified_socket)
            if msg_age != 'quit':
                print('\nAll Data for {} number of users'.format(len(user_details)))
                for x, y in user_details.items():
                    print(x, ":", y)

                stat_calc()
