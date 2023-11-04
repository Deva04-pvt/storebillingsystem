import datetime
from mysqlsetup import *


def ObtainSqlPassword():
    with open("passwd.txt", "r") as filehandle:
        password = filehandle.read()
        return password


passwd = ObtainSqlPassword()
mydb = sql.connect(host="localhost", user="root", passwd=passwd, database="billingsystem")
mycursor = mydb.cursor()


def AddNewUser(username, password, admin, staysignedin, primary_admin=False):
    if admin:
        if primary_admin:
            if staysignedin == 1:
                mycursor.execute(
                    "INSERT INTO LOGINDATA(username, password, usertype, signedin, primary_admin) VALUES(%s, %s, %s, %s, %s)",
                    (username, password, "A", "Y", 1))
            else:
                mycursor.execute(
                    "INSERT INTO LOGINDATA(username, password, usertype, signedin, primary_admin) VALUES(%s, %s, %s, %s, %s)",
                    (username, password, "A", "N", 1))
        else:
            if staysignedin == 1:
                mycursor.execute("INSERT INTO LOGINDATA(username, password, usertype, signedin) VALUES(%s, %s, %s, %s)",
                                 (username, password, "A", "Y"))
            else:
                mycursor.execute("INSERT INTO LOGINDATA(username, password, usertype, signedin) VALUES(%s, %s, %s, %s)",
                                 (username, password, "A", "N"))
    else:
        if staysignedin == 1:
            mycursor.execute("INSERT INTO LOGINDATA(username, password, usertype, signedin) VALUES(%s, %s, %s, %s)",
                             (username, password, "E", "Y"))
        else:
            mycursor.execute("INSERT INTO LOGINDATA(username, password, usertype, signedin) VALUES(%s, %s, %s, %s)",
                             (username, password, "E", "N"))
    mydb.commit()


def GetUsers():
    mycursor.execute("SELECT username FROM logindata")
    users = mycursor.fetchall()
    users_list = []
    for item in users:
        users_list.append(item[0])
    return users_list


def ResetData(tablename):
    mycursor.execute("TRUNCATE TABLE " + tablename)
    mydb.commit()


def SetStaySignedIn(username, var):
    if var:
        mycursor.execute("UPDATE logindata SET signedin = %s WHERE signedin = %s", ("N", "Y"))
        mycursor.execute("UPDATE logindata SET signedin = %s WHERE username = %s", ("Y", username))
    else:
        mycursor.execute("UPDATE logindata SET signedin = %s WHERE username = %s", ("N", username))
    mydb.commit()


def CheckStocks(item_code, requested_stocks):
    mycursor.execute("select stocks FROM inventory WHERE item_code = %s", (item_code,))
    data = int(mycursor.fetchall()[0][0])
    if requested_stocks <= data:
        return True
    return False


def CheckSignedIn():
    mycursor.execute("SELECT username, signedin FROM logindata")
    data_tuple = mycursor.fetchall()
    for item in data_tuple:
        if item[1] == "Y":
            return item[0]


def GetActivity(username="None", date="None", month="None", year="None", hour="None"):
    query = "SELECT * FROM activitylog WHERE"
    insert_and = False
    if username != "None":
        query += f" username LIKE '%{username}%'"
        insert_and = True
    if date != "None":
        if insert_and:
            if len(date) == 1:
                query += f" AND date LIKE '%-0{date}'"
            else:
                query += f" AND date LIKE '%-{date}'"
        else:
            if len(date) == 1:
                query += f" date LIKE '%-0{date}'"
                insert_and = True
            else:
                query += f" date LIKE '%-{date}'"
                insert_and = True
    if month != "None":
        if insert_and:
            if len(month) == 1:
                query += f" AND date LIKE '%-0{month}-%'"
            else:
                query += f" AND date LIKE '%-{month}-%'"
        else:
            if len(month) == 1:
                query += f" date LIKE '%-0{month}-%'"
                insert_and = True
            else:
                query += f" date LIKE '%-{month}-%'"
                insert_and = True
    if year != "None":
        if insert_and:
            query += f" AND date like '{year}-%'"
        else:
            query += f" date like '{year}-%'"
            insert_and = True
    if hour != "None":
        if insert_and:
            if len(hour) == 1:
                query += f" AND login_time LIKE '0{hour}:%'"
            else:
                query += f" AND login_time LIKE '{hour}:%'"
        else:
            if len(hour) == 1:
                query += f" login_time LIKE '0{hour}:%'"
            else:
                query += f" login_time LIKE '{hour}:%'"
    print(query)
    mycursor.execute(query)
    records = mycursor.fetchall()
    return_records = []
    for item in records:
        single_record = list(item)
        single_record.pop(0)
        return_records.append(single_record)
    return return_records


def FetchItem(item_code):
    mycursor.execute("SELECT item_code, item_name, rate FROM inventory WHERE item_code = %s", (item_code,))
    records = mycursor.fetchall()
    return records


def CheckAdmin(username):
    mycursor.execute("SELECT usertype FROM logindata WHERE username = %s", (username,))
    usertype = mycursor.fetchall()[0][0]
    if usertype == "A":
        return True
    return False


def UpdateActivity(username, logintime, date, turnover=0):
    End_Time = str(datetime.datetime.now())
    logouttime = End_Time.split()[1].split(".")[0]
    mycursor.execute(
        f"INSERT INTO activitylog(username, date, login_time, logout_time, turnover) VALUES(%s, %s, %s, %s, {turnover})",
        (username, date, logintime, logouttime))
    mydb.commit()


def ReturnPassword(username):
    mycursor.execute("SELECT password FROM logindata WHERE username = %s", (username,))
    password_tuple = mycursor.fetchall()
    correct_password = ""
    for item in password_tuple:
        correct_password += item[0]
    return correct_password


def ChangeUsername(current_username, new_username):
    mycursor.execute("UPDATE logindata SET username = %s WHERE username = %s", (new_username, current_username))
    mycursor.execute("UPDATE activitylog SET username = %s WHERE username = %s", (new_username, current_username))
    mydb.commit()
    return True


def ChangePassword(username, old_password, new_password):
    correct_password = ReturnPassword(username)
    if old_password == correct_password:
        mycursor.execute("UPDATE logindata SET password = %s WHERE username = %s", (new_password, username))
        mydb.commit()
        return True
    else:
        return False


def CheckUniqueCode(code):
    mycursor.execute("SELECT item_code FROM inventory")
    list_of_codes = []
    for item in mycursor.fetchall():
        list_of_codes.append(item[0])
    if code not in list_of_codes:
        return True


def FetchAllItems():
    mycursor.execute("SELECT item_code, item_name, rate, stocks FROM inventory")
    records = mycursor.fetchall()
    return records


def FetchAllActivity():
    mycursor.execute("SELECT * FROM activitylog")
    records = mycursor.fetchall()
    return records


def FetchAllUsers():
    mycursor.execute("SELECT username, usertype FROM logindata")
    records = mycursor.fetchall()
    return records


def SearchUsers(search_element, search_criteria):
    if search_criteria == "Username":
        mycursor.execute(
            f"SELECT username,usertype FROM logindata WHERE username LIKE '%{search_element}%'")
        records = mycursor.fetchall()
        return records
    elif search_criteria == "Usertype":
        mycursor.execute(
            f"SELECT username,usertype FROM logindata WHERE usertype LIKE '%{search_element[0]}%'")
        records = mycursor.fetchall()
        return records


def DeleteUsers(usernames):
    passed_records = []
    failed_records = []
    for username in usernames:
        result = CheckIfPrimaryAdmin(username)
        if result:
            failed_records.append(username)
        else:
            passed_records.append(username)
    for username in passed_records:
        mycursor.execute("DELETE FROM logindata WHERE username = %s", (username,))
        mydb.commit()
    if not failed_records:
        return True
    else:
        return "ok", failed_records


def PromoteUser(username):
    user = username[0]
    mycursor.execute("SELECT usertype FROM logindata WHERE username = %s", (user,))
    type_of_user = mycursor.fetchall()[0][0]
    if type_of_user == "E":
        mycursor.execute("UPDATE logindata SET usertype = 'A' WHERE username = %s", (user,))
        return True
    else:
        return False


def DePromoteUser(username):
    user = username[0]
    mycursor.execute("SELECT usertype FROM logindata WHERE username = %s", (user,))
    type_of_user = mycursor.fetchall()[0][0]
    if type_of_user == "A":
        mycursor.execute("UPDATE logindata SET usertype = 'E' WHERE username = %s", (user,))
        return True
    else:
        return False


def CheckIfPrimaryAdmin(username):
    mycursor.execute("SELECT primary_admin FROM logindata WHERE username = %s", (username,))
    result = mycursor.fetchall()[0][0]
    if result == 1:
        return True
    return False


def AddItem(code, name, rate, stocks):
    mycursor.execute(f"INSERT INTO inventory(item_code, item_name, rate, stocks) VALUES (%s, %s, %s, {stocks})",
                     (code, name, rate))
    mydb.commit()


def UpdateItemByName(current_itemcode, new_name):
    mycursor.execute(f"UPDATE inventory SET item_name = %s WHERE item_code = %s", (new_name, current_itemcode))
    mydb.commit()
    return True


def UpdateItemByCode(current_itemcode, new_code):
    mycursor.execute(f"UPDATE inventory SET item_code = %s WHERE item_code = %s", (new_code, current_itemcode))
    mydb.commit()
    return True


def UpdateItemByRate(current_itemcode, new_rate):
    mycursor.execute(f"UPDATE inventory SET rate = %s WHERE item_code = %s", (new_rate, current_itemcode))
    mydb.commit()
    return True


def UpdateItemByStocks(current_itemcode, new_stocks):
    mycursor.execute(f"UPDATE inventory SET stocks = %s WHERE item_code = %s", (new_stocks, current_itemcode))
    mydb.commit()
    return True


def SearchItem(value, search_criteria):
    if search_criteria == "Item Code":
        mycursor.execute(f"SELECT * FROM inventory WHERE item_code LIKE '%{value}%'")
    elif search_criteria == "Item Name":
        mycursor.execute(f"SELECT * FROM inventory WHERE item_name LIKE '%{value}%'")
    elif search_criteria == "Rate":
        mycursor.execute(f"SELECT * FROM inventory WHERE rate LIKE '%{value}%'")
    data = mycursor.fetchall()
    return data


def ReduceStocks(item_code, stocks_value):
    mycursor.execute("UPDATE inventory SET stocks = stocks - %s WHERE item_code = %s", (stocks_value, item_code))
    mydb.commit()


if __name__ == "__main__":
    ResetData("logindata")
    ResetData("activitylog")
    ResetData("inventory")
    ResetData("customername")
