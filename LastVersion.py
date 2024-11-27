import random
import mysql.connector as sqlcon

mydb = sqlcon.connect(host="localhost", user="user", passwd="root")
cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS Railway")
cursor.execute("USE Railway")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS RailwayTickets (
        pnr VARCHAR(11) PRIMARY KEY,
        name VARCHAR(20) NOT NULL,
        TrainNo VARCHAR(20),
        date VARCHAR(10),
        contact VARCHAR(15)
    )
""")

def print_menu():
    print("""WELCOME TO RAILWAY TICKET BOOKING SIMULATOR

                TO BOOK A TICKET TYPE "BOOK"
                TO CANCEL A TICKET TYPE "CANCEL"
                TO CHECK YOUR RESERVATION TYPE "CHECK"
                TO END THE PROGRAM TYPE "QUIT"
                TO REPEAT THIS DIALOG BOX TYPE "HELP"

                NOTE: ALL THESE ABOVE COMMANDS MUST BE TYPED at the '>' symbol not in between another process
                      Please enter the values appropriately for the smoothest experience""")


def TicketGenerator(cursor_obj, mydb_obj, name, TrainNo, date, contact):
    cursor_obj.execute("Select PNR from RailwayTickets")
    used = cursor_obj.fetchall()
    print(used)
    pnr = f"PNR{random.randint(4000000, 9999999)}"
    while (f'{pnr}',) in used:
        pnr = "PNR" + str(random.randint(4000000, 9999999))
    # mydb.free_result()
    try:
        cursor_obj.execute(
            f"INSERT INTO RailwayTickets (PNR, name, TrainNo, date, contact) VALUES ('{pnr}', '{name}', '{TrainNo}', '{date}', '{contact}');")

    except sqlcon.Error as err:
        print("Something went wrong: {}".format(err))

    mydb_obj.commit()

    return pnr


def cancel_ticket(cursor_obj, mydb_obj, pnr):
    cursor_obj.execute("Select * from RailwayTickets")
    alltickets = cursor_obj.fetchall()
    for ticket in alltickets:
        if ticket[0] == pnr:
            cursor_obj.execute(f"DELETE FROM RailwayTickets where pnr='{pnr}' ;")
            mydb_obj.commit()
            print("TICKET CANCELLED\n")

    else:
        print("This Ticket does not exist please check your pnr no and try again.")


def ticket_checker(cursor_obj, pnr):
    cursor_obj.execute("Select * from RailwayTickets")
    alltickets = cursor_obj.fetchall()
    for ticket in alltickets:
        if ticket[0] == pnr:
            print(f"""
                PNR no: {ticket[0]}
                Name: {ticket[1]}
                TRAIN no: {ticket[2]}
                DATE: {ticket[3]}
                CONTACT: {ticket[4]}""")
            break
    else:
        print("Given PNR Does not exist, "
              "Please check the number you have entered and avoid any spaces.")


def DateEntry():
    date = ''
    while True:
        i = 1
        try:
            date = input("date of travel (dd/mm/yy): ")
            if len(date) != 8:
                raise ValueError

            for char in date:
                if i % 3 != 0:
                    int(char)
                    i += 1
                elif char == '/':
                    i += 1
                else:
                    raise ValueError

            else:
                break
        except ValueError:
            print("Please enter a Valid Date: \n")

    return date


####
# MAIN PROGRAM STARTS HERE

print_menu()
command = input("> ")

while command.lower() != "quit":

    if command.lower() == "book":
        while True:
            name = input("name: ")
            if len(name)<=50:
                break
            else:
                print("enter name less than 50 char long\n")

        while True:
            try:
                TrainNo = int(input("TrainNo: "))
                break
            except ValueError:
                print("Please enter a number \n")

        date=DateEntry()

        contact = input("contact number:(phno)  ")
        print(f"Your PNR No. is: {TicketGenerator(cursor, mydb, name, TrainNo, date, contact)}")
        print(" Do make sure to REMEMBER IT ")

    elif command.lower() == "cancel":
        your_pnr = input("ENTER THE PNR of the ticket you want to cancel: ")
        cancel_ticket(cursor, mydb, your_pnr)


    elif command.lower() == "check":
        your_pnr = input("Enter your pnr: ")
        ticket_checker(cursor, your_pnr.upper())

    elif command.lower() == "help":
        print_menu()
    else:
        print("please enter a valid command (type 'help' for more info)")

    command = input("> ")


#USER HAS DECIDED TO QUIT
command = input("DO YOU WISH TO DELETE THE DATA:(Y/N) ")

if command.lower() == "y":
    command = input("ARE YOU SURE YOU WANT TO PERMANENTLY DELETE THE DATA"
                    "YOU WILL NOT BE ABLE TO RETRIEVE THIS DATA AGAIN:(Y/N) ")
    if command.lower() == "y":
        cursor.execute("DROP DATABASE Railway")
        print("ALL DATA HAS BEEN DELETED")
    else:
        print("DATA NOT DELETED")

if command.lower() != "y":
    print("""YOUR DATA IS STILL SAVED AND CAN BE ACCESSED BY SIMPLY RERUNNING THE PROGRAM""")

print("\nTHANKS FOR USING RAILWAY TICKET BOOKING SIMULATOR")