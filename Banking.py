import numpy as np
import mysql.connector as con

sqlcon = con.connect(host="localhost", user="root", passwd="9978", database="BANK")
mycursor = sqlcon.cursor()
if sqlcon.is_connected():
    print("Welcome to the Bank")

# Main Table ---------------------------------------
#mycursor.execute("""
#CREATE TABLE BANKING(
    #Accno INT(8),
    #Name CHAR(100),
    #Acctype CHAR(20),
    #Age INT(3),
    #Gender CHAR(1),
    #Date VARCHAR(20),
    #Mobile VARCHAR(200),
    #Balance INT(100),
    #City CHAR(60)
#)
#""")

#sqlcon.commit()


# ---------------------------------------------------------
# MAIN MENU
# ---------------------------------------------------------

def mainmenu():
    print("Choose what you want to perform")
    print("1. Create New Account")
    print("2. Modify Your Account")
    print("3. Deposit your money")
    print("4. Withdraw Money")
    print("5. Transfer Money")
    print("6. Show your current Balance")
    print("7. Display Account Holders List")
    print("8. Search your Account")
    print("9. Close your Account")
    print("10. EXIT")

# ---------------------------------------------------------
# CREATE NEW ACCOUNT
# ---------------------------------------------------------

def adduser():
    Name = input("Enter your Name---")
    print("1. Current Account\n2. Savings Account\n3. Salary Account\n4. Fixed Deposit Account\n5. NRI Account")
    n = input("Choose your Account Type---")
    
    types = {
        "1": "Current Acc",
        "2": "Savings Acc",
        "3": "Salary Acc",
        "4": "Fixed Deposit Acc",
        "5": "NRI Acc"
    }
    
    acctyp = types.get(n, "Savings Acc")
    print("Your Account Type is", acctyp)

    Date = input("Enter today's Date (YYYY-MM-DD)---")
    mob = input("Enter your Mobile Number---")
    age = input("Enter your Age---")
    gen = input("Enter your Gender (F/M)---")
    city = input("Enter your city---")
    
    acc = np.random.randint(15000000, 99999999, 1)[0]
    print("Your Account Number is", acc)
    
    Accno = input("Enter the Account Number provided above---")
    bal = 0
    
    n1 = input("Do you want to deposit money now (Y/N)---")
    if n1.lower() == "y":
        bal = int(input("Enter the amount you want to deposit---"))

    add = "INSERT INTO BANKING VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    data = (Accno, Name, acctyp, age, gen, Date, mob, bal, city)
    mycursor.execute(add, data)
    sqlcon.commit()

# ---------------------------------------------------------
# MODIFY ACCOUNT
# ---------------------------------------------------------

def modacc():
    no = input("Enter your Account Number---")
    print("1. Your Acctype\n2. Your Age\n3. Your Mobile number\n4. Your City")
    m = input("What would you like to modify?---")

    if m in ("1", "Acctype", "acctype"):
        newacc = input("Enter your new Acctype---")
        rec = "UPDATE BANKING SET Acctype=%s WHERE Accno=%s"
        mycursor.execute(rec, (newacc, no))
        sqlcon.commit()

    elif m in ("2", "Age", "age"):
        age1 = input("Enter new age--")
        rec = "UPDATE BANKING SET Age=%s WHERE Accno=%s"
        mycursor.execute(rec, (age1, no))
        sqlcon.commit()

    elif m in ("3", "Mobile", "mobile", "mobile number"):
        mob1 = input("Enter new Mobile number--")
        rec = "UPDATE BANKING SET Mobile=%s WHERE Accno=%s"
        mycursor.execute(rec, (mob1, no))
        sqlcon.commit()

    elif m in ("4", "City", "city"):
        cit = input("Enter new city--")
        rec = "UPDATE BANKING SET City=%s WHERE Accno=%s"
        mycursor.execute(rec, (cit, no))
        sqlcon.commit()

# ---------------------------------------------------------
# DEPOSIT MONEY
# ---------------------------------------------------------

def dep_money():
    no = input("Enter your Account Number---")
    dep = int(input("Enter Amount to deposit---"))
    
    mycursor.execute("SELECT Balance FROM BANKING WHERE Accno=%s", (no,))
    bal = mycursor.fetchone()

    if bal:
        new_bal = bal[0] + dep
        print("Previous Balance:", bal[0])
        print("Updated Balance:", new_bal)
        mycursor.execute("UPDATE BANKING SET Balance=%s WHERE Accno=%s", (new_bal, no))
        sqlcon.commit()

# ---------------------------------------------------------
# WITHDRAW MONEY
# ---------------------------------------------------------

def with_money():
    no = input("Enter your Account Number---")
    withdraw = int(input("Enter Amount to withdraw---"))
    
    mycursor.execute("SELECT Balance FROM BANKING WHERE Accno=%s", (no,))
    bal = mycursor.fetchone()

    if bal:
        new_bal = bal[0] - withdraw
        print("Updated Balance:", new_bal)
        mycursor.execute("UPDATE BANKING SET Balance=%s WHERE Accno=%s", (new_bal, no))
        sqlcon.commit()

# ---------------------------------------------------------
# TRANSFER MONEY
# ---------------------------------------------------------

def trans():
    no = input("Your Account Number---")
    no2 = input("Receiver Account Number---")
    mon = int(input("Amount to Transfer---"))

    # Deduct from sender
    mycursor.execute("SELECT Balance FROM BANKING WHERE Accno=%s", (no,))
    bal = mycursor.fetchone()
    if bal:
        new_bal = bal[0] - mon
        mycursor.execute("UPDATE BANKING SET Balance=%s WHERE Accno=%s", (new_bal, no))
        sqlcon.commit()

    # Add to receiver
    mycursor.execute("SELECT Balance FROM BANKING WHERE Accno=%s", (no2,))
    bal2 = mycursor.fetchone()
    if bal2:
        new_bal2 = bal2[0] + mon
        mycursor.execute("UPDATE BANKING SET Balance=%s WHERE Accno=%s", (new_bal2, no2))
        sqlcon.commit()

# ---------------------------------------------------------
# CURRENT BALANCE
# ---------------------------------------------------------

def curbal():
    no = input("Enter your Account Number---")
    mycursor.execute("SELECT ACCNO, NAME, BALANCE FROM BANKING WHERE ACCNO=%s", (no,))
    data = mycursor.fetchone()
    
    if data:
        print("Account Number:", data[0])
        print("Name:", data[1])
        print("Balance:", data[2])

# ---------------------------------------------------------
# ACCOUNT HOLDER NAME
# ---------------------------------------------------------

def acchol():
    no = input("Enter Account Number---")
    mycursor.execute("SELECT NAME FROM BANKING WHERE ACCNO=%s", (no,))
    data = mycursor.fetchone()
    if data:
        print("Account Holder:", data[0])

# ---------------------------------------------------------
# SEARCH
# ---------------------------------------------------------

def search():
    print("1. By Name\n2. By Account Type\n3. By Account Number\n4. By City")
    n = int(input("Enter your option---"))

    if n == 1:
        name = input("Enter Name---")
        mycursor.execute("SELECT * FROM BANKING WHERE NAME LIKE %s", ("%" + name + "%",))
        print(mycursor.fetchall())

    elif n == 2:
        print("1.Current 2.Savings 3.Salary 4.Fixed 5.NRI")
        idx = int(input("Choose Type---"))
        types = ["Current Acc", "Savings Acc", "Salary Acc", "Fixed Deposit Acc", "NRI Acc"]
        acctyp = types[idx - 1]
        mycursor.execute("SELECT * FROM BANKING WHERE Acctype=%s", (acctyp,))
        print(mycursor.fetchall())

    elif n == 3:
        acc = input("Enter Account Number---")
        mycursor.execute("SELECT * FROM BANKING WHERE Accno=%s", (acc,))
        print(mycursor.fetchall())

    elif n == 4:
        city = input("Enter City---")
        mycursor.execute("SELECT * FROM BANKING WHERE City LIKE %s", ("%" + city + "%",))
        print(mycursor.fetchall())

# ---------------------------------------------------------
# DELETE ACCOUNT
# ---------------------------------------------------------

def delete():
    n = input("Enter Account Number---")
    mycursor.execute("DELETE FROM BANKING WHERE Accno=%s", (n,))
    sqlcon.commit()
    print("Account Deleted Successfully!")

# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------

while True:
    mainmenu()
    opt = int(input("Enter your Choice (1-10)---"))
    
    if opt == 1: adduser()
    elif opt == 2: modacc()
    elif opt == 3: dep_money()
    elif opt == 4: with_money()
    elif opt == 5: trans()
    elif opt == 6: curbal()
    elif opt == 7: acchol()
    elif opt == 8: search()
    elif opt == 9: delete()
    elif opt == 10:
        print("Have a nice day!")
        break

mycursor.close()
sqlcon.close()
