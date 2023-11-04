import mysql.connector as sql
from tkinter import *
from tkinter import messagebox

Icon = r"shop.ico"
Font5 = ("Helvetica", 16, "bold", "italic")
LoginPageTheme1 = "#bdfff6"
LoginPageTheme2 = "#e23c52"
TreeviewHeadingBackground1 = "#e23c52"


def ObtainSqlPassword():
    with open("passwd.txt", "r") as file:
        password = file.read()
        return password


def SetSqlPassword(passwd):
    with open("passwd.txt", "w") as file:
        file.write(passwd)


def MysqlSetup():
    try:
        mydb = sql.connect(host="localhost", user="root", passwd=ObtainSqlPassword())
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE IF NOT EXISTS BILLINGSYSTEM")
        mycursor.execute("CREATE DATABASE IF NOT EXISTS BILLS")
        mydb = sql.connect(host="localhost", user="root", passwd=ObtainSqlPassword(), database="billingsystem")
        mycursor = mydb.cursor()
        mycursor.execute(
            "CREATE TABLE IF NOT EXISTS logindata (username varchar(20) NOT NULL,password varchar(20) NOT NULL,usertype char(1) NOT NULL,signedin char(1) NOT NULL,primary_admin tinyint DEFAULT '0',PRIMARY KEY (username))")
        mycursor.execute("""CREATE TABLE IF NOT EXISTS activitylog (
      SERIAL_NO int NOT NULL AUTO_INCREMENT,
      USERNAME varchar(20) NOT NULL,
      DATE varchar(10) NOT NULL,
      LOGIN_TIME varchar(15) NOT NULL,
      LOGOUT_TIME varchar(15) NOT NULL,
      TURNOVER int DEFAULT NULL,
      PRIMARY KEY (SERIAL_NO)
    )""")
        mycursor.execute("""CREATE TABLE IF NOT EXISTS inventory (
      serial_no int NOT NULL AUTO_INCREMENT,
      item_code varchar(3) DEFAULT NULL,
      item_name varchar(50) DEFAULT NULL,
      rate varchar(20) NOT NULL,
      stocks int DEFAULT NULL,
      PRIMARY KEY (serial_no),
      UNIQUE KEY item_code (item_code)
    )""")
        mycursor.execute("""CREATE TABLE IF NOT EXISTS customername (
      name varchar(50) NOT NULL,
      customerid varchar(20) NOT NULL,
      time timestamp NULL DEFAULT CURRENT_TIMESTAMP,
      total varchar(30) DEFAULT NULL,
      PRIMARY KEY (customerid)
    )""")
    except sql.ProgrammingError:
        SqlSetupStartWindow = Tk()
        SqlSetupStartWindow.focus_force()
        SqlSetupStartWindow.title("Set MySQL Password")
        SqlSetupStartWindow.config(bg=LoginPageTheme1)
        window_width = 470
        window_height = 120
        screen_width = SqlSetupStartWindow.winfo_screenwidth()
        screen_height = SqlSetupStartWindow.winfo_screenheight()
        xCoordinate = int(screen_width / 2 - window_width / 2)
        yCoordinate = int(screen_height / 2 - window_height / 2)
        SqlSetupStartWindow.geometry(f'{window_width}x{window_height}+{xCoordinate}+{yCoordinate}')
        SqlSetupStartWindow.resizable(False, False)
        SqlSetupStartWindow.iconbitmap(Icon)

        Label(SqlSetupStartWindow, text="MySQL Password: ", font=Font5, bg=LoginPageTheme1,
              fg=TreeviewHeadingBackground1).place(x=5, y=20)
        NewUsername = Entry(SqlSetupStartWindow, font=Font5, relief=SOLID)
        NewUsername.place(x=205, y=20)

        ChangeButton = Button(SqlSetupStartWindow, text="Enter", font=Font5, bg=LoginPageTheme1,
                              activebackground=LoginPageTheme1,
                              fg=LoginPageTheme2, activeforeground=LoginPageTheme2, relief=RIDGE, bd=2,
                              command=lambda: (
                                  SetSqlPassword(NewUsername.get()), SqlSetupStartWindow.destroy(), MysqlSetup()))
        ChangeButton.place(x=182, y=70)
        messagebox.showinfo("Setup",
                            "It seems the application needs your correct Mysql password.Please enter it correctly")
        SqlSetupStartWindow.mainloop()


MysqlSetup()
