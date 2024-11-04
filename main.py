#-----------------------------IMPORTS------------------------------#
from tkinter import *
from tkinter import messagebox, simpledialog
import random
import pyperclip
import json
from encryptor import Encryptor
from decryptor import Decryptor
from duplicateRemover import DuplicateRemover

#--------------------CONSTANTS--------------------#
LOGO_BG = '#CBD2A4'
WINDOW_BG = '#9A7E6F'
BUTTON_BG = '#E9EED9'
FONT = ("Ariel",12,'normal')

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    lower_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    upper_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [random.choice(lower_letters) for _ in range(random.randint(4,5))]
    password_list += [random.choice(upper_letters) for _ in range(random.randint(4, 5))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2,4))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2,4))]

    random.shuffle(password_list)

    password ="".join(password_list)

    password_input.delete(0, END)
    password_input.insert(0, password)

    pyperclip.copy(password_input.get())

    messagebox.showinfo(title='Notice', message='Password copied to clipboard!')

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password(password_code):
    secure_web = Encryptor(password_code, website_input.get())
    secure_username = Encryptor(password_code,username_input.get())
    secure_password = Encryptor(password_code, password_input.get())

    new_data = {
        secure_web.secretMessage:{
            'email': secure_username.secretMessage,
            'password': secure_password.secretMessage
        }
    }

    if secure_web.secretMessage == "" or secure_username.secretMessage == "" or secure_password.secretMessage == "":
        messagebox.showinfo(title="oops", message= "All fields must have entry to save info!")
    else:
        try:
            with open('data.json', 'r') as data_file:
                # Open and read current data into dictionary
                data = json.load(data_file)
        except FileNotFoundError:
            with open('data.json', 'w') as data_file:
                # Write new info back to data_file
                json.dump(new_data, data_file, indent=4)
        else:
            # Update old data with new data
            data.update(new_data)
            with open('data.json', 'w') as data_file:
                # Write new info back to data_file
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, END)
            password_input.delete(0, END)

#-------------------- SEARCH PASSWORD --------------------#
def search_password(password_code):
    secure_web = Encryptor(password_code, website_input.get())

    try:
        with open('data.json', 'r') as data_file:
            # Open and read current data into dictionary
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo('No Data','No password database found!')
    else:
        try:
            email = Decryptor(password_code, data[secure_web.secretMessage]['email'])
            password = Decryptor(password_code, data[secure_web.secretMessage]['password'])
        except KeyError:
            username_input.delete(0, END)
            password_input.delete(0, END)
            messagebox.showinfo('No Password Found', f'No password found for {website_input.get()}')
        else:
            username_input.delete(0, END)
            password_input.delete(0, END)
            username_input.insert(0, email.unsecretMessage)
            password_input.insert(0, password.unsecretMessage)

#--------------------GET MASTER PASSWORD--------------------#
def master_password():
    while True:
        master_passcode = simpledialog.askstring("Master Password", "Please enter your master password: ", show='*')
        if master_passcode:  # Check if the password is not empty
            return master_passcode
        else:
            messagebox.showwarning("Invalid Entry", "Master password cannot be empty.")
            exit()
# ---------------------------- UI SETUP ------------------------------- #

master = master_password()

##Window
window = Tk()
window.title("My Passwords")
window.config(padx=20, pady=20, bg=WINDOW_BG)

##Canvas
logo = PhotoImage(file='logo.png')
canvas = Canvas(width=210, height=199, bg=LOGO_BG, highlightthickness=0)
canvas.create_image(105, 99,image=logo)
canvas.grid(row=0,column=1)

##Labels
website_label = Label(text="Website: ",bg=WINDOW_BG, font=FONT)
website_label.grid(row=1,column=0)
username_label = Label(text='Email\\Username: ', bg=WINDOW_BG, font=FONT)
username_label.grid(row=2, column=0)
password_label = Label(text='Password: ', bg=WINDOW_BG, font=FONT)
password_label.grid(row=3, column=0)

##Inputs Boxes
website_input = Entry(width=38)
website_input.grid(row=1, column=1, columnspan=2, sticky='w')
website_input.focus()
username_input = Entry(width=53)
username_input.grid(row=2, column=1, columnspan=2, sticky='w')
password_input = Entry(width=33)
password_input.grid(row=3, column=1, sticky='w')

##Buttons
search_button = Button(text='Search', bg=BUTTON_BG, width=11, command=lambda: search_password(master))
search_button.grid(row=1, column=2, sticky='e')
gen_password_button = Button(text='Generate Password', bg=BUTTON_BG, command=generate_password)
gen_password_button.grid(row=3, column=2, sticky='w')
add_button= Button(text='Add', width=36, bg=BUTTON_BG, command=lambda: save_password(master))
add_button.grid(row=4, column=1, columnspan=2, sticky='w')

try:
    with open('data.json', 'r') as data_file:
        data = json.load(data_file)
except FileNotFoundError:
    pass
else:
    available_passwords = ''
    for key in data.keys():
        wp = Decryptor(master, key)
        available_passwords += f'{wp.unsecretMessage}\n'
    messagebox.showinfo('Your Password', f'If list is unreadable you Master password is wrong!\nAvailable passwords\n{available_passwords}')


window.mainloop()