import mysql.connector as sqlcon

mydb =  sqlcon.connect(host='localhost',user='user',passwd='root')
cursor = mydb.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS BANK;")
cursor.execute("USE BANK;")
cursor.execute("CREATE TABLE IF NOT EXISTS USERS(name varchar(30),passwd varchar(30),Balance varchar(30));")

cursor.execute("INSERT INTO USERS values('Vibhor','GOS123',300000),('Raghav','Raghav2587',40000);")
mydb.commit()

def GetBalance(username,password):
    cursor.execute("Select * from users;")
    userdata=cursor.fetchall()
    for data in userdata:
        if (data[0],data[1]) == (username,password):
            print(f"your balance is {data[2]}")
            break
    else:
        print("In correct details please try again: (type balance to check your balance)")


command=''
while command.lower() != 'quit':

    if command.lower() == 'balance':
        username = input("Username: ")
        password= input("Password: ")
        GetBalance(username,password)

    else:
        print("\nplease enter a valid command")

    command = input("> ").lower()

