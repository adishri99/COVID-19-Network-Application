import socket
import errno
from tkinter import *
import time

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234
user_id = ''
user_id_header = ''

top = Tk()  # Create GUI
top.title("HSE Covid-19 Citizen App")


# Sourced externally from google search and code forums
class Checkbar(Frame):
    def __init__(self, parent=None, picks=[], side=LEFT, anchor=W):
        Frame.__init__(self, parent)
        self.vars = []
        for pick in picks:
            var = IntVar()
            chk = Checkbutton(self, text=pick, variable=var)
            chk.pack(side=side, anchor=anchor, expand=YES)
            self.vars.append(var)

    def state(self):
        return map((lambda var: var.get()), self.vars)


def receive_message(sock):
    try:
        # Receive our "header" containing server's name length, it's size is defined and constant
        server_header = sock.recv(HEADER_LENGTH)
        # If we received no data, server closed a connection,
        if not len(server_header):
            print('Connection closed by the server')
            sys.exit()

        # Convert header into int val
        servername_len = int(server_header.decode('utf-8').strip())
        # Receive and decode username
        servername = sock.recv(servername_len).decode('utf-8')
        # Now do the same for message
        message_header = sock.recv(HEADER_LENGTH)
        message_length = int(message_header.decode('utf-8').strip())
        msg = sock.recv(message_length).decode('utf-8')
        # print to the text box
        top.textBox_fb.delete('1.0', END)
        top.textBox_fb.insert(END, msg)
        # Print message to console
        print(f'{servername} > {msg}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()


def enter_user():
    global user_id, user_id_header
    user_id = top.textBox_user.get("1.0", "end-1c")
    if user_id != '':
        user_id = user_id.encode('utf-8')
        user_id_header = f"{len(user_id):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(user_id_header + user_id)
        time.sleep(1)
        receive_message(client_socket)
    else:
        error_msg = "Enter your PPS Number First"
        top.textBox_user.delete('1.0', END)
        top.textBox_user.insert(END, error_msg)


def commit_info():
    age = top.textBox_age.get("1.0", "end-1c")
    phone_no = top.textBox_ph.get("1.0", "end-1c")
    # uch = top.textBox_uch.get("1.0", "end-1c")
    if gen_male.get() == 1:
        gender = 'male'
    if gen_female.get() == 1:
        gender = 'female'
    if gen_other.get() == 1:
        gender = 'other'

    if uhc_status.get() == 1:
        uch = 'Yes'
    else:
        uch = 'No'
    if tested_pos.get() == 1:
        tested = 'Yes'
    else:
        tested = 'No'
    if smoker_var.get() == 1:
        smoker = 'Yes'
    else:
        smoker = 'No'
    if cough_var.get() == 1:
        cough = 'Yes'
    else:
        cough = 'No'
    if fever_var.get() == 1:
        fever = 'Yes'
    else:
        fever = 'No'
    if fatigue_var.get() == 1:
        fatigue = 'Yes'
    else:
        fatigue = 'No'
    if breathing_var.get() == 1:
        breathing_norm = 'Yes'
    else:
        breathing_norm = 'No'

    location = top.textBox_loc.get("1.0", "end-1c")

    if user_id != '':
        if age and phone_no and uch and gender and location != '':
            age = age.encode('utf-8')
            phone_no = phone_no.encode('utf-8')
            gender = gender.encode('utf-8')
            uch = uch.encode('utf-8')
            location = location.encode('utf-8')
            tested = tested.encode('utf-8')
            smoker = smoker.encode('utf-8')
            cough = cough.encode('utf-8')
            fever = fever.encode('utf-8')
            fatigue = fatigue.encode('utf-8')
            breathing_norm = breathing_norm.encode('utf-8')

            age_header = f"{len(age):<{HEADER_LENGTH}}".encode('utf-8')
            phone_no_header = f"{len(phone_no):<{HEADER_LENGTH}}".encode('utf-8')
            gender_header = f"{len(gender):<{HEADER_LENGTH}}".encode('utf-8')
            uch_header = f"{len(uch):<{HEADER_LENGTH}}".encode('utf-8')
            location_header = f"{len(location):<{HEADER_LENGTH}}".encode('utf-8')
            tested_header = f"{len(tested):<{HEADER_LENGTH}}".encode('utf-8')
            # feel_symp_header = f"{len(feel_symp):<{HEADER_LENGTH}}".encode('utf-8')
            smoker_header = f"{len(smoker):<{HEADER_LENGTH}}".encode('utf-8')
            cough_header = f"{len(cough):<{HEADER_LENGTH}}".encode('utf-8')
            fever_header = f"{len(fever):<{HEADER_LENGTH}}".encode('utf-8')
            fatigue_header = f"{len(fatigue):<{HEADER_LENGTH}}".encode('utf-8')
            breathing_norm_header = f"{len(breathing_norm):<{HEADER_LENGTH}}".encode('utf-8')

            client_socket.send(age_header + age)
            client_socket.send(phone_no_header + phone_no)
            client_socket.send(gender_header + gender)
            client_socket.send(uch_header + uch)
            client_socket.send(location_header + location)
            client_socket.send(tested_header + tested)
            # client_socket.send(feel_symp_header + feel_symp)
            client_socket.send(smoker_header + smoker)
            client_socket.send(cough_header + cough)
            client_socket.send(fever_header + fever)
            client_socket.send(fatigue_header + fatigue)
            client_socket.send(breathing_norm_header + breathing_norm)

            top.textBox_age.delete('1.0', END)
            top.textBox_ph.delete('1.0', END)
            top.textBox_uch.delete('1.0', END)
            top.textBox_gender.delete('1.0', END)
            top.textBox_loc.delete('1.0', END)
            top.textBox_covid.delete('1.0', END)
            top.textBox_symp.delete('1.0', END)

            time.sleep(0.2)
            # get the greeting message
            receive_message(client_socket)
            time.sleep(0.2)
            # get the automated response
            receive_message(client_socket)

        else:
            error_msg = "One or more fields  left blank\nPlease Fix"
            top.textBox_fb.delete('1.0', END)
            top.textBox_fb.insert(END, error_msg)

    else:
        error_msg = "Enter your PPS Number First"
        top.textBox_user.delete('1.0', END)
        top.textBox_user.insert(END, error_msg)


def quit_gui():
    msg = "quit"
    msg = msg.encode('utf-8')
    msg_header = f"{len(msg):<{HEADER_LENGTH}}".encode('utf-8')
    client_socket.send(msg_header + msg)
    print("console about to close")
    client_socket.close()
    time.sleep(3)
    sys.exit()


# Create a label to display info
# username
top.textBox_user = Text(top.master, height=2, width=20)
top.textBox_user.grid(row=0, column=1, columnspan=2, padx=2, pady=2)
top.LabelBox_user = Label(top.master, text="PPS Number: ")
top.LabelBox_user.grid(row=0, column=0)

# Age
top.textBox_age = Text(top.master, height=2, width=20)
top.textBox_age.grid(row=1, column=1, columnspan=2, padx=2, pady=2)
top.LabelBox_age = Label(top.master, text="Age: ")
top.LabelBox_age.grid(row=1, column=0)

# Phone Number
top.textBox_ph = Text(top.master, height=2, width=20)
top.textBox_ph.grid(row=2, column=1, columnspan=2, padx=2, pady=2)
top.LabelBox_ph = Label(top.master, text="Phone Number: ")
top.LabelBox_ph.grid(row=2, column=0)

# Gender
top.textBox_gender = Text(top.master, height=2, width=20)
# top.textBox_gender.grid(row=3, column=1, columnspan=2, padx=2, pady=2)
top.LabelBox_gender = Label(top.master, text="Gender:")
top.LabelBox_gender.grid(row=3, column=0)
gen_male = IntVar()
Checkbutton(top, text="Male", variable=gen_male).grid(row=3, column=2, columnspan=1, padx=2, pady=2)
gen_female = IntVar()
Checkbutton(top, text="Female", variable=gen_female).grid(row=3, column=3, columnspan=1, padx=2, pady=2)
gen_other = IntVar()
Checkbutton(top, text="Other", variable=gen_other).grid(row=3, column=4, columnspan=1, padx=2, pady=2)

# Underlying health conditions
top.textBox_uch = Text(top.master, height=2, width=20)
# top.textBox_uch.grid(row=4, column=1, columnspan=2, padx=2, pady=2)
top.LabelBox_uch = Label(top.master, text="Underlying Health Conditions: ")
top.LabelBox_uch.grid(row=4, column=0)
uhc_status = IntVar()
Checkbutton(top, text="Yes", variable=uhc_status).grid(row=4, column=2, columnspan=1, padx=2, pady=2)
Checkbar(top, ['No']).grid(row=4, column=3, columnspan=1, padx=2, pady=2)

# Location
top.textBox_loc = Text(top.master, height=2, width=20)
top.textBox_loc.grid(row=5, column=1, columnspan=2, padx=2, pady=2)
top.LabelBox_loc = Label(top.master, text="Location\n(County): ")
top.LabelBox_loc.grid(row=5, column=0)

# Covid Status
top.textBox_covid = Text(top.master, height=2, width=20)
# top.textBox_covid.grid(row=6, column=1, columnspan=2, padx=2, pady=2)
top.LabelBox_covid = Label(top.master, text="Have You Tested Positive for COVID-19: ")
top.LabelBox_covid.grid(row=6, column=0)
tested_pos = IntVar()
Checkbutton(top, text="Yes", variable=tested_pos).grid(row=6, column=2, columnspan=1, padx=2, pady=2)
Checkbar(top, ['No']).grid(row=6, column=3, columnspan=1, padx=2, pady=2)

# Smoker Status
top.textBox_smoker = Text(top.master, height=2, width=20)
top.LabelBox_covid = Label(top.master, text="Do You Smoke? ")
top.LabelBox_covid.grid(row=7, column=0)
smoker_var = IntVar()
Checkbutton(top, text="Yes", variable=smoker_var).grid(row=7, column=2, columnspan=1, padx=2, pady=2)
Checkbar(top, ['No']).grid(row=7, column=3, columnspan=1, padx=2, pady=2)

# Symptoms
top.textBox_symp = Text(top.master, height=2, width=20)
# top.textBox_symp.grid(row=8, column=1, columnspan=2, padx=2, pady=2)
top.LabelBox_symp = Label(top.master, text="Symptoms:\n Please select all symptoms you are experiencing:")
top.LabelBox_symp.grid(row=8, column=0)
cough_var = IntVar()
Checkbutton(top, text="Cough", variable=cough_var).grid(row=8, column=2, columnspan=1, padx=2, pady=2)
fever_var = IntVar()
Checkbutton(top, text="Fever", variable=fever_var).grid(row=8, column=3, columnspan=1, padx=2, pady=2)
fatigue_var = IntVar()
Checkbutton(top, text="Fatigue", variable=fatigue_var).grid(row=8, column=4, columnspan=1, padx=2, pady=2)
breathing_var = IntVar()
Checkbutton(top, text="Shortness Of Breath", variable=breathing_var).grid(row=8, column=5, columnspan=1, padx=2, pady=2)

# Feedback box
top.textBox_fb = Text(top.master, height=5, width=30)
top.textBox_fb.grid(row=10, column=1, columnspan=5, padx=5, pady=5)
top.LabelBox_fb = Label(top.master, text="Feedback: ")
top.LabelBox_fb.grid(row=10, column=0)

# Enter button
top.enter = Button(top.master, height=2, width=8, padx=3, pady=3)
top.enter["text"] = "Enter"
top.enter["command"] = enter_user
top.enter.grid(row=0, column=3, padx=2, pady=2)

# Commit button
top.enter = Button(top.master, height=2, width=8, padx=3, pady=3)
top.enter["text"] = "Confirm"
top.enter["command"] = commit_info
top.enter.grid(row=11, column=3, padx=2, pady=2)

# Quit button
top.enter = Button(top.master, height=2, width=8, padx=3, pady=3)
top.enter["text"] = "Quit"
top.enter["command"] = quit_gui
top.enter.grid(row=11, column=0, padx=2, pady=2)

# Create a socket
# socket.SOCK_STREAM - TCP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

top.mainloop()

while True:
    # Wait for user to input a message
    message = input(f'{user_id} > ')
    # If message is not empty - send it
    if message:
        while True:
            receive_message(client_socket)
