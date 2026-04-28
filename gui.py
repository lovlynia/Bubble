import tkinter as tk
from tkinter import *
from session import Session
from user import User
from tkinter import messagebox

#Stephanie Abundio
#April 7,2026

''' to run file gui.py
    on windows terminal write : python gui.py 
     on mac terminal write : python3 gui.py 
'''

session= Session()
users=User()

#FUNCTIONS HERE  ***

# Function to validate the login
def validate_login():
    username = username_entry.get()
    password = password_entry.get()

    result=session.authenticate(username,password)

    # validation logic here
    if result:
        login_frame.place_forget() #hide login 
        chat_frame.place(relwidth=1,relheight=1)#show chat page
        load_contacts()
        sender_label.config(text="YOU (no chat selected)")

        for widget in [sender_log, middle_log]:
            widget.config(state=NORMAL)
            widget.delete(1.0, END)
            widget.config(state=DISABLED)
        
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

#validate creation of registration 
def creation():
    username=regusername_entry.get()
    password=regpassword_entry.get()
    first=firstname_entry.get()
    last=lastname_entry.get()

    check=users.register(first,last,username,password)
        
    if check == "Account created!":
        messagebox.showinfo("Success",check)
        show_login()
    else:
        messagebox.showerror("Error:",check)

#show login panel 
def show_login():
    reg_frame.place_forget()
    login_frame.place(relwidth=1,relheight=1)

#show registration panel 
def show_register():
    login_frame.place_forget()
    reg_frame.place(relwidth=1,relheight=1)

#loading contacts from json file 
def load_contacts():
    contact_list.delete(0,END)
    users.cursor.execute("SELECT username FROM users")

    rows=users.cursor.fetchall()
    for row in rows:
        name=row[0]
        if name!=session.logged_in_user:
            contact_list.insert(END,name)


def on_contact_click(event):
    selection = contact_list.curselection()
    if not selection:
        return

    selected = contact_list.get(selection[0])
    session.set_recipient(selected)

    sender_label.config(text=f"YOU → {selected}")

    for widget in [sender_log, middle_log]:
        widget.config(state=NORMAL)
        widget.delete(1.0, END)
        widget.config(state=DISABLED)

    all_msgs = session.get_conversations(selected)

    for msg in all_msgs:
        pt=session.receive_message(msg["ciphertext"])
        if msg["from"] == session.logged_in_user:
            log(sender_log, pt, side="right")   # YOU → right
        else:
            log(sender_log, pt, side="left")    # THEM → left

        log(middle_log, str(msg["ciphertext"]))

    

def send_message():
    msg = sender_entry.get().strip()
    if not msg:
        return

    ct = session.send_message(msg)
    pt = session.receive_message(ct)

    log(sender_log,pt,side="right")
    log(middle_log,     str(ct))

    sender_entry.delete(0, END)

def log(widget, text,side="left"):

    widget.config(state=NORMAL)

    if side=="right":
        widget.insert(END, text + "\n","right")  
    else:
        widget.insert(END, text + "\n","left")  
    widget.config(state=DISABLED)
    widget.see(END)

def logout():
    session.logout()
    chat_frame.place_forget()
    login_frame.place(relwidth=1, relheight=1)
    
    username_entry.delete(0, END)
    password_entry.delete(0, END)
    session.active_recipient = None
    sender_label.config(text="YOU (no chat selected)")

'''
End of all functions 
beginning of user interface 
that includes login, register, contacts panel and chatbox 
'''

root = tk.Tk()  # Create the main window
root.geometry("900x600")
root.title("Bubble")

#colors set & fonts 
BG_BLUE = "#6083CE"
BG_COLOR = "#A784E4"
TEXT_COLOR = "#101010"
HEADER_COLOR = "#FFFFFF"

FONT = "Helvetica 14"
FONT_BOLD =("Comic Sans MS", 16)

BUBBLE_SENT="#99d1f9"
BUBBLE_RECEIVED="#ee93ae"

#LOG IN ******************************************************************************

login_frame=tk.Frame(root,bg=BG_COLOR)
login_frame.place(relwidth=1,relheight=1)

img = tk.PhotoImage(file="bubble.png") #icon application
img = img.subsample(3, 3) 

#the label of application
Label(login_frame, bg=BG_BLUE, fg=HEADER_COLOR, text="BUBBLES", font=FONT_BOLD, pady=20,width=900).pack()

Label(login_frame,image=img,bg=BG_COLOR).pack(pady=10)

#username entry
username_label=tk.Label(login_frame,text="Username:",bg=BG_COLOR,fg=HEADER_COLOR,font=FONT)
username_label.pack()

username_entry = tk.Entry(login_frame,font=FONT,width=30)
username_entry.pack(pady=5)

# Create and place the password label and entry
password_label = tk.Label(login_frame, text="Password:",bg=BG_COLOR,fg=HEADER_COLOR,font=FONT)
password_label.pack()

password_entry = tk.Entry(login_frame,font=FONT,width=30, show="*")  # Show asterisks for password
password_entry.pack(pady=5)

login_button = tk.Button(login_frame, text="Login", font=FONT_BOLD, bg=BG_BLUE,fg=HEADER_COLOR,width=12,command=validate_login)
login_button.pack(pady=5)

register_button=tk.Button(login_frame,text="Register",
                          font=FONT_BOLD, bg=BG_BLUE, fg=HEADER_COLOR, width=12, command=show_register)
register_button.pack(pady=2)


#Register Section -- Account Creation 

reg_frame=tk.Frame(root,bg=BG_COLOR)

Label(reg_frame,bg=BG_BLUE, fg=HEADER_COLOR, text="BUBBLES",font=FONT_BOLD,
      pady=20, width=900).pack()

Label(reg_frame,text="Create Account",
      bg=BG_COLOR, fg=HEADER_COLOR,font=FONT_BOLD).pack(pady=5)

#first name input
firstname_label = tk.Label(reg_frame, text="First Name:",bg=BG_COLOR,fg=HEADER_COLOR,font=FONT)
firstname_label.pack()

firstname_entry = tk.Entry(reg_frame,font=FONT,width=30)
firstname_entry.pack(pady=5)

#last name input
lastname_label = tk.Label(reg_frame, text="Last Name:",bg=BG_COLOR,fg=HEADER_COLOR,font=FONT)
lastname_label.pack()

lastname_entry = tk.Entry(reg_frame,font=FONT,width=30)
lastname_entry.pack(pady=5)

#username input
regusername_label=tk.Label(reg_frame,text="Username:",bg=BG_COLOR,fg=HEADER_COLOR,font=FONT)
regusername_label.pack()

regusername_entry = tk.Entry(reg_frame,font=FONT,width=30)
regusername_entry.pack(pady=5)

# password input and entry
regpassword_label = tk.Label(reg_frame, text="Password:",bg=BG_COLOR,fg=HEADER_COLOR,font=FONT)
regpassword_label.pack()

regpassword_entry = tk.Entry(reg_frame,font=FONT,width=30, show="*")  # Show asterisks for password
regpassword_entry.pack(pady=5)

#create account :)
create_button=tk.Button(reg_frame,text="Register",
                          font=FONT_BOLD, bg=BG_BLUE, fg=HEADER_COLOR, width=12, command=creation)
create_button.pack(pady=5)

back_button=tk.Button(reg_frame,text="back to login",
                          font=FONT_BOLD, bg=BG_BLUE, fg=HEADER_COLOR, width=12, command=show_login)
back_button.pack(pady=2)

#CHAT BOX *****************************************************************************************

chat_frame=tk.Frame(root,bg=BG_COLOR)

#** contacts here ***
contact_panel=tk.Frame(chat_frame, bg=BG_BLUE,width=180)
contact_panel.pack(side=LEFT,fill=Y) #placing contacts section on left side of messaging application 
contact_panel.pack_propagate(False)

contact_label=tk.Label(contact_panel,text="Contacts",bg=BG_BLUE,fg=HEADER_COLOR,font=FONT_BOLD)
contact_label.pack(pady=10)

contact_list=tk.Listbox(contact_panel,bg=BG_BLUE,fg=HEADER_COLOR,font=FONT, selectbackground=BUBBLE_SENT,
                         borderwidth=0,highlightthickness=0)

contact_list.pack(fill=BOTH,expand=True, padx=5)
contact_list.bind("<ButtonRelease-1>", on_contact_click)

logout_button=tk.Button(contact_panel,text="LOGOUT",bg=BG_BLUE,fg=HEADER_COLOR,font=FONT,
                         width=20, command=logout)

logout_button.pack(side=BOTTOM, pady=10)

#** sender panel ***

sender_panel=tk.Frame(chat_frame,bg=BG_COLOR)
sender_panel.pack(side=LEFT,fill=BOTH,expand=True)

sender_label=tk.Label(sender_panel,text="YOU (no chat selected)",bg=BG_COLOR,fg=HEADER_COLOR,font=FONT_BOLD)
sender_label.pack(pady=5)

sender_log=tk.Text(sender_panel,bg=BG_COLOR,fg=TEXT_COLOR,
                   font=FONT,width=60)

sender_log.pack(fill=BOTH,expand=True)
sender_log.config(state=DISABLED)


scrollbar = Scrollbar(sender_log)
scrollbar.place(relheight=1, relx=0.974)

sender_entry = tk.Entry(sender_panel, bg="#A7AFB6", fg=TEXT_COLOR, font=FONT, width=55)
sender_entry.pack(pady=5)

send = tk.Button(sender_panel, text="Send", font=FONT_BOLD, bg=BG_BLUE,
              fg=HEADER_COLOR,command=send_message)

send.pack()

#** middle panel ***
middle_panel=tk.Frame(chat_frame,bg="#bbf3f0")
middle_panel.pack(side=LEFT,fill=BOTH,expand=True)

middle_label = tk.Label(middle_panel, text="Encrypted Channel",
                        bg="#c6fcf9", fg=HEADER_COLOR, font=FONT_BOLD)
middle_label.pack(pady=5)

middle_log = tk.Text(middle_panel, bg="#c6fcf9", fg=TEXT_COLOR,
                     font=FONT, state=DISABLED)

middle_log.pack(fill=BOTH, expand=True, padx=5)



#you've reached the end :)

root.mainloop()  # Start the event loop