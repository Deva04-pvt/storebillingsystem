import time

from sqlfunctions import *
from random import seed, choice, randint

Customer_Name = None
Customer_ID = None
Customer_bill = []
Grand_Total = 0
Turnover = 0

billdb = sql.connect(host="localhost", user="root", passwd=ObtainSqlPassword(), database="bills")
billcursor = billdb.cursor()


def CalculatePrice(rate, qty):
    price = rate * qty
    return price


def GenerateCustomerId():
    seed(time.time())
    global Customer_ID
    output_id = ""
    for i in range(3):
        char = choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        output_id += char
    part_two = randint(1000000, 9999999)
    output_id += str(part_two)
    for i in range(3):
        char = choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        output_id += char
    Customer_ID = output_id
    return output_id


def AddIntoBill(item_code):
    if Customer_bill is not None:
        for item in Customer_bill:
            if item_code == item[0]:
                return "Exists"
    mycursor.execute("SELECT item_code, item_name, rate FROM inventory WHERE item_code = %s", (item_code,))
    record = mycursor.fetchall()
    if record:
        record = record[0]
        record = list(record)
        price = record[2]
        item_list = record + ["1"] + [price]
        Customer_bill.append(item_list)
        return True
    else:
        return False


def ReturnBill():
    return Customer_bill


def DeleteFromBill(item_code):
    for item in Customer_bill:
        if item[0] == item_code:
            Customer_bill.remove(item)


def ClearBill():
    global Customer_bill
    Customer_bill = []


def CalculateTotal():
    global Customer_bill, Grand_Total
    Grand_Total = 0
    if Customer_bill:
        for item in Customer_bill:
            Grand_Total += float(item[4])
    return Grand_Total


def SetQuantity(quantity, item_code):
    for item in Customer_bill:
        if item[0] == item_code:
            item[3] = str(quantity)
            item[4] = CalculatePrice(qty=int(quantity), rate=float((item[2])))


def SetCustomerName(name):
    global Customer_Name
    Customer_Name = name


def WriteBill():
    global Turnover
    Turnover += Grand_Total
    mycursor.execute("INSERT INTO customername (name, customerid, total) VALUES (%s, %s, %s)",
                     (Customer_Name, Customer_ID, Grand_Total))
    mydb.commit()
    billcursor.execute(
        "CREATE TABLE " + str(
            Customer_ID) + "(serial_no INT AUTO_INCREMENT PRIMARY KEY, item_code VARCHAR(5) not null, item_name VARCHAR(50) not null, rate INT not null, qty INT NOT NULL, price INT NOT NULL)")
    for item in Customer_bill:
        item = tuple(item)
        billcursor.execute(
            "INSERT INTO " + str(Customer_ID) + f"(item_code, item_name, rate, qty, price) VALUES(%s, %s, %s, %s, %s)",
            (item[0], item[1], item[2], item[3], item[4]))
    billdb.commit()
    for item in Customer_bill:
        ReduceStocks(item[0], item[3])
    ResetBillAndItems()


def GetTurnover():
    return Turnover


def ResetBillAndItems():
    global Customer_bill, Customer_ID, Customer_Name, Grand_Total
    Customer_bill = []
    Customer_Name = None
    Customer_ID = None
    Grand_Total = 0


def GetBill(tablename):
    billcursor.execute("SELECT * FROM " + str(tablename))
    data = billcursor.fetchall()
    return data
