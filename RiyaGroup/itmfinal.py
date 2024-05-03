"""import mysql.connector as sqltor
import pandas as pd
import sys
from email.utils import parseaddr
global inp
inp='y'
global user
user='a'
mycon = sqltor.connect(host="localhost", user="root", password="riya@avanish2007", database="encryption")
if mycon.is_connected() == False:
    print("error in connecting to mysql")
else:
    print("successfully connected to mysql")
print()
cur = mycon.cursor()


def generate_key():
    shift = 3
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    return shifted_alphabet

def encrypt_message(message):
    shift = 3
    encrypted_message = ""
    for char in message:
        if char.isalpha():  
            shifted_char = chr(((ord(char) - ord('a' if char.islower() else 'A') + shift) % 26) + ord('a' if char.islower() else 'A'))
            encrypted_message += shifted_char
        else:
            encrypted_message += char
    return encrypted_message

def add_message():
    c1 = mycon.cursor()
    sender = input("Enter your name:")
    recipient = input("Enter receiver's name:")
    message = input("Message for the user:")
    key = generate_key()
    encrypted_message = encrypt_message(message)
    sql = "insert into messages(sender, recipient, message, encryption_key) values(%s, %s, %s, %s)"
    c1.execute(sql, (sender, recipient, encrypted_message, key))
    mycon.commit()
    print("Encrypted message stored successfully!")

def decrypt_message(encrypted_message):
    shift = 3
    decrypted_message = ""
    for char in encrypted_message:
        if char.isalpha():  
            shifted_char = chr(((ord(char) - ord('a' if char.islower() else 'A') - shift) % 26) + ord('a' if char.islower() else 'A'))
            decrypted_message += shifted_char
        elif char == ' ':
            decrypted_message += ' '
        else:
            decrypted_message += char
    return decrypted_message

def view_messagesreciever(user):
    c1 = mycon.cursor()
    sql = "SELECT sender, message, encryption_key FROM messages WHERE recipient = %s"
    c1.execute(sql, (user,))
    messages = c1.fetchall()
    print("Received messages:")
    for sender, encrypted_message, key in messages:
        decrypted_message = decrypt_message(encrypted_message)
        print(f"{sender}: {decrypted_message}")

def view_messagessender(user):
    c1 = mycon.cursor()
    sql = "SELECT recipient, message, encryption_key FROM messages WHERE sender = %s"
    c1.execute(sql, (user,))
    messages = c1.fetchall()
    print("Sent messages to:")
    for receiver, encrypted_message, key in messages:
        decrypted_message = decrypt_message(encrypted_message)
        print(f"{receiver}: {decrypted_message}")

while True:
    print("\n1. Send Message\n2. View Receiver Messages\n3. View Sender Messages\n4. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        add_message()
    
    elif choice == '2':
        user = input("Enter your name whose message you want to see: ")
        view_messagesreciever(user)

    elif choice == '3':
        user = input("Enter your name whose message you want to see: ")
        view_messagessender(user)
    
    elif choice == '4':
        break
    
    else:
        print("Invalid choice. Please try again.")
"""


import mysql.connector as sqltor
import pandas as pd
import random
import sys
from email.utils import parseaddr
"""
global inp
inp = 'y'
global user
user = 'a' """
mycon = sqltor.connect(host="localhost", user="root", password="riya@avanish2007", database="encryption_final")
if mycon.is_connected() == False:
    print("error in connecting to mysql")
else:
    print("successfully connected to mysql")
print()
cur = mycon.cursor()

def generate_key():
    shift = 3
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    return shifted_alphabet

def encrypt_message(message):
    shift = 3
    encrypted_message = ""
    for char in message:
        if char.isalpha():  
            shifted_char = chr(((ord(char) - ord('a' if char.islower() else 'A') + shift) % 26) + ord('a' if char.islower() else 'A'))
            encrypted_message += shifted_char
        else:
            encrypted_message += char
    return encrypted_message

def add_message():
    c1 = mycon.cursor()
    table_name = f"messages_{random.randint(1, 3)}"
    c1.execute(f'create table if not exists {table_name}(sender varchar(50), recipient varchar(50), message varchar(6000), encryption_key varchar(10000));')
    sender = input("Enter your name:")
    recipient = input("Enter receiver's name:")
    message = input("Message for the user:")
    key = generate_key()
    encrypted_message = encrypt_message(message)
    sql = f"insert into {table_name}(sender, recipient, message, encryption_key) values(%s, %s, %s, %s)"
    c1.execute(sql, (sender, recipient, encrypted_message, key))
    mycon.commit()
    print("Encrypted message stored successfully in  " f"{table_name}!")

def decrypt_message(encrypted_message):
    shift = 3
    decrypted_message = ""
    for char in encrypted_message:
        if char.isalpha():  
            shifted_char = chr(((ord(char) - ord('a' if char.islower() else 'A') - shift) % 26) + ord('a' if char.islower() else 'A'))
            decrypted_message += shifted_char
        elif char == ' ':
            decrypted_message += ' '
        else:
            decrypted_message += char
    return decrypted_message

def view_messagesreciever(user):
    c1 = mycon.cursor()
    for i in range(1, 4):
        table_name = f"messages_{i}"
        sql = f"SELECT sender, message, encryption_key FROM {table_name} WHERE recipient = %s"
        c1.execute(sql, (user,))
        messages = c1.fetchall()
        print(f"Received messages from table {table_name}:")
        for sender, encrypted_message, key in messages:
            decrypted_message = decrypt_message(encrypted_message)
            print(f"{sender}: {decrypted_message}")


def view_messagessender(user):
    c1 = mycon.cursor()
    for i in range(1, 4):
        table_name = f"messages_{i}"
        sql = f"SELECT recipient, message, encryption_key FROM {table_name} WHERE sender = %s"
        c1.execute(sql, (user,))
        messages = c1.fetchall()
        print(f"Sent messages to table {table_name}:")
        for recipient, encrypted_message, key in messages:
            decrypted_message = decrypt_message(encrypted_message)
            print(f"{recipient}: {decrypted_message}")

            
while True:
    print("\n1. Send Message\n2. View Receiver Messages\n3.View Sender Messages\n4. Exit")
    choice = input("Enter your choice: ")
    if choice == '1':
        add_message()
    elif choice == '2':
        user = input("Enter your reciver name whose message you want to see:")
        view_messagesreciever(user)
    elif choice == '3':
        user = input("Enter your sender name whose message you want to see:")
        view_messagessender(user)
    elif choice == '4':
        break
    else:
        print("Invalid choice. Please try again.")



    
