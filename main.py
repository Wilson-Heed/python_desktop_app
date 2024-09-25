from tkinter import *
#from authentication.register import signup
#from authentication.login import login
#from features.deposit import deposit
from database.postgres_db import connect
import bcrypt
from tkinter import messagebox as msg

def validate_numeric_input(char):
    return char.isdigit() or char == ""


# REGISTER

def signup():
    global register_screen
    global username
    global password
    global email
    global phone_no
    global address
    global username_entry
    global password_entry
    global email_entry
    global phone_no_entry
    global address_entry
    
    register_screen = Toplevel(main_screen)
    register_screen.geometry("600x500")
    register_screen.title("Create an account")

    username = StringVar()
    password = StringVar()
    email = StringVar()
    phone_no = StringVar()
    address = StringVar()

    validate_cmd = register_screen.register(validate_numeric_input)

    Label(register_screen, text="").pack()
    Label(register_screen, text="Please enter the following details", bg="red", font=("Calibri", 13)).pack()
    
    username_label = Label(register_screen, text="Username * ")
    username_label.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()

    password_label = Label(register_screen, text="Password * ")
    password_label.pack()
    password_entry = Entry(register_screen, textvariable=password, show="*")
    password_entry.pack()

    email_label = Label(register_screen, text="Email * ")
    email_label.pack()
    email_entry = Entry(register_screen, textvariable=email)
    email_entry.pack()

    phone_no_label = Label(register_screen, text="Phone_no * ")
    phone_no_label.pack()
    phone_no_entry = Entry(register_screen, textvariable=phone_no, validate="key", validatecommand=(validate_cmd, "%S"))
    phone_no_entry.pack()

    address_label = Label(register_screen, text="Address * ")
    address_label.pack()
    address_entry = Entry(register_screen, textvariable=address)
    address_entry.pack()

    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", bg="green", font=("Calibri", 13), width=13, height=1, command=register_user).pack()

    signup()

def register_user():
    username_info = username.get()
    password_info = password.get()
    email_info = email.get()
    phone_no_info = phone_no.get()
    address_info = address.get()

    hashed_password = bcrypt.hashpw(password_info.encode('utf-8'), bcrypt.gensalt())

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO user_acct(username, password, email, phone_no, address)
        VALUES(%s, %s, %s, %s, %s)
        """, (username_info, hashed_password.decode('utf-8'), email_info, phone_no_info, address_info)
    )
    
    conn.commit()
    cur.close()
    conn.close()

    username_entry.delete(0, END)
    password_entry.delete(0, END)
    email_entry.delete(0, END)
    phone_no_entry.delete(0, END)
    address_entry.delete(0, END)


    Label(register_screen, text="Registration successfully", fg="green", font=("Calibri", 13)).pack()

    register_user()


# LOGIN

def login():
    global login_screen
    global email_entry
    global password_entry
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("600x500")

    email = StringVar()
    password = StringVar()

    Label(login_screen, text="Please enter the following details", bg="red", font=('Calibri', 13))
    email_label = Label(login_screen, text="Email * ")
    email_label.pack()
    email_entry = Entry(login_screen, textvariable=email)
    email_entry.pack()
    password_label = Label(login_screen, text="password * ")
    password_label.pack()
    password_entry = Entry(login_screen, textvariable=password, show= '*').pack()

    Button(login_screen, text="Login", bg="green", command=login_verify).pack()

def login_verify(password):
    email_info = email_entry.get()
    password_info = password_entry.get()
    
    conn = connect()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM user_acct WHERE email = %s AND password = %s;
        """, (email_info,)
    )
    result = cur.fetchone()

    conn.close()

    if result:
        stored_hashed_password = result[0].encode('utf-8')
        if bcrypt.checkpw(password_info.encode('utf-8'), stored_hashed_password):
            login_success()
        else:
            password_invalid()
    else:
        user_not_found()

def login_success():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")

    Label(login_success_screen, text="Login Successfully", fg="green", font=("Calibri", 13)).pack()
    Button(login_success_screen, text='OK', command=menu).pack()

def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Failed")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User not found", fg="red", font= ("Calibri", 13)).pack()
    Button(user_not_found_screen, text="OK", bg="red", command=delete_user_not_found).pack()

def delete_user_not_found():
    user_not_found_screen.destroy()

def password_invalid():
    global password_invalid_screen
    password_invalid_screen = Toplevel(login_screen)
    password_invalid_screen.title("Password")
    password_invalid_screen.geometry("150x100")
    Label(password_invalid_screen, text="Password is invalid", fg="red", font=("Calibri", 13)).pack()
    Button(password_invalid_screen, text="OK", bg="red", command=delete_password_invalid)

def delete_password_invalid():
    password_invalid_screen.destroy()
    
    # DEPOSIT
    
    
def deposit():
    global deposit_screen
    global name_entry
    global account_number_entry
    global amount_entry
    global name_label
    global account_number_label
    global amount_label
    global name
    global account_number
    global amount

    
    name = StringVar()
    account_number = StringVar()
    amount = StringVar()
    
    deposit_screen = Toplevel(menu_screen)
    deposit_screen.title("Deposit Screen")
    deposit_screen.geometry("600x500")
    
    Label(deposit_screen, text="")
    Label(deposit_screen, text="Please fill the details", bg='red', font=('Calibri', 13)).pack()
    name_label = Label(deposit_screen, text="Name", font=('Calbri', 13)).pack()
    name_entry = Entry(deposit_screen, textvariable=name).pack()
    account_number_label = Label(deposit_screen, text="Account Number", font=('Calibri', 13)).pack()
    account_number_entry = Entry(deposit_screen, textvariable=account_number).pack()
    amount_label = Label(deposit_screen, text="Amount", font=('Calibri', 13)).pack()
    amount_entry = Entry(deposit_screen, textvariable=amount).pack()
    
    Button(deposit_screen, text="Deposit", bg="green", font=('Calibri', 13), width=13, height=1, command=deposit_verify).pack()
    
def deposit_verify():
    #from authentication.register import email
    conn = connect()
    cur = conn.cursor()
    
    name_info = name.get()
    account_number_info = account_number.get()
    amount_info = amount.get()
    email_info = email.get()
    cur.execute(
        """
        SELECT id FROM user_acct WHERE email = %s
        """, (email_info)
    )
    user = cur.fetchone()
    if user is None:
        msg.showerror('Error', 'User not found')
        
    user_id = user[0]
    
    cur.execute(
        """
        INSERT INTO transactions(name, account_number, amount, user_id)
        VALUES(%s, %s, %s, %s)
        """,(name_info, account_number_info, amount_info, user_id)
    )
    
    cur.execute(
        """
        UPDATE user_acct SET balance = %s WHERE email = %s
        """, (amount_info, email_info)
    )
    
    conn.commit()
    conn.close()
    cur.close()
    msg.showinfo('Saved', 'Record info has been saved')
    
    
    # WITHDRAW
    
def withdraw():
    global withdraw_screen
    global withdraw_name_entry
    global withdraw_amount_entry
    global withdraw_name
    global withdraw_account_no
    global withdraw_account_no_entry
    global withdraw_amount
    withdraw_screen = Toplevel(menu_screen)
    withdraw_screen.title("Withdraw Screen")
    withdraw_screen.geometry("600x500")
    
    withdraw_name = StringVar()
    withdraw_account_no = StringVar()
    withdraw_amount = StringVar() 
    
    Label(withdraw_screen, text="").pack()
    Label(withdraw_screen, text="Please fill the details", bg='red', font=('Calibri', 13)).pack()
    Label(withdraw_screen, text="Name", font=('Calbri', 13)).pack()
    withdraw_name_entry = Entry(withdraw_screen, textvariable=withdraw_name).pack()
    Label(withdraw_screen, text="Account Number", font=('Calibri', 13)).pack()
    withdraw_account_no_entry = Entry(withdraw_screen, textvariable=withdraw_account_no).pack()
    Label(withdraw_screen, text="Amount", font=('Calibri', 13)).pack()
    withdraw_amount_entry = Entry(withdraw_screen, textvariable=withdraw_amount).pack()
    Button(withdraw_screen, text="Withdraw", bg="green", font=("Calibri", 13))
    
def withdraw_verify():
    conn = connect()
    cur = conn.coursor()
    
    withdraw_name_info = withdraw_name.get()
    withdraw_account_no_info = withdraw_account_no.get()
    withdraw_amount_info = withdraw_amount.get()
    withdraw_email_info = email_entry.get()
    
    cur.execute(
        """
        SELECT id, amount FROM user_acct WHERE email = %s
        """, (withdraw_email_info,)
        
    ) 
    user = cur.fetchone()
    if user is None:
        msg.showerror('Error', 'User not Found')
        
    user_id = user[0]
    cur.execute(
        """
        SELECT id, balance FROM user_acct WHERE email = %s
        """, (user_id,)
    )
    trans_amount = cur.fetchone()
    current_balance = float(trans_amount[1])
    if float(withdraw_amount_info) > current_balance:
        msg.showerror('Error', 'insufficient funds')
        return
    
    new_balance = current_balance - float(withdraw_amount_info)
    
    cur.execute(
        """
        UPDATE useer_acct SET balance = %s WHERE id = %s        
        """, (new_balance, user_id)
    )
    
    cur.execute(
        """
        INSERT INTO transaction(name, account_number, amount, transaction_type, user_id)
        VALUES (%s, %s, %s, 'withdrawal', %s)
        """, (
            withdraw_name_info,
            withdraw_account_no_info,
            withdraw_amount_info,
            user_id
        )
        
    )
    conn.commit()
    conn.close()
    cur.close()
    msg.showinfo('Saved', f'Amount of ${withdraw_amount_info} withdrawed successful')
    
    
    #TRANSFER
    
    
def transfer():
    global transfer_screen
    global transfer_amount_entry
    global transfer_amount
    global transfer_sender_account
    global transfer_sender_account_entry
    global transfer_recepient_name_entry
    global transfer_recepient_name
    global transfer_recepient_account_no_entry
    global transfer_recepient_account_no

    transfer_screen = Toplevel(menu_screen)
    transfer_screen.title("Transfer Screen")
    transfer_screen.geometry("600x500")
    
    transfer_amount = StringVar()
    transfer_recepient_name = StringVar()
    transfer_recepient_account_no = StringVar()
    transfer_sender_account = StringVar()
    
    Label(transfer_screen, text="").pack()
    Label(transfer_sender_account, text="Sender Name").pack()
    transfer_sender_account_entry = Entry(transfer_screen, textvariable=transfer_sender_account).pack()
    Label(transfer_screen, text="Recepient Name").pack()
    transfer_recepient_name_entry = Entry(transfer_screen, textvariable=transfer_recepient_name).pack()
    Label(transfer_screen, text="Recepient Account Number",).pack()
    transfer_recepient_account_no_entry = Entry(transfer_screen, textvariable=transfer_recepient_account_no).pack()
    Label(transfer_screen, text="Enter Amount").pack()
    transfer_amount_entry = Entry(transfer_screen, textvariable=transfer_amount).pack()
    Button(transfer_screen, text='Transfer', bg='red', font=('Calibri', 13)).pack()
    
def transfer_verify():
    conn = connect()
    cur = conn.cursor()
    
    sender_acct_info = transfer_sender_account.get()
    recepient_acct_no_info = transfer_recepient_account_no.get()
    transfer_amount_info = transfer_amount.get()
    #transfer_email_info = email_entry.get()
    
    cur.execute(
        """
        SELECT u.id, u.balance FROM user_acct u
        JOIN transcactions t ON u.d = t.user_id
        WHERE t,account_number = %s
        """,  (sender_acct_info,)
    )
    sender = cur.fetchone()
    if sender is None:
        msg.showerror('Error', 'Sender account not found')
    sender_id = sender[0]
    sender_balance = float(sender[1])
    
    if float(transfer_amount_info) > sender_balance:
        msg.showerror('Error', f'Insuffuicient fund, your balance is ${sender_balance}')
        return
    
    cur.execute(
        """ SELECT u.id, u u.balance
        FROM user_acct u 
        JOIN transactions t ON u.id = t.user_id
        WHERE t.account_number = %s
        """,(recepient_acct_no_info,)
    )
    recepient = cur.fetchone()
    if recepient is None:
        msg.showerror('Error', 'Recepient not found')
        
    recepient_id = recepient[0]
    recepient_balance =  float(recepient[1])
    
    new_sender_balance = sender_balance - float(transfer_amount_info)
    new_recepient_balance = recepient_balance + float(transfer_amount_info)   
    
    cur.execute(
        """
        UPDATE user_acct SET balance = %s WHERE id = %s
        """, (new_sender_balance, sender_id)
    )
    
    cur.execute(
        """
        UPDATE user_acct SET balance = %s WHERE id = %s
        """, (new_recepient_balance, recepient_id)
    )    
    
    cur.execute(
        """
        INSERT INTO transaction(name, account_nymber, amount, transaction_type, user_id)
        VALUES (%s, %s, %s, 'transfer_sent', %s)
        """,(
            'sender',
            sender_acct_info,
            transfer_amount_info,
            sender_id
        )
    )
     
    cur.execute(
        """
        INSERT INTO transaction(name, account_nymber, amount, transaction_type, user_id)
        VALUES (%s, %s, %s, 'transfer_received', %s)
        """,(
            'Recepient',
            recepient_acct_no_info,
            transfer_amount_info,
            recepient_id
        )
    )
    conn.commit()
    conn.close()
    cur.close()
    msg.showinfo('Saved', f'Amount of ${transfer_amount_info} transaction successful to {recepient_acct_no_info}')
    
    #CHECK BALANCE
    
def check_balance():
    global balance_screen
    global acct_entry
    global acct_number 
    
    balance_screen = Toplevel(menu_screen)
    balance_screen.title("Check your balance")
    balance_screen.geometry("600x500")
    
    acct_number = StringVar()
    Label(balance_screen, text='Enter your account number').pack()
    acct_entry = Entry(balance_screen, textvariable=acct_number).pack()
    Button(balance_screen, text="check Balance", bg="green", font=("Calibri", 13), width=10, height=1) 
    
def check_balance_verify():
    conn = connect()
    cur = conn.cursor()
    
    acct_entry_info = acct_number.get()
    check_balance_email_info = email_entry.get()
    
    cur.execute(
        """
        SELECT id 
        FROM user_acct
        Where email = %s
        """, (check_balance_email_info,)
    )
    
    current_user = cur.fetchone()
    if current_user is None:
        msg.showerror('Error', 'Current user not found')
        return
    current_user_id = current_user[0]
    
    cur.execute(
        """ SELECT u.id, u.balance
        FROM user_acct u 
        JOIN transactions t ON u.id = t.user_id
        WHERE t.account_number = %s
        """,(acct_entry_info,)
    )
    
    acct = cur.fetchone()
    if acct is None:
        msg.showerror('Error', 'Account Not Found')
    else:
        user_id = acct[0]
        balance = acct[1]
        
        if user_id != current_user_id:
            msg.showerror('Error', 'Ypu are not authorized to view this account')
        else:
            msg.showinfo('Success', f'Your balance is ${balance}')
    
    
def menu():
    global menu_screen
    menu_screen = Toplevel(main_screen)
    menu_screen.title("Menu")
    menu_screen.geometry("3000x2500")
    
    Button(menu_screen, text='Deposit', bg='violet', fg='black', width="30", height='2', font=('Arial Bold', 10), command=deposit).pack()
    Button(menu_screen, text='Withdraw', bg='green', fg='black', width="30", height='2', font=('Arial Bold', 10), command=withdraw).pack()
    Button(menu_screen, text='Balance', bg='yellow', fg='black', width="30", height='2', font=('Arial Bold', 10), command=check_balance).pack()
    Button(menu_screen, text='Transfer', bg='red', fg='black', width="30", height='2', font=('Arial Bold', 10), command=transfer).pack()
    Label(menu_screen, text="").pack(side=LEFT)
    
def main_action_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x2500")
    main_screen.title("User Account Login/Register")
    
    Label(text="Select your choice", bg="green", width="300", height="2", font=("Calibri", 13)).pack()
    
    Button(text="Register", bg="red", width="30", height="2", font=("Arial Bold", 10), command=signup).pack()
    Button(text="Login", bg="green", width="30", height="2", font=("Arial Bold", 10), command=login).pack()
    
    main_screen.mainloop()
    
    main_action_screen()   


# TRANFER

    


    
    


# from tkinter import *
# from database.postgres_db import connect  # Assuming this is your database connection module
# import bcrypt
# from tkinter import messagebox as msg


# # Helper function to validate numeric input
# def validate_numeric_input(char):
#     return char.isdigit() or char == ""

# def menu():
#     global menu_screen
#     menu_screen = Toplevel(main_screen)
#     menu_screen.title("Menu")
#     menu_screen.geometry("3000x2500")
    
#     Button(menu_screen, text='Deposit', bg='violet', fg='black', width="30", height='2', font=('Arial Bold', 10), command=deposit).pack()
#     Button(menu_screen, text='Withdraw', bg='green', fg='black', width="30", height='2', font=('Arial Bold', 10), command=withdraw).pack()
#     Button(menu_screen, text='Balance', bg='yellow', fg='black', width="30", height='2', font=('Arial Bold', 10)).pack()
#     Button(menu_screen, text='Transfer', bg='red', fg='black', width="30", height='2', font=('Arial Bold', 10)).pack()
#     Label(menu_screen, text="").pack(side=LEFT)
  


# def main_action_screen():
#     global main_screen
#     main_screen = Tk()
#     main_screen.geometry("300x2500")
#     main_screen.title("User Account Login/Register")
    
#     Label(text="Select your choice", bg="green", width="300", height="2", font=("Calibri", 13)).pack()
    
#     Button(text="Register", bg="red", width="30", height="2", font=("Arial Bold", 10), command=signup).pack()
#     Button(text="Login", bg="green", width="30", height="2", font=("Arial Bold", 10), command=login).pack()
    
#     main_screen.mainloop()
#     main_action_screen()


# # Register Function
# def signup():
#     global register_screen, username, password, email, phone_no, address
#     global username_entry, password_entry, email_entry, phone_no_entry, address_entry
    
#     register_screen = Toplevel(main_screen)
#     register_screen.geometry("600x500")
#     register_screen.title("Create an Account")

#     # Initialize variables
#     username = StringVar()
#     password = StringVar()
#     email = StringVar()
#     phone_no = StringVar()
#     address = StringVar()

#     validate_cmd = register_screen.register(validate_numeric_input)

#     Label(register_screen, text="Please enter the following details", bg="red", font=("Calibri", 13)).pack()
#     Label(register_screen, text="Username * ").pack()
#     username_entry = Entry(register_screen, textvariable=username)
#     username_entry.pack()

#     Label(register_screen, text="Password * ").pack()
#     password_entry = Entry(register_screen, textvariable=password, show="*")
#     password_entry.pack()

#     Label(register_screen, text="Email * ").pack()
#     email_entry = Entry(register_screen, textvariable=email)
#     email_entry.pack()

#     Label(register_screen, text="Phone_no * ").pack()
#     phone_no_entry = Entry(register_screen, textvariable=phone_no, validate="key", validatecommand=(validate_cmd, "%S"))
#     phone_no_entry.pack()

#     Label(register_screen, text="Address * ").pack()
#     address_entry = Entry(register_screen, textvariable=address)
#     address_entry.pack()

#     Button(register_screen, text="Register", bg="green", font=("Calibri", 13), width=13, height=1, command=register_user).pack()

#     signup()

# def register_user():
#     username_info = username.get()
#     password_info = password.get()
#     email_info = email.get()
#     phone_no_info = phone_no.get()
#     address_info = address.get()

#     hashed_password = bcrypt.hashpw(password_info.encode('utf-8'), bcrypt.gensalt())

#     conn = connect()
#     cur = conn.cursor()

#     try:
#         cur.execute(
#             """
#             INSERT INTO user_acct(username, password, email, phone_no, address)
#             VALUES(%s, %s, %s, %s, %s)
#             """, (username_info, hashed_password.decode('utf-8'), email_info, phone_no_info, address_info)
#         )
#         conn.commit()
#         msg.showinfo("Registration", "Registration successful")
#     except Exception as e:
#         msg.showerror("Error", str(e))
#     finally:
#         cur.close()
#         conn.close()

#     username_entry.delete(0, END)
#     password_entry.delete(0, END)
#     email_entry.delete(0, END)
#     phone_no_entry.delete(0, END)
#     address_entry.delete(0, END)
    
#     register_user()


# # Login Function
# def login():
#     global login_screen, email_entry, password_entry, email, password
    
#     login_screen = Toplevel(main_screen)
#     login_screen.title("Login")
#     login_screen.geometry("600x500")

#     email = StringVar()
#     password = StringVar()

#     Label(login_screen, text="Please enter the following details", bg="red", font=('Calibri', 13)).pack()
#     Label(login_screen, text="Email * ").pack()
#     email_entry = Entry(login_screen, textvariable=email)
#     email_entry.pack()

#     Label(login_screen, text="Password * ").pack()
#     password_entry = Entry(login_screen, textvariable=password, show='*')
#     password_entry.pack()

#     Button(login_screen, text="Login", bg="green", command=login_verify).pack()


# def login_verify():
#     email_info = email_entry.get()
#     password_info = password_entry.get()
    
#     conn = connect()
#     cur = conn.cursor()
    
#     try:
#         cur.execute(
#             """
#             SELECT password FROM user_acct WHERE email = %s
#             """, (email_info,)
#         )
#         result = cur.fetchone()

#         if result and bcrypt.checkpw(password_info.encode('utf-8'), result[0].encode('utf-8')):
#             login_success()
#         else:
#             msg.showerror("Error", "Invalid credentials")
#     except Exception as e:
#         msg.showerror("Error", str(e))
#     finally:
#         cur.close()
#         conn.close()


# def login_success():
#     msg.showinfo("Success", "Login Successfully")
#     menu()


# # Deposit Function
# def deposit():
#     global deposit_screen, name_entry, account_number_entry, amount_entry
#     global name, account_number, amount
    
#     deposit_screen = Toplevel(menu_screen)
#     deposit_screen.title("Deposit Screen")
#     deposit_screen.geometry("600x500")

#     name = StringVar()
#     account_number = StringVar()
#     amount = StringVar()

#     Label(deposit_screen, text="Please fill the details", bg='red', font=('Calibri', 13)).pack()
#     Label(deposit_screen, text="Name", font=('Calbri', 13)).pack()
#     name_entry = Entry(deposit_screen, textvariable=name)
#     name_entry.pack()
    
#     Label(deposit_screen, text="Account Number", font=('Calibri', 13)).pack()
#     account_number_entry = Entry(deposit_screen, textvariable=account_number)
#     account_number_entry.pack()

#     Label(deposit_screen, text="Amount", font=('Calibri', 13)).pack()
#     amount_entry = Entry(deposit_screen, textvariable=amount)
#     amount_entry.pack()

#     Button(deposit_screen, text="Deposit", bg="green", font=('Calibri', 13), width=13, height=1, command=deposit_verify).pack()


# def deposit_verify():
#     conn = connect()
#     cur = conn.cursor()
    
#     try:
#         name_info = name.get()
#         account_number_info = account_number.get()
#         amount_info = amount.get()
#         email_info = email.get()

#         cur.execute(
#             """
#             SELECT id FROM user_acct WHERE email = %s
#             """, (email_info,)
#         )
#         user = cur.fetchone()

#         if user is None:
#             msg.showerror('Error', 'User not found')
#             return
        
#         user_id = user[0]

#         cur.execute(
#             """
#             INSERT INTO transactions(name, account_number, amount, user_id)
#             VALUES(%s, %s, %s, %s)
#             """, (name_info, account_number_info, amount_info, user_id)
#         )
#         conn.commit()
#         msg.showinfo('Saved', 'Record info has been saved')
#     except Exception as e:
#         msg.showerror("Error", str(e))
#     finally:
#         cur.close()
#         conn.close()


# # Withdraw Function
# def withdraw():
#     global withdraw_screen, withdraw_name_entry, withdraw_account_no_entry, withdraw_amount_entry
#     global withdraw_name, withdraw_account_no, withdraw_amount
    
#     withdraw_screen = Toplevel(menu_screen)
#     withdraw_screen.title("Withdraw Screen")
#     withdraw_screen.geometry("600x500")

#     withdraw_name = StringVar()
#     withdraw_account_no = StringVar()
#     withdraw_amount = StringVar()

#     Label(withdraw_screen, text="Please fill the details", bg='red', font=('Calibri', 13)).pack()
#     Label(withdraw_screen, text="Name", font=('Calbri', 13)).pack()
#     withdraw_name_entry = Entry(withdraw_screen, textvariable=withdraw_name)
#     withdraw_name_entry.pack()

#     Label(withdraw_screen, text="Account Number", font=('Calibri', 13)).pack()
#     withdraw_account_no_entry = Entry(withdraw_screen, textvariable=withdraw_account_no)
#     withdraw_account_no_entry.pack()

#     Label(withdraw_screen, text="Amount", font=('Calibri', 13)).pack()
#     withdraw_amount_entry = Entry(withdraw_screen, textvariable=withdraw_amount)
#     withdraw_amount_entry.pack()

#     Button(withdraw_screen, text="Withdraw", bg="green", font=("Calibri", 13), command=withdraw_verify).pack()


# def withdraw_verify():
#     conn = connect()
   

    