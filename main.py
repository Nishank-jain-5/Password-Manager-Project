from tkinter import *
from tkinter import messagebox
import random
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    for char in range(nr_letters):
        password_list.append(random.choice(letters))

    for char in range(nr_symbols):
        password_list += random.choice(symbols)

    for char in range(nr_numbers):
        password_list += random.choice(numbers)

    random.shuffle(password_list)

    password = ""
    for char in password_list:
        password += char

    pass_entry.delete(0,END)
    pass_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_data():

    website = web_entry.get()
    email = email_entry.get()
    password = pass_entry.get()

    if len(email) == 0 or len(password) == 0 or len(website) == 0:
        messagebox.showinfo(title="Warning", message="You have left some field empty!")
    else:
        new_data = {
            website : {
                    "Email": email,
                    "Password": password
                }
            }

        # handle the exception if file is not exist

        try:
            with open("data.json", 'r') as file:
                # read/load data
                data = json.load(file)

        except FileNotFoundError:
            with open("data.json", 'w') as file:
                json.dump(new_data, file, indent=4)

        else:
            # update the data
            data.update(new_data)

            with open("data.json", 'w') as file:
                # save data into json file
                json.dump(data, file, indent=4)

        finally:
            web_entry.delete(0,END)
            email_entry.delete(0,END)
            pass_entry.delete(0,END)

# ---------------------------- find password ------------------------------- #

def find_password():
    website = web_entry.get()

    try:
        with open("data.json", 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website in data:
            email = data[website]["Email"]
            password = data[website]["Password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword:{password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100,100, image=logo)
canvas.grid(column=1, row=0)

web_label = Label(text="Website: ")
web_label.grid(column=0, row=1)

web_entry = Entry(width=21)
web_entry.focus()
web_entry.grid(column=1, row=1)

email_label = Label(text="Email/Username: ")
email_label.grid(column=0, row=2)

email_entry = Entry(width=40)
email_entry.grid(column=1, row=2, columnspan=2)

pass_label = Label(text="Password: ")
pass_label.grid(column=0, row=3)

pass_entry = Entry(width=21)
pass_entry.grid(column=1, row=3)

gen_pass_button = Button(text="Generate Password", command=generate_pass)
gen_pass_button.grid(column=2, row=3)

add_button = Button(text="Add", width=30, command=save_data)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
