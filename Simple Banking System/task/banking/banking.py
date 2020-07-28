import random
import sqlite3
from math import ceil
database = r"C:\Users\Ishwar\PycharmProjects\Simple Banking System\Simple Banking System\task\card.s3db"
connection = sqlite3.connect(database)
cursor = connection.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS card (
        id INTEGER NULL,
        number TEXT NULL,
        pin TEXT NULL,
        balance INTEGER DEFAULT 0
    )
    """)
connection.commit()


def add_database(card_number, card_pin):
    cursor.execute(
        "SELECT COUNT(number) FROM card"
    )
    serial = int(cursor.fetchone()[0])
    cursor.execute(
        f'INSERT INTO card VALUES ({serial + 1}, {str(card_number)}, {str(card_pin)}, 0)'
    )
    connection.commit()


def menu_control(menu_option):
    if menu_option == 1:
        print("\nYour card has been created")
        create_acc()
    elif menu_option == 2:
        card = input("\nEnter your card number:\n")
        pin = input("Enter your PIN:\n")

        cursor.execute(f'SELECT number, pin, balance FROM card WHERE number = {card}')
        query = cursor.fetchone()
        if query is not None:
            if card == str(query[0]) and pin == str(query[1]):
                print("\nYou have successfully logged in!\n")
                log_in(query[0], query[1])
            else:
                print("\nWrong card number or PIN!\n")
        else:
            print("\nWrong card number or PIN!\n")
    elif menu_option == 0:
        print("\nBye!")
        exit()


def luhn(initial_number):
    num = list(initial_number)
    for i in range(0, 15, 2):
        num[i] = str(int(num[i]) * 2)
    for j in num:
        if int(j) > 9:
            num[num.index(j)] = str(int(j) - 9)
    addition = 0
    for i in num:
        addition += int(i)
    return str((ceil(addition / 10) * 10) - addition)


def create_acc():
    issuer_id_num = '400000'
    customer_acc_num = str(random.randrange(100000000, 999999999))
    checksum = luhn(issuer_id_num + customer_acc_num)
    card_num = (issuer_id_num + customer_acc_num + checksum)
    card_pin = (random.randint(1000, 9999))
    add_database(card_num, card_pin)
    print(f"Your card number:\n{card_num}\nYour card PIN:\n{card_pin}\n")


def log_in(card, pin):
    log_menu = int(input("1. Balance\n"
                         "2. Add income\n"
                         "3. Do transfer\n"
                         "4. Close account\n"
                         "5. Log out\n"
                         "0. Exit\n"))
    if log_menu == 1:
        cursor.execute(f'SELECT number, pin, balance FROM card WHERE number = {card}')
        query = cursor.fetchone()
        print(f"\nBalance: $ {query[2]}\n")
        log_in(card, pin)
    elif log_menu == 2:
        income = int(input("Enter income:\n"))
        cursor.execute(f'UPDATE card SET balance = balance + {income} WHERE number = {card}')
        connection.commit()
        print("Income was added!")
        log_in(card, pin)

    elif log_menu == 3:
        transfer_number = input("Transfer\nEnter card number:\n")
        if transfer_number.startswith('400000'):
            if transfer_number[15] == luhn(transfer_number[0: 15]):
                cursor.execute(f'SELECT number, pin, balance FROM card WHERE number = {transfer_number}')
                query = cursor.fetchone()
                print(query)
                if transfer_number == query[0]:
                    amount = int(input("Enter how much money you want to transfer:\n"))
                    cursor.execute(f'SELECT balance FROM card WHERE number = {card}')
                    balance = cursor.fetchone()
                    if amount <= balance[0]:
                        cursor.execute(f'UPDATE card SET balance = balance - {amount} WHERE number = {card}')
                        cursor.execute(f'UPDATE card SET balance = balance + {amount} WHERE number = {transfer_number}')
                        connection.commit()
                        print("Success!")
                    else:
                        print("Not enough money!")
                else:
                    print("Such card does not exist!")
            else:
                print("Probably you made mistake in the card number.\nPlease try again!")
        else:
            print("Such card does not exist")
        log_in(card, pin)

    elif log_menu == 4:
        cursor.execute(f'DELETE FROM card WHERE number = {card}')
        connection.commit()
        print("The account has been closed!")
        init()

    elif log_menu == 5:
        print("\nYou have successfully logged out!\n")
        init()
    elif log_menu == 0:
        print("\nBye!")
        exit()
    else:
        print("Wrong option!")
        log_in(card, pin)


def init():
    menu = int(input("1. Create an account\n2. Log into account\n0. Exit\n"))
    menu_control(menu)


while True:
    init()
