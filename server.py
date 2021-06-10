import socket
import time
import pickle
import os

HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050


class Customer():
    def __init__(self, first_name, last_name, phonenumber, mail_adress, socialnumber):
        self.first_name = first_name
        self.last_name = last_name
        self.phonenumber = phonenumber
        self.mail_adress = mail_adress
        self.socialnumber = socialnumber


class CustomerInfo():
    def __init__(self):
        if os.path.isfile('./cust.pickle'):
            pickle_in = open("cust.pickle", "rb")
            self.customer_list = pickle.load(pickle_in)
        else:
            self.customer_list = []  # Use dump in here from existing record

    def register(self, info):

        first_name = info[0]
        last_name = info[1]
        phonenumber = info[2]
        mail_adress = info[3]
        socialnumber = info[4]
        obj = Customer(first_name, last_name, phonenumber, mail_adress, socialnumber)
        self.customer_list.append(obj)

        pickle_out = open("cust.pickle", "wb")
        pickle.dump(self.customer_list, pickle_out)
        pickle_out.close()
        return "succsess"

    def show(self):

        all_records = ""
        for record in self.customer_list:
            all_records += str(record.first_name) + " " + str(record.last_name) + " " + str(record.phonenumber) + " " + str(record.mail_adress) + " " + str(record.socialnumber) + "\n"
        return all_records

    def search(self, info):
        num = info
        record = []
        for cust in self.customer_list:
            cust.first_name
            cust.socialnumber
            cust.last_name
            if cust.socialnumber == num:
                record = cust
                break
        search_info = str(record.first_name) + " " + str(record.last_name) + " " + str(record.phonenumber) + " " + str(record.mail_adress) + " " + str(record.socialnumber) + "\n"
        return search_info


def sendTextViaSocket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen()
    print(f"[LISTENING] Server is listening on {HOST}")
    conn, addr = sock.accept()
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        encodedAckText = conn.recv(1024)
        ackText = encodedAckText.decode('utf-8')
        print(ackText)

        textsplit = ackText.split()
        if textsplit[0] == "register":
            message = custemers.register(textsplit[1:])
        elif textsplit[0] == "show":
            message = custemers.show()
        elif textsplit[0] == "search":
            message = custemers.search(textsplit[1])

        print(message)
        encodedMessage = bytes(message, 'utf-8')
        conn.sendall(encodedMessage)
        time.sleep(1)


if __name__ == '__main__':
    custemers = CustomerInfo()
    sendTextViaSocket()