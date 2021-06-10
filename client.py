
import socket
import tkinter as tk


root = tk.Tk()
root.title = ("Register window")
root.geometry("500x400")


HOST = socket.gethostbyname(socket.gethostname())
PORT = 5050
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
match_label = tk.Label(root)
query_label = tk.Label(root)


class GUI_TOLLS:

    def __init__(self, first_name="", last_name="", phonenumber="", mail_adress="", socialnumber="", search_txt="" ):
        self.first_name = first_name
        self.last_name = last_name
        self.phonenumber = phonenumber
        self.mail_adress = mail_adress
        self.socialnumber = socialnumber
        self.search_txt = search_txt

    def generateACK(self, comment):
        if comment == "register":
            ACK_TEXT = "register " + self.first_name + " " + self.last_name + " " + self.phonenumber + " " + self.mail_adress + " " + self.socialnumber
        elif comment == "show":
            ACK_TEXT = "show"
        elif comment == "search":
            ACK_TEXT = "search " + self.search_txt
        return ACK_TEXT

    def register(self):
        self.first_name = first_name_txt.get()
        self.last_name = last_name_txt.get()
        self.phonenumber = phonenumber_txt.get()
        self.mail_adress = mail_adress_txt.get()
        self.socialnumber = socialnumber_txt.get()
        ACK_TEXT = self.generateACK("register")
        receiveTextViaSocket(ACK_TEXT)
        first_name_txt.delete(0, tk.END)
        last_name_txt.delete(0, tk.END)
        phonenumber_txt.delete(0, tk.END)
        mail_adress_txt.delete(0, tk.END)
        socialnumber_txt.delete(0, tk.END)
        search_txt.delete(0, tk.END)

    def show(self):
        global query_label
        query_label.destroy()
        ACK_TEXT = self.generateACK("show")
        all_records = receiveTextViaSocket(ACK_TEXT)
        query_label = tk.Label(root, text=all_records)
        query_label.grid(row=12, column=0, columnspan=2)

    def search(self):
        global match_label
        match_label.destroy()
        self.search_txt = search_txt.get()
        ACK_TEXT = self.generateACK("search")
        search_info = receiveTextViaSocket(ACK_TEXT)
        match_label = tk.Label(root, text=search_info)
        match_label.grid(row=13, column=0, columnspan=2)
        search_txt.delete(0, tk.END)


def receiveTextViaSocket(ACK_TEXT):

    encodedAckText = bytes(ACK_TEXT, 'utf-8')
    sock.sendall(encodedAckText)
    encodedMessage = sock.recv(1024)

    if not encodedMessage:
        raise ValueError

    message = encodedMessage.decode('utf-8')
    print(message)
    return message


if __name__ == '__main__':
    myGUI = GUI_TOLLS()
    connectionSuccessful = False
    while not connectionSuccessful:
        try:
            sock.connect((HOST, PORT))
            connectionSuccessful = True
        except ConnectionError as err:
            print(err)

    # ----------ENTRIES
    first_name_txt = tk.Entry(root, width=30)
    first_name_txt.grid(row=0, column=1)
    last_name_txt = tk.Entry(root, width=30)
    last_name_txt.grid(row=1, column=1)
    phonenumber_txt = tk.Entry(root, width=30)
    phonenumber_txt.grid(row=2, column=1)
    mail_adress_txt = tk.Entry(root, width=30)
    mail_adress_txt.grid(row=3, column=1)
    socialnumber_txt = tk.Entry(root, width=30)
    socialnumber_txt.grid(row=4, column=1)
    search_txt = tk.Entry(root, width=30)
    search_txt.grid(row=5, column=1)
    # -----------LABELS
    first_name_label = tk.Label(root, text='First Name')
    first_name_label.grid(row=0, column=0)
    last_name_label = tk.Label(root, text='Last Name')
    last_name_label.grid(row=1, column=0)
    phonenumber_label = tk.Label(root, text='Phonenumber')
    phonenumber_label.grid(row=2, column=0)
    mail_adress_label = tk.Label(root, text='E-Mail')
    mail_adress_label.grid(row=3, column=0)
    socialnumber_label = tk.Label(root, text='Socialnumber')
    socialnumber_label.grid(row=4, column=0)
    search_label = tk.Label(root, text="Search customer with personnummer")
    search_label.grid(row=5, column=0)
    # -----------BUTTONS
    submit_btn = tk.Button(root, text='Register', command=myGUI.register)
    submit_btn.grid(row=6, column=1, columnspan=2, padx=10, pady=10, ipadx=70)
    show_button = tk.Button(root, text="Show records", command=myGUI.show)
    show_button.grid(row=7, column=1, columnspan=2, padx=10, pady=10, ipadx=55)
    search_btn = tk.Button(root, text="Search", command=myGUI.search)
    search_btn.grid(row=8, column=1, columnspan=2, padx=10, pady=10, ipadx=40)
    root.mainloop()
