import mysql.connector
import pyotp
import os
import password1
from cryptography.fernet import Fernet

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password1.PASSWORD1,
    database="itm"
)
cursor = conn.cursor()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def press_enter_to_continue():
    input("Press Enter to continue...")

def create_user():
    clear_screen()
    print("1. For UPI User")
    print("2. Create OTP Account")
    choice = input("Select an option: ")

    if choice == '1':
        mobile_number = input("Enter mobile number: ")
        pin = input("Enter PIN: ")
        cursor.execute('INSERT INTO users (mobile_number, pin) VALUES (%s, %s)', (mobile_number, pin))
        conn.commit()
        print("User created successfully!")
        press_enter_to_continue()
    elif choice == '2':
        uname = input("Enter Username: ")
        pwd = input("Enter Password: ")
        cursor.execute('INSERT INTO users (mobile_number, pin) VALUES (%s, %s)', (uname, pwd))
        conn.commit()
        print("User created successfully!")
        press_enter_to_continue()
    else:
        print("Invalid option. Please try again.")

def login():
    clear_screen()
    mobile_number = input("Enter mobile number: ")
    pin = input("Enter PIN: ")

    cursor.execute('SELECT * FROM users WHERE mobile_number=%s AND pin=%s', (mobile_number, pin))
    user = cursor.fetchone()
    if user:
        clear_screen()
        print("Login successful!")
        print("Press 1 to show balance")
        print("Press 2 to Pay")
        choice = input("Select an option: ")
        if choice == '1':
            show_balance(user[0])
            press_enter_to_continue()
        elif choice == '2':
            show_balance(user[0])
            pay_mobile(user[0])
        else:
            print("Invalid Input try again")
            press_enter_to_continue()
    else:
        print("Invalid mobile number or PIN.")
        press_enter_to_continue()

def generate_otp():
    return pyotp.TOTP(pyotp.random_base32()).now()

def show_balance(mobile_number):
    cursor.execute('SELECT balance FROM users WHERE mobile_number=%s', (mobile_number,))
    balance = cursor.fetchone()[0]
    print(f"Available balance: {balance}")

def get_balance(mobile_number):
    cursor.execute('SELECT balance FROM users WHERE mobile_number=%s', (mobile_number,))
    balance = cursor.fetchone()[0]
    return balance

key = Fernet.generate_key()
cipher_suite = Fernet(key)

def encrypt(num):
    num_str = str(num).zfill(16)
    cipher_text = cipher_suite.encrypt(num_str.encode())
    return cipher_text

def decrypt(encrypted_num):
    decrypted_text = cipher_suite.decrypt(encrypted_num).decode()
    return int(decrypted_text)
    
def copy_last_6_numbers(input_string):
    if len(input_string) < 6:
        return input_string
    last_6 = input_string[-6:]

    return last_6

def pay_mobile(sender_mobile):
    receiver_mobile = input("Enter receiver's mobile number: ")
    amount = int(input("Enter amount to pay: "))
    bal = get_balance(sender_mobile)
    if bal >= amount:
    
        sender_pin = input("Enter your PIN to confirm: ")

        cursor.execute('SELECT * FROM users WHERE mobile_number=%s AND pin=%s', (sender_mobile, sender_pin))
        sender = cursor.fetchone()

        if sender:
            cursor.execute('SELECT * FROM users WHERE mobile_number=%s', (receiver_mobile,))
            receiver = cursor.fetchone()
            if receiver:
                clear_screen()
                otp = generate_otp()
                encrypted = encrypt(otp)
                print("Encrypted OTP:", copy_last_6_numbers(encrypted))
                print("To decrypt the OTP Login to OTP Account")
                press_enter_to_continue()
                clear_screen()
                print("OTP Account Login")
                uname = input("Enter username: ")
                pword = input("Enter password: ")
                if verify_receiver_login(uname, pword):
                    print(f"Decrypted OTP for the transaction: {otp}")
                    press_enter_to_continue()
                    clear_screen()
                    print("Logout from OTP Account Successfull")
                    entered_otp = input("Enter OTP to confirm transaction: ")
                    if otp == entered_otp:
                        new_sender_balance = sender[2] - amount
                        new_receiver_balance = receiver[2] + amount
                        cursor.execute('''
                            UPDATE users
                            SET balance = %s
                            WHERE mobile_number = %s
                        ''', (new_sender_balance, sender_mobile))

                        cursor.execute('''
                            UPDATE users
                            SET balance = %s
                            WHERE mobile_number = %s
                        ''', (new_receiver_balance, receiver_mobile))

                        conn.commit()
                        clear_screen()
                        print("Transaction successful!")
                        show_balance(sender_mobile)
                        press_enter_to_continue()
                        return
                    else:
                        print("Invalid OTP. Transaction cancelled.")
                        press_enter_to_continue()
                        return
                else:
                    print("Invalid receiver's username or password.")
                    press_enter_to_continue()
                    return
            else:
                print("Receiver's mobile number not found.")
                press_enter_to_continue()
                return
        else:
            print("Invalid PIN.")
            press_enter_to_continue()
            return
    else:
        clear_screen
        print("Insufficient balance to complete transaction")
        press_enter_to_continue()

def verify_receiver_login(username, password):
    cursor.execute('SELECT * FROM users WHERE mobile_number=%s AND pin=%s', (username, password))
    return cursor.fetchone() is not None

def main():
    while True:
        clear_screen()
        print("\n===== Welcome to the UPI App =====")
        print("1. Login")
        print("2. Create a new user")
        print("3. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            login()
        elif choice == '2':
            create_user()
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid option. Please try again.")

    conn.close()

main()