from bill import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import qrcode
from PIL import ImageTk

Year = int(str(datetime.datetime.now()).split()[0].split("-")[0])
Icon = r"shop.ico"
Font1 = ("Georgia", 40, "bold", "italic")
Font2 = ("Georgia", 25, "bold", "italic")
Font3 = ("Helvetica", 20, "bold", "italic")
Font4 = ("Helvetica", 15, "bold")
Font5 = ("Helvetica", 16, "bold", "italic")
Font6 = ("Verdana", 18, "italic")
Font7 = ("Verdana", 16, "italic")
LoginPageTheme1 = "#bdfff6"
LoginPageTheme2 = "#e23c52"
LoginEntryTheme = "#f5f5f5"
BillingFrameTheme = "#bdfff6"
SelectionBackground1 = "#6f8faf"
SelectionBackground2 = "#00154f"
SelectionBackground3 = '#008080'
ActivityLogFrameTheme = '#a7c7e7'
ManageUsersFrameTheme = "#40b5ad"
TreeviewBackgroundTheme1 = "#f88379"
TreeviewForegroundTheme1 = "#000000"
TreeviewBackgroundTheme2 = "#c075b7"
TreeviewForegroundTheme2 = "#000000"
TreeviewBackgroundTheme3 = "#AAFF00"
TreeviewForegroundTheme3 = "#000000"
TreeviewHeadingBackground1 = "#e23c52"
TreeviewHeadingForeground1 = "#f5f5f5"
TreeviewHeadingBackground2 = "#104c91"
TreeviewHeadingForeground2 = "#fffff0"
TreeviewHeadingBackground3 = "#DFFF00"
TreeviewHeadingForeground3 = "#000000"
# variables
CurrentUser = None
LoggedIn = False
ActivityUpdatable = False
# Frames
BillingFrame = Frame
ActivityLogFrame = Frame
ActivityTree = ttk.Treeview
ManageUsersFrame = Frame
InventoryFrame = Frame
ViewBillFrame = Frame
CurrentTopFrame = Frame
PreviousTopFrame = Frame
Start_Time = ""
End_Time = ""
InventoryTree = ttk.Treeview


def DestroyWindow(window_name):
    window_name.destroy()


def AddUserBtn(username, window_name, staysignedin, password="Emp@000", Admin="Employee"):
    global CurrentUser, LoggedIn
    variable = messagebox.askyesno("Login", "Do you wish to create a new account with the given data?")
    if variable:
        Eligible = EligibilityCheck(username, password)
        if Eligible:
            if Admin == "Employee":
                AddNewUser(username, password, False, staysignedin)
            else:
                AddNewUser(username, password, True, staysignedin)
            if password == "Emp@000":
                messagebox.showinfo("Login", "Account created successfully with default password 'Emp@000'")
            else:
                messagebox.showinfo("Login", "Account created successfully")
            if window_name is not None:
                DestroyWindow(window_name)
                CurrentUser = username
                LoggedIn = True


def LoginButton(username, password, window_name, staysignedin):
    global CurrentUser, LoggedIn, ActivityUpdatable
    ExistingUsers = GetUsers()
    if username in ExistingUsers:
        correct_password = ReturnPassword(username)
        if password == correct_password:
            CurrentUser = username
            LoggedIn = True
            if staysignedin == 1:
                SetStaySignedIn(username, True)
            else:
                SetStaySignedIn(username, False)
            messagebox.showinfo("Login", "Login Successful!")
            ActivityUpdatable = True
            DestroyWindow(window_name)
        else:
            messagebox.showerror("Login", "Incorrect Password!")
    else:
        messagebox.showerror("Login", "Username Not Found!")


def EligibilityCheck(username="", password="", OnlyCheckPass=False, OnlyCheckUsername=False):
    username_ok = False
    if not OnlyCheckPass:
        ExistingUsers = GetUsers()
        if 16 >= len(username) >= 1:
            if username not in ExistingUsers:
                username_ok = True
            else:
                messagebox.showerror("Add User", "Username already taken")
        else:
            messagebox.showerror("Add User", "Username should be within 1 and 16 characters")
    else:
        username_ok = True
    if username_ok:
        if not OnlyCheckUsername:
            if 20 >= len(password) >= 6:
                special_char = 0
                uppercase = 0
                for i in password:
                    if i in "1234567890!@#$%^&*":
                        special_char += 1
                    elif i.isupper():
                        uppercase += 1
                if special_char != 0:
                    if uppercase != 0:
                        return True
                    else:
                        messagebox.showerror("Add User", "Password should contain at least one uppercase character")
                else:
                    messagebox.showerror("Add User", "Password should contain at least one number or special character")
            else:
                messagebox.showerror("Add User", "Password should be within 6 and 20 characters")
        else:
            return True


def FirstWindowCreateButton(username, password, admin, window_name):
    global CurrentUser, LoggedIn, ActivityUpdatable
    Eligible = EligibilityCheck(username, password)
    if Eligible:
        AddNewUser(username, password, admin, False, primary_admin=True)
        messagebox.showinfo("Account", "First Administrative Account Created Successfully!")
        CurrentUser = username
        LoggedIn = True
        ActivityUpdatable = True
        DestroyWindow(window_name)


def show_password(widgets, variable):
    for widget in widgets:
        if variable.get() == 1:
            widget.config(show="")
        elif variable.get() == 0:
            widget.config(show="*")


def ClearTreeview(TreeviewName):
    for item in TreeviewName.get_children():
        TreeviewName.delete(item)


def CreateFirstWindow():
    FirstWindow = Tk()
    FirstWindow.title("Welcome")
    FirstWindow.configure(bg=LoginPageTheme1)
    window_width = 620
    window_height = 500
    screen_width = FirstWindow.winfo_screenwidth()
    screen_height = FirstWindow.winfo_screenheight()
    xCoordinate = int(screen_width / 2 - window_width / 2)
    yCoordinate = int(screen_height / 2 - window_height / 2)
    FirstWindow.geometry(f'{window_width}x{window_height}+{xCoordinate}+{yCoordinate}')
    FirstWindow.resizable(False, False)
    FirstWindow.iconbitmap(Icon)

    Label(FirstWindow, text="Create Admin Account", font=Font1, relief=SOLID, bg=LoginPageTheme1, bd=4,
          fg=LoginPageTheme2).place(relx=0.5, rely=0.0, anchor="n")  # Placed at the top-center
    Label(FirstWindow, text="Username: ", font=Font2, bg=LoginPageTheme1, fg=LoginPageTheme2).place(relx=0.08,
                                                                                                    rely=0.31)
    Label(FirstWindow, text="Password: ", font=Font2, bg=LoginPageTheme1, fg=LoginPageTheme2).place(relx=0.08,
                                                                                                    rely=0.46)

    UsernameEntry = Entry(FirstWindow, relief=SOLID, font=Font3, bd=2, bg=LoginEntryTheme)
    UsernameEntry.place(relx=0.4, rely=0.32)  # Adjusted relative coordinates
    PasswordEntry = Entry(FirstWindow, relief=SOLID, font=Font3, bd=2, show="*", bg=LoginEntryTheme)
    PasswordEntry.place(relx=0.4, rely=0.48)  # Adjusted relative coordinates

    ShowPasswordVar = IntVar()
    ShowPasswordButton = Checkbutton(FirstWindow, text="Show Password", font=Font4, bg=LoginPageTheme1,
                                     activebackground=LoginPageTheme1, variable=ShowPasswordVar,
                                     command=lambda: show_password((PasswordEntry,), ShowPasswordVar),
                                     selectcolor=LoginEntryTheme, fg=LoginPageTheme2, activeforeground=LoginPageTheme2)
    ShowPasswordButton.place(relx=0.4, rely=0.58)  # Adjusted relative coordinates

    CreateButton = Button(FirstWindow, font=Font2, text="Create", bg=LoginPageTheme1, relief=RIDGE, bd=3,
                          activebackground=LoginPageTheme1, fg=LoginPageTheme2,
                          command=lambda: FirstWindowCreateButton(UsernameEntry.get(), PasswordEntry.get(), True,
                                                                  FirstWindow), activeforeground=LoginPageTheme2)
    CreateButton.place(relx=0.4, rely=0.68)  # Adjusted relative coordinates

    FirstWindow.mainloop()


from tkinter import *


def CreateLoginWindow():
    global CurrentUser, LoggedIn, ActivityUpdatable
    LoginWindow = Tk()
    LoginWindow.title("Welcome")
    LoginWindow.configure(bg=LoginPageTheme1)
    window_width = 620
    window_height = 500
    screen_width = LoginWindow.winfo_screenwidth()
    screen_height = LoginWindow.winfo_screenheight()

    x = (screen_width - window_width) / 2
    y = (screen_height - window_height) / 2

    # Set the window position
    LoginWindow.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
    LoginWindow.resizable(False, False)
    LoginWindow.iconbitmap(Icon)

    Label(LoginWindow, text="Login Portal", font=Font1, relief=SOLID, bg=LoginPageTheme1, bd=4, anchor=CENTER, width=18,
          fg=LoginPageTheme2).place(relx=0.5, rely=0.0, anchor="n")
    Label(LoginWindow, text="Username: ", font=Font2, bg=LoginPageTheme1, fg=LoginPageTheme2).place(relx=0.1, rely=0.28)
    Label(LoginWindow, text="Password: ", font=Font2, bg=LoginPageTheme1, fg=LoginPageTheme2).place(relx=0.1, rely=0.44)

    UsernameEntry = Entry(LoginWindow, relief=SOLID, font=Font3, bd=2, bg=LoginEntryTheme)
    UsernameEntry.place(relx=0.42, rely=0.32)
    PasswordEntry = Entry(LoginWindow, relief=SOLID, font=Font3, bd=2, show="*", bg=LoginEntryTheme)
    PasswordEntry.place(relx=0.42, rely=0.48)

    ShowPasswordVar = IntVar()
    ShowPasswordButton = Checkbutton(LoginWindow, text="Show Password", font=Font4, bg=LoginPageTheme1,
                                     activebackground=LoginPageTheme1, variable=ShowPasswordVar, fg=LoginPageTheme2,
                                     command=lambda: show_password((PasswordEntry,), ShowPasswordVar),
                                     activeforeground=LoginPageTheme2, selectcolor=LoginEntryTheme)
    ShowPasswordButton.place(relx=0.42, rely=0.58)

    StaySignedInVar = IntVar()
    StaySignedInButton = Checkbutton(LoginWindow, text="Stay Signed In", font=Font4, bg=LoginPageTheme1,
                                     activebackground=LoginPageTheme1, variable=StaySignedInVar, fg=LoginPageTheme2,
                                     selectcolor=LoginEntryTheme, activeforeground=LoginPageTheme2)
    StaySignedInButton.place(relx=0.42, rely=0.68)

    LoginBtn = Button(LoginWindow, font=Font2, text="Login", bg=LoginPageTheme1, relief=RIDGE, bd=3,
                      activebackground=LoginPageTheme1, fg=LoginPageTheme2,
                      command=lambda: LoginButton(UsernameEntry.get(), PasswordEntry.get(), LoginWindow,
                                                  StaySignedInVar.get()), activeforeground=LoginPageTheme2)
    LoginBtn.place(relx=0.27, rely=0.8)
    AddNewUserBtn = Button(LoginWindow, font=Font2, text="Create", bg=LoginPageTheme1, relief=RIDGE, bd=3,
                           activebackground=LoginPageTheme1, fg=LoginPageTheme2,
                           command=lambda: AddUserBtn(UsernameEntry.get(), LoginWindow, StaySignedInVar.get(),
                                                      Admin="Employee", password=PasswordEntry.get()),
                           activeforeground=LoginPageTheme2)
    AddNewUserBtn.place(relx=0.57, rely=0.8)

    SignedInUser = CheckSignedIn()
    if SignedInUser:
        variable = messagebox.askyesno("Login", SignedInUser + " is already Signed In. Do you wish to proceed?")
        if variable:
            CurrentUser = SignedInUser
            LoggedIn = True
            ActivityUpdatable = True
            DestroyWindow(LoginWindow)
        else:
            SetStaySignedIn(SignedInUser, False)
    LoginWindow.mainloop()


def CreateMainWindow():
    global BillingFrame, ActivityLogFrame, ManageUsersFrame, InventoryFrame, ViewBillFrame, Start_Time
    if LoggedIn:
        Current_time = datetime.datetime.now()
        Start_Time = str(Current_time)
        MainWindow = Tk()
        MainWindow.title("Billing System")
        MainWindow.iconbitmap(Icon)
        MainWindow.state("zoomed")
        width = MainWindow.winfo_screenwidth()
        height = MainWindow.winfo_screenheight()
        MainWindow.geometry("%dx%d" % (width, height))
        MainWindow.rowconfigure(0, weight=1)
        MainWindow.columnconfigure(0, weight=1)
        Admin = CheckAdmin(CurrentUser)

        MainMenu = Menu(MainWindow)
        MainWindow.config(menu=MainMenu)

        if Admin:
            AdminsMenu(MainWindow)

        else:
            UsersMenu(MainWindow)

        # ================================== BILLING FRAME ================================== #
        BillingFrame = Frame(MainWindow, bg=BillingFrameTheme, relief=SOLID, bd=7)
        BillingFrame.grid(row=0, column=0, sticky="nsew")
        BillingFrameWidgets(BillingFrame)

        # ================================== ACTIVITY LOG =================================== #
        ActivityLogFrame = Frame(MainWindow, bg=ActivityLogFrameTheme, relief=SOLID, bd=7)
        ActivityLogFrame.grid(row=0, column=0, sticky="nsew")
        ActivityFrameWidgets(ActivityLogFrame)
        # =================================== MANAGE USERS FRAME ============================ #
        ManageUsersFrame = Frame(MainWindow, bg=ManageUsersFrameTheme, relief=SOLID, bd=7)
        ManageUsersFrame.grid(row=0, column=0, sticky="nsew")
        ManageUsersFrameWidgets(ManageUsersFrame)

        # =================================== INVENTORY FRAME =============================== #
        InventoryFrame = Frame(MainWindow, bg=LoginPageTheme1, relief=SOLID, bd=7)
        InventoryFrame.grid(row=0, column=0, sticky="nsew")
        InventoryFrameWidgets(InventoryFrame)
        # =====================================VIEW BILL FRAME=============================== #
        ViewBillFrame = Frame(MainWindow, bg=LoginPageTheme1, relief=SOLID, bd=7)
        ViewBillFrame.grid(row=0, column=0, sticky="nsew")
        ViewBillFrameWidgets(ViewBillFrame)

        FrameRaise(BillingFrame)
        MainWindow.mainloop()


def AdminsMenu(window_name):
    MainMenu = Menu(window_name)
    window_name.config(menu=MainMenu)
    # General Menu
    GeneralMenu = Menu(MainMenu, tearoff=0)
    MainMenu.add_cascade(label="General", menu=GeneralMenu)
    GeneralMenu.add_command(label="Change Username", command=ChangeUsernameWindow)
    GeneralMenu.add_command(label="Change Password", command=ChangePassWindow)
    GeneralMenu.add_separator()
    GeneralMenu.add_command(label="Logout and Quit",
                            command=lambda: (SetStaySignedIn(CurrentUser, False), window_name.quit()))
    GeneralMenu.add_command(label="Quit Application", command=lambda: window_name.quit())

    # Manage Menu
    ManageMenu = Menu(MainMenu, tearoff=0)
    MainMenu.add_cascade(label="Manage", menu=ManageMenu)
    ManageMenu.add_command(label="Activity Log", command=lambda: FrameRaise(ActivityLogFrame))
    ManageMenu.add_command(label="Manage Users", command=lambda: FrameRaise(ManageUsersFrame))
    ManageMenu.add_command(label="View Bills", command=lambda: FrameRaise(ViewBillFrame))

    # Edit Menu
    EditMenu = Menu(MainMenu, tearoff=0)
    MainMenu.add_cascade(label="Edit", menu=EditMenu)
    EditMenu.add_command(label="Edit Inventory", command=lambda: FrameRaise(InventoryFrame))


def UsersMenu(window_name):
    MainMenu = Menu(window_name)
    window_name.config(menu=MainMenu)
    # General Menu
    GeneralMenu = Menu(MainMenu, tearoff=0)
    MainMenu.add_cascade(label="General", menu=GeneralMenu)
    GeneralMenu.add_command(label="Change Username", command=ChangeUsernameWindow)
    GeneralMenu.add_command(label="Change Password", command=ChangePassWindow)
    GeneralMenu.add_separator()
    GeneralMenu.add_command(label="Logout and Quit",
                            command=lambda: (SetStaySignedIn(CurrentUser, False), window_name.quit()))
    GeneralMenu.add_command(label="Quit Application", command=lambda: window_name.quit())


def SearchItemBtn(value, TreeviewName, search_criteria=None, varname=None):
    data = []
    if search_criteria == "Rate":
        try:
            value = int(value)
            data = SearchItem(value=value, search_criteria=search_criteria)

        except ValueError:
            messagebox.showerror("Search", "Rate should be of integer type")
    else:
        data = SearchItem(value=value, search_criteria=search_criteria)

    if data is not None:
        InsertIntoInventory(data, TreeviewName, with_index=False)
    if varname is not None:
        varname.delete(0, END)


def BillingFrameWidgets(window_name):
    BillingHolder = LabelFrame(window_name, bg=BillingFrameTheme, text="Bill", width=1000)
    BillingHolder.pack(side=LEFT, fill=Y, padx=(5, 0), pady=(0, 5))
    BillingHolder.pack_propagate(False)
    StyleTTK(window_name)
    Columns = ("Sno", "ItC", "ItN", "Rate", "Qty", "Price")
    BillTree = ttk.Treeview(BillingHolder, columns=Columns, show="headings", style="mystyle1.Treeview")
    BillTree.tag_configure('nonstylized', background=BillingFrameTheme)
    BillTree.column("Sno", width=35, anchor=CENTER)
    BillTree.column("ItC", width=35, anchor=CENTER)
    BillTree.column("ItN", width=120, anchor=CENTER)
    BillTree.column("Qty", width=35, anchor=CENTER)
    BillTree.column("Rate", width=35, anchor=CENTER)
    BillTree.column("Price", width=35, anchor=CENTER)
    BillTree.heading("Sno", text="Serial No.")
    BillTree.heading("ItC", text="Item Code")
    BillTree.heading("ItN", text="Item Name")
    BillTree.heading("Qty", text="Qty.")
    BillTree.heading("Rate", text="Rate")
    BillTree.heading("Price", text="Amount")
    BillTree.pack(fill="both", expand=True, padx=10)
    # ============================================================================================================== #
    WidgetHolder = LabelFrame(window_name, bg=BillingFrameTheme, text="Widgets", height=625)
    WidgetHolder.pack(side=TOP, fill=X, padx=(0, 5))
    WidgetHolder.pack_propagate(False)
    Label(WidgetHolder, text="Item Code: ", font=Font6, bg=BillingFrameTheme, width=33, relief=SOLID).place(x=4, y=20)
    BillInsertCodeEntry = Entry(WidgetHolder, font=Font6, bg=TreeviewBackgroundTheme1, relief=SOLID, bd=2)
    BillInsertCodeEntry.place(x=110, y=80)
    BillInsertAddButton = Button(WidgetHolder, text="Add Item", font=Font6, bg=TreeviewBackgroundTheme1, relief=SOLID,
                                 command=lambda: AddItemToInsertIntoBillButton(BillInsertCodeEntry.get(), BillTree,
                                                                               BillInsertCodeEntry, TotalLabel))
    BillInsertAddButton.place(x=190, y=140)
    Label(WidgetHolder, text="Set Qty: ", font=Font6, bg=BillingFrameTheme, width=33, relief=SOLID).place(x=4, y=220)
    QuantityEntry = Entry(WidgetHolder, font=Font6, bg=TreeviewBackgroundTheme1, relief=SOLID, bd=2, width=5,
                          justify=CENTER)
    QuantityEntry.place(x=210, y=280)
    QuantityEntry.insert(0, "1")
    QtyIncreaseButton = Button(WidgetHolder, text=">", font=Font6, bg=TreeviewBackgroundTheme1, relief=SOLID, bd=2,
                               command=lambda: QuantityIncreaseButton(QuantityEntry, BillTree, TotalLabel))
    QtyIncreaseButton.place(x=305, y=280)
    QtyDecreaseButton = Button(WidgetHolder, text="<", font=Font6, bg=TreeviewBackgroundTheme1, relief=SOLID, bd=2,
                               command=lambda: QuantityDecreaseButton(QuantityEntry, BillTree, TotalLabel))
    QtyDecreaseButton.place(x=150, y=280)
    SetQtyButton = Button(WidgetHolder, text="Set", font=Font6, bg=TreeviewBackgroundTheme1, relief=SOLID, bd=2,
                          command=lambda: SetQuantityButton(value=QuantityEntry.get(), TreeviewName=BillTree,
                                                            LabelName=TotalLabel))
    SetQtyButton.place(x=220, y=330)
    Label(WidgetHolder, text="Bill Settings: ", font=Font6, bg=BillingFrameTheme, width=33, relief=SOLID).place(x=4,
                                                                                                                y=400)
    CreateBillButton = Button(WidgetHolder, text=" Create Bill ", font=Font6, bg=TreeviewBackgroundTheme1, relief=SOLID,
                              bd=2, command=lambda: CreateBillWindow(BillTree, TotalLabel))
    CreateBillButton.place(x=70, y=470)
    BillClearButton = Button(WidgetHolder, font=Font6, bg=TreeviewBackgroundTheme1, relief=SOLID, text="  Clear Bill  ",
                             command=lambda: ClearBillButton(BillTree, TotalLabel))
    BillClearButton.place(x=70, y=540)
    BillDeleteButton = Button(WidgetHolder, font=Font6, bg=TreeviewBackgroundTheme1, relief=SOLID, text="Delete Item",
                              command=lambda: DeleteSelectionsFromBillButton(BillTree, TotalLabel))
    BillDeleteButton.place(x=270, y=540)
    DeselectAllButton = Button(WidgetHolder, font=Font6, bg=TreeviewBackgroundTheme1, relief=SOLID, text="Deselect All",
                               command=lambda: DeselectAllButtonFunction(BillTree))
    DeselectAllButton.place(x=270, y=470)
    # =============================================================================================================== #
    TotalHolder = LabelFrame(window_name, bg=BillingFrameTheme, text="Grand Total", height=150)
    TotalHolder.pack(side=BOTTOM, fill=X, padx=(0, 5))
    TotalHolder.pack_propagate(False)
    Label(TotalHolder, text="Rs:", font=Font1, bg=BillingFrameTheme).place(x=130, y=20)
    TotalLabel = Label(TotalHolder, text="0.00", font=Font1, bg=BillingFrameTheme)
    TotalLabel.place(x=230, y=20)


def InsertIntoActivityTree(TreeviewName, records=FetchAllActivity()):
    all_activity = FetchAllActivity()
    for item in TreeviewName.get_children():
        TreeviewName.delete(item)
    if records == all_activity:
        for record in records:
            if records.index(record) % 2 == 0:
                TreeviewName.insert(parent="", index="end", values=record,
                                    tags=('nonstylized',))
            else:
                TreeviewName.insert(parent="", index="end", values=record)
    else:
        for record in records:
            serial_no = records.index(record)
            record = (serial_no + 1,) + tuple(record)
            if serial_no % 2 == 0:
                TreeviewName.insert(parent="", index="end", values=record,
                                    tags=('nonstylized',))
            else:
                TreeviewName.insert(parent="", index="end", values=record)


def GetActivityBtn(TreeviewName, username="None", date="None", month="None", year="None", hour="None"):
    records = GetActivity(username=username, date=date, month=month, year=year, hour=hour)
    if len(records) == 0:
        messagebox.showinfo("Activity", "No matching records were found")
    else:
        InsertIntoActivityTree(TreeviewName, records=records)


def ActivityFrameWidgets(window_name):
    global ActivityTree
    LogHolder = LabelFrame(window_name, text="Activity Log", width=1000, bg=ActivityLogFrameTheme)
    LogHolder.pack(fill="both", side=RIGHT)
    LogHolder.pack_propagate(False)
    StyleTTK(window_name)
    Columns = ("sno", "username", "date", "logintime", "logouttime", "turnover")
    ActivityTree = ttk.Treeview(LogHolder, columns=Columns, show="headings", style="mystyle2.Treeview")
    ActivityTree.tag_configure('nonstylized', background=ActivityLogFrameTheme)
    ActivityTree.column("sno", anchor=CENTER, width=40)
    ActivityTree.column("username", anchor=CENTER, width=40)
    ActivityTree.column("date", anchor=CENTER, width=40)
    ActivityTree.column("logintime", anchor=CENTER, width=40)
    ActivityTree.column("logouttime", anchor=CENTER, width=40)
    ActivityTree.column("turnover", anchor=CENTER, width=40)
    ActivityTree.heading("sno", text="Serial No.")
    ActivityTree.heading("username", text="Username")
    ActivityTree.heading("date", text="Date")
    ActivityTree.heading("logintime", text="Login Time")
    ActivityTree.heading("logouttime", text="Logout Time")
    ActivityTree.heading("turnover", text="Turnover")

    ActivityTree.pack(fill="both", expand=True, side=TOP, padx=10, pady=(5, 5))
    InsertIntoActivityTree(ActivityTree)

    ButtonHoldFrame = Frame(LogHolder)
    ButtonHoldFrame.pack(side=BOTTOM)

    ReturnBtn = Button(ButtonHoldFrame, text="Return To Billing Page", font=Font4, bg=ActivityLogFrameTheme,
                       relief=SOLID,
                       command=lambda: FrameRaise(BillingFrame))
    ReturnBtn.grid(row=0, column=0)

    RetBtn = Button(ButtonHoldFrame, text="Return To Previous Tab", font=Font4, bg=ActivityLogFrameTheme, relief=SOLID,
                    command=lambda: FrameRaise(PreviousTopFrame))
    RetBtn.grid(row=0, column=1)
    # ================================================================================================================ #
    WidgetHolder = LabelFrame(window_name, text="Search", width=540, bg=ActivityLogFrameTheme)
    WidgetHolder.pack(side=LEFT, fill="both")
    WidgetHolder.pack_propagate(False)
    Label(WidgetHolder, text="Check Activity", font=Font3, bg=TreeviewHeadingBackground2).pack(fill=X)
    Label(WidgetHolder, text="Username: ", font=Font6, bg=ActivityLogFrameTheme).place(x=80, y=50)
    ActivityUsernameChoiceVar = StringVar()
    ActivityUsernameChoiceOptions = GetUsers() + ["None"]
    ActivityUsernameChoiceBox = ttk.OptionMenu(WidgetHolder, ActivityUsernameChoiceVar,
                                               ActivityUsernameChoiceOptions[-1], *ActivityUsernameChoiceOptions,
                                               style='mystyle3.TMenubutton')
    ActivityUsernameChoiceBox.place(x=230, y=50)
    Label(WidgetHolder, text="----------------------------------------------", font=Font6,
          bg=ActivityLogFrameTheme).place(x=3, y=100)
    Label(WidgetHolder, text="Year:", font=Font6, bg=ActivityLogFrameTheme).place(x=80, y=143)
    ActivityYearChoiceVar = StringVar()
    ActivityYearChoiceOptions = [str(i) for i in range(Year - 5, Year + 5)] + ["None"]
    ActivityYearChoiceBox = ttk.OptionMenu(WidgetHolder, ActivityYearChoiceVar,
                                           ActivityYearChoiceOptions[-1], *ActivityYearChoiceOptions,
                                           style='mystyle3.TMenubutton')
    ActivityYearChoiceBox.place(x=190, y=140)
    Label(WidgetHolder, text="Month: ", font=Font6, bg=ActivityLogFrameTheme).place(x=80, y=203)
    ActivityMonthChoiceVar = StringVar()
    ActivityMonthChoiceOptions = [str(i) for i in range(1, 13)] + ["None"]
    ActivityMonthChoiceBox = ttk.OptionMenu(WidgetHolder, ActivityMonthChoiceVar,
                                            ActivityMonthChoiceOptions[-1], *ActivityMonthChoiceOptions,
                                            style='mystyle3.TMenubutton')
    ActivityMonthChoiceBox.place(x=190, y=200)
    Label(WidgetHolder, text="Date: ", font=Font6, bg=ActivityLogFrameTheme).place(x=80, y=263)
    ActivityDateChoiceVar = StringVar()
    ActivityDateChoiceOptions = [str(i) for i in range(1, 31)] + ["None"]
    ActivityDateChoiceBox = ttk.OptionMenu(WidgetHolder, ActivityDateChoiceVar,
                                           ActivityDateChoiceOptions[-1], *ActivityDateChoiceOptions,
                                           style='mystyle3.TMenubutton')
    ActivityDateChoiceBox.place(x=190, y=260)
    Label(WidgetHolder, text="Hour: ", font=Font6, bg=ActivityLogFrameTheme).place(x=80, y=323)
    ActivityHourChoiceVar = StringVar()
    ActivityHourChoiceOptions = [str(i) for i in range(0, 24)] + ["None"]
    ActivityHourChoiceBox = ttk.OptionMenu(WidgetHolder, ActivityHourChoiceVar,
                                           ActivityHourChoiceOptions[-1], *ActivityHourChoiceOptions,
                                           style='mystyle3.TMenubutton')
    ActivityHourChoiceBox.place(x=190, y=320)
    Label(WidgetHolder, text="----------------------------------------------", font=Font6,
          bg=ActivityLogFrameTheme).place(x=3, y=370)

    SearchActivityBtn = Button(WidgetHolder, text="Search", font=Font2, bg=ActivityLogFrameTheme, relief=SOLID,
                               command=lambda: GetActivityBtn(TreeviewName=ActivityTree,
                                                              username=ActivityUsernameChoiceVar.get(),
                                                              date=ActivityDateChoiceVar.get(),
                                                              month=ActivityMonthChoiceVar.get(),
                                                              year=ActivityYearChoiceVar.get(),
                                                              hour=ActivityHourChoiceVar.get()))

    SearchActivityBtn.place(x=170, y=440)
    ResetActivityBtn = Button(WidgetHolder, text="Reset", font=Font2, bg=ActivityLogFrameTheme, relief=SOLID,
                              command=lambda: InsertIntoActivityTree(ActivityTree))
    ResetActivityBtn.place(x=183, y=525)


def InsertIntoUserTree(rec, TreeviewName):
    for record in TreeviewName.get_children():
        TreeviewName.delete(record)
    for item in rec:
        serialno = rec.index(item) + 1
        if serialno % 2 == 0:
            if item[1] == "A":
                TreeviewName.insert(parent="", index="end", values=(serialno, item[0], "Admin"))
            else:
                TreeviewName.insert(parent="", index="end", values=(serialno, item[0], "Employee"))
        else:
            if item[1] == "A":
                TreeviewName.insert(parent="", index="end", values=(serialno, item[0], "Admin"),
                                    tags='nonstylized')
            else:
                TreeviewName.insert(parent="", index="end", values=(serialno, item[0], "Employee"),
                                    tags='nonstylized')


def ResetItemsBtn(TreeviewName):
    InsertIntoInventory(FetchAllItems(), TreeviewName)


def InsertIntoInventory(rec, TreeviewName, with_index=True):
    for record in TreeviewName.get_children():
        TreeviewName.delete(record)
    for item in rec:
        index = rec.index(item) + 1
        if with_index:
            record_tuple = (index,) + item
        else:
            item_list = list(item)
            record_list = [index] + item_list[1::]
            record_tuple = tuple(record_list)
        if index % 2 == 0:
            TreeviewName.insert(parent="", index="end", values=record_tuple)
        else:
            TreeviewName.insert(parent="", index="end", values=record_tuple, tags="nonstylized")


def ResetUsersButtonFunction(TreeviewName):
    records = FetchAllUsers()
    InsertIntoUserTree(records, TreeviewName)


def SearchUsersButton(TreeviewName, search_element, search_criteria):
    rec = SearchUsers(search_element, search_criteria)
    if not rec:
        messagebox.showinfo("Search Query", "No records found")
    else:
        InsertIntoUserTree(rec, TreeviewName)


def TreeviewSelectionValueObtain(TreeviewName):
    selected = TreeviewName.selection()
    selected_list = []
    for value in selected:
        selected_list.append(TreeviewName.item(value)['values'])
    if not selected_list:
        messagebox.showerror("Selection", "No entries were selected")
        return None
    else:
        return selected_list


def DeleteUserButton(TreeviewName):
    recs = TreeviewSelectionValueObtain(TreeviewName)
    if recs:
        reply = messagebox.askyesno("Delete", "Are you sure you want to delete the selected user(s)?")
        if reply:
            delete_list = []
            for item in recs:
                delete_list.append(item[1])
            delete_tuple = tuple(delete_list)
            action = DeleteUsers(delete_tuple)
            if action is True:
                messagebox.showinfo("Delete", "User(s) deleted successfully")
            elif action[0] == "ok":
                messagebox.showerror("Delete",
                                     f"User Account: {action[1]} cannot be deleted as its is the primary admin account")
            records = FetchAllUsers()
            InsertIntoUserTree(records, TreeviewName)
        else:
            pass


def PromoteUserButton(TreeviewName):
    recs = TreeviewSelectionValueObtain(TreeviewName)
    if recs:
        reply = messagebox.askyesno("Delete", "Are you sure you want to promote the selected user?")
        if reply:
            promote_list = []
            for item in recs:
                promote_list.append(item[1])
            promote_tuple = tuple(promote_list)
            if len(promote_tuple) > 1:
                messagebox.showerror("Promote", "Only one user can be promoted at a time")
            else:
                ok = PromoteUser(promote_tuple)
                if ok:
                    messagebox.showinfo("Promote", "User has been promoted to admin")
                    InsertIntoUserTree(FetchAllUsers(), TreeviewName)
                else:
                    messagebox.showinfo("Promote", "User is already an admin")
        else:
            pass


def DePromoteUserButton(TreeviewName):
    recs = TreeviewSelectionValueObtain(TreeviewName)
    if recs:
        reply = messagebox.askyesno("Delete", "Are you sure you want to De-promote the selected user?")
        if reply:
            depromote_list = []
            for item in recs:
                depromote_list.append(item[1])
            depromote_tuple = tuple(depromote_list)
            if len(depromote_tuple) > 1:
                messagebox.showerror("De-Promote", "Only one user can be de-promoted at a time")
            else:
                result = CheckIfPrimaryAdmin(depromote_tuple[0])
                if not result:
                    ok = DePromoteUser(depromote_tuple)
                    if ok:
                        messagebox.showinfo("De-Promote", "User has been de-promoted to employee")
                        InsertIntoUserTree(FetchAllUsers(), TreeviewName)
                    else:
                        messagebox.showinfo("Promote", "User is already an employee")
                else:
                    messagebox.showerror("Delete",
                                         f"User Account: {depromote_tuple[0]} cannot be de-promoted as its is the primary admin account")
        else:
            pass


def UpdateItemByNameButton(new_name, TreeviewName):
    records = TreeviewSelectionValueObtain(TreeviewName)
    if records is None:
        pass
    elif len(records) > 1:
        messagebox.showerror("Update", "Only one record can be updated as a time")
    else:
        current_itemcode = records[0][1]
        if new_name != "":
            var = UpdateItemByName(current_itemcode, new_name)
            if var:
                messagebox.showinfo("Update", "Name has been successfully updated")
                InsertIntoInventory(FetchAllItems(), TreeviewName)
        else:
            messagebox.showerror("Update", "Name cannot be empty")


def UpdateItemByCodeButton(new_code, TreeviewName):
    records = TreeviewSelectionValueObtain(TreeviewName)
    if records is None:
        pass
    elif len(records) > 1:
        messagebox.showerror("Update", "Only one record can be updated as a time")
    else:
        current_itemcode = records[0][1]
        if len(new_code) == 3:
            var = UpdateItemByCode(current_itemcode, new_code)
            if var:
                messagebox.showinfo("Update", "Code has been successfully updated")
                InsertIntoInventory(FetchAllItems(), TreeviewName)
        else:
            messagebox.showerror("Update", "Code should be of 3 characters")


def UpdateItemByStocksButton(new_stocks, TreeviewName):
    records = TreeviewSelectionValueObtain(TreeviewName)
    if records is None:
        pass
    elif len(records) > 1:
        messagebox.showerror("Update", "Only one record can be updated as a time")
    else:
        current_itemcode = records[0][1]
        try:
            new_stocks = int(new_stocks)
            var = UpdateItemByStocks(current_itemcode, new_stocks)
            if var:
                messagebox.showinfo("Update", "Stocks has been successfully updated")
                InsertIntoInventory(FetchAllItems(), TreeviewName)
        except ValueError:
            messagebox.showerror("Update", "Stocks should be of integer type")


def UpdateItemByRateButton(new_rate, TreeviewName):
    records = TreeviewSelectionValueObtain(TreeviewName)
    if records is None:
        pass
    elif len(records) > 1:
        messagebox.showerror("Update", "Only one record can be updated as a time")
    else:
        current_itemcode = records[0][1]
        try:
            new_rate = float(new_rate)
            var = UpdateItemByRate(current_itemcode, new_rate)
            if var:
                messagebox.showinfo("Update", "Rate has been successfully updated")
                InsertIntoInventory(FetchAllItems(), TreeviewName)
        except ValueError:
            messagebox.showerror("Update", "Rate should be of Numerical type")


def UpdateItemByAll(new_name, new_code, new_rate, new_stocks, TreeviewName):
    name_ok = False
    code_ok = False
    rate_ok = False
    stocks_ok = False
    records = TreeviewSelectionValueObtain(TreeviewName)
    if records is None:
        pass
    elif len(records) > 1:
        messagebox.showerror("Update", "Only one record can be updated at a time")
    else:
        current_itemcode = records[0][1]
        if len(new_code) == 3:
            code_ok = True
        if new_name != "":
            name_ok = True
        try:
            new_rate = float(new_rate)
            new_stocks = float(new_stocks)
            stocks_ok = True
            rate_ok = True
        except ValueError:
            messagebox.showerror("Update", "Rate and Stocks should be of integer type")

        if name_ok and code_ok and rate_ok and stocks_ok:
            UpdateItemByName(current_itemcode, new_name)
            UpdateItemByRate(current_itemcode, new_rate)
            UpdateItemByStocks(current_itemcode, new_stocks)
            UpdateItemByCode(current_itemcode, new_code)
            messagebox.showinfo("Update", "Record has been updated")
            InsertIntoInventory(FetchAllItems(), TreeviewName)


def DeleteSelectedItems(TreeviewName):
    records = TreeviewSelectionValueObtain(TreeviewName)
    codes = []
    if records is None:
        return False
    else:
        for item in records:
            codes.append(item[1])
    if codes is not None:
        for item in codes:
            mycursor.execute("DELETE FROM inventory WHERE item_code = %s", (item,))
            mydb.commit()
    messagebox.showinfo("Delete", "Selected record(s) deleted")
    InsertIntoInventory(FetchAllItems(), TreeviewName)


def AddItemButtonFunction(code, name, rate, stocks, TreeviewName):
    if code != "":
        if len(code) == 3:
            if name != "":
                var = CheckUniqueCode(code)
                if var:
                    if rate != "":
                        if stocks != "":
                            try:
                                rate = float(rate)
                                stocks = int(stocks)
                                AddItem(code, name, rate, stocks)
                                messagebox.showinfo("Add Item", "Item Successfully added")
                                InsertIntoInventory(FetchAllItems(), TreeviewName)
                            except ValueError:
                                messagebox.showerror("Add Item", "Rate and Stocks should be of Numerical type")
                        else:
                            messagebox.showerror("Add Item", "Item Stocks Unfilled")
                    else:
                        messagebox.showerror("Add Item", "Item Rate Unfilled")
                else:
                    messagebox.showerror("Add Item", "Item code is already used")
            else:
                messagebox.showerror("Add Item", "Item Name Unfilled")
        else:
            messagebox.showerror("Add Item", "Item Code should be 3 characters")
    else:
        messagebox.showerror("Add Item", "Item Code Unfilled")


def ManageViewActivityButton(DeliveryTreeviewName, TargetTreeviewName):
    records = TreeviewSelectionValueObtain(DeliveryTreeviewName)
    if records is None:
        pass
    elif len(records) > 1:
        messagebox.showinfo("View Activity", "Only one record can be selected at a time")
    else:
        username = records[0][1]
        FrameRaise(ActivityLogFrame)
        records = GetActivity(username=username)
        if len(records) == 0:
            messagebox.showinfo("Activity", "No matching records were found")
        else:
            InsertIntoActivityTree(TreeviewName=TargetTreeviewName, records=records)


def InventoryFrameWidgets(window_name):
    global InventoryTree
    StyleTTK(InventoryFrame)
    # =============================================================================================================== #
    InventoryHolder = LabelFrame(window_name, bg=LoginPageTheme1, width=800, text="View")
    InventoryHolder.pack(side=RIGHT, fill=Y, padx=(0, 5))
    InventoryHolder.pack_propagate(False)
    Columns = ("sno", "icode", "iname", "rate", "stocks")
    InventoryTree = ttk.Treeview(InventoryHolder, columns=Columns, show="headings", style='mystyle1.Treeview')
    InventoryTree.tag_configure('nonstylized', background=LoginPageTheme1)
    InventoryTree.column("sno", width=100, anchor=CENTER)
    InventoryTree.column("icode", width=100, anchor=CENTER)
    InventoryTree.column("iname", width=100, anchor=CENTER)
    InventoryTree.column("rate", width=100, anchor=CENTER)
    InventoryTree.column("stocks", width=100, anchor=CENTER)
    InventoryTree.heading("sno", text="Serial No.")
    InventoryTree.heading("icode", text="Item Code")
    InventoryTree.heading("iname", text="Item Name")
    InventoryTree.heading("rate", text="Rate")
    InventoryTree.heading("stocks", text="Stocks")
    InventoryTree.pack(fill="both", expand=True, pady=(9, 0), padx=(5, 5))
    InsertIntoInventory(FetchAllItems(), InventoryTree)
    ButtonHoldFrame = Frame(InventoryHolder)
    ButtonHoldFrame.pack(side=BOTTOM)

    ReturnBtn = Button(ButtonHoldFrame, text="Return To Billing Page", font=Font4, bg=LoginPageTheme1,
                       relief=SOLID,
                       command=lambda: FrameRaise(BillingFrame))
    ReturnBtn.grid(row=0, column=0)

    RetBtn = Button(ButtonHoldFrame, text="Return To Previous Tab", font=Font4, bg=LoginPageTheme1, relief=SOLID,
                    command=lambda: FrameRaise(PreviousTopFrame))
    RetBtn.grid(row=0, column=1)
    # =============================================================================================================== #
    UpdateInventoryHolder = LabelFrame(window_name, bg=LoginPageTheme1, width=710)
    UpdateInventoryHolder.pack(side=LEFT, fill=Y, padx=(5, 0))
    UpdateInventoryHolder.pack_propagate(False)
    # =============================================================================================================== #
    SearchItemHolder = LabelFrame(UpdateInventoryHolder, text="Search", height=155, bg=LoginPageTheme1)
    SearchItemHolder.pack(fill=X)
    SearchItemHolder.pack_propagate(False)
    Label(SearchItemHolder, text="Search Criteria: ", font=Font7, bg=LoginPageTheme1).place(x=140, y=0)
    MenuBoxChoice = ("Item Code", 'Item Name', "Rate")
    MenuBoxVar = StringVar()
    MenuBox = ttk.OptionMenu(SearchItemHolder, MenuBoxVar, MenuBoxChoice[1], *MenuBoxChoice,
                             style='mystyle2.TMenubutton')
    MenuBox.place(x=345, y=0)
    Label(SearchItemHolder, text="Enter Query:", font=Font7, bg=LoginPageTheme1).place(x=10, y=62)
    QueryEntryField = Entry(SearchItemHolder, font=Font7, bg=TreeviewBackgroundTheme1, relief=SOLID)
    QueryEntryField.place(x=175, y=65)
    SearchButton = Button(SearchItemHolder, font=Font7, text="Search", bg=TreeviewBackgroundTheme1,
                          activebackground=TreeviewBackgroundTheme1,
                          relief=SOLID,
                          command=lambda: SearchItemBtn(value=QueryEntryField.get(), TreeviewName=InventoryTree,
                                                        search_criteria=MenuBoxVar.get(), varname=QueryEntryField))
    SearchButton.place(x=470, y=55)

    RefreshButton = Button(SearchItemHolder, font=Font7, text=" Reset ", bg=TreeviewBackgroundTheme1,
                           activebackground=TreeviewBackgroundTheme1, relief=SOLID,
                           command=lambda: ResetItemsBtn(InventoryTree))
    RefreshButton.place(x=580, y=55)
    #  ============================================================================================================== #
    AddItemHolder = LabelFrame(UpdateInventoryHolder, text="Add item", height=220, bg=LoginPageTheme1)
    AddItemHolder.pack(fill=X, pady=(5, 5))
    AddItemHolder.pack_propagate(False)
    Label(AddItemHolder, font=Font7, text="Item Name:", bg=LoginPageTheme1).place(x=0, y=0)
    Label(AddItemHolder, font=Font7, text="Item Code:", bg=LoginPageTheme1).place(x=0, y=50)
    Label(AddItemHolder, font=Font7, text="Item Rate:", bg=LoginPageTheme1).place(x=0, y=100)
    Label(AddItemHolder, font=Font7, text="Stocks:", bg=LoginPageTheme1).place(x=0, y=150)
    ItemNameEntry = Entry(AddItemHolder, font=Font7, bg=TreeviewBackgroundTheme1, relief=SOLID)
    ItemNameEntry.place(x=150, y=0)
    ItemCodeEntry = Entry(AddItemHolder, font=Font7, bg=TreeviewBackgroundTheme1, relief=SOLID)
    ItemCodeEntry.place(x=150, y=50)
    ItemRateEntry = Entry(AddItemHolder, font=Font7, bg=TreeviewBackgroundTheme1, relief=SOLID)
    ItemRateEntry.place(x=150, y=100)
    ItemStocksEntry = Entry(AddItemHolder, font=Font7, bg=TreeviewBackgroundTheme1, relief=SOLID)
    ItemStocksEntry.place(x=150, y=150)
    AddItemButton = Button(AddItemHolder, font=Font7, text="Add Item", bg=TreeviewBackgroundTheme1,
                           activebackground=TreeviewBackgroundTheme1, relief=SOLID,
                           command=lambda: (AddItemButtonFunction(ItemCodeEntry.get(), ItemNameEntry.get(),
                                                                  ItemRateEntry.get(), ItemStocksEntry.get(),
                                                                  InventoryTree), ItemNameEntry.delete(0, END),
                                            ItemRateEntry.delete(0, END), ItemCodeEntry.delete(0, END),
                                            ItemStocksEntry.delete(0, END)))
    AddItemButton.place(x=470, y=70)
    # ============================================================================================================== #
    UpdateAndDeleteHolder = LabelFrame(UpdateInventoryHolder, text="Update and Delete", height=400, bg=LoginPageTheme1)
    UpdateAndDeleteHolder.pack(fill=X)
    UpdateAndDeleteHolder.pack_propagate(False)
    Label(UpdateAndDeleteHolder, font=Font7, text="Name:", bg=LoginPageTheme1).place(x=0, y=8)
    Label(UpdateAndDeleteHolder, font=Font7, text="Code:", bg=LoginPageTheme1).place(x=0, y=78)
    Label(UpdateAndDeleteHolder, font=Font7, text="Rate:", bg=LoginPageTheme1).place(x=0, y=148)
    Label(UpdateAndDeleteHolder, font=Font7, text="Stocks:", bg=LoginPageTheme1).place(x=0, y=218)
    ItemUpdateNameEntry = Entry(UpdateAndDeleteHolder, font=Font7, bg=TreeviewBackgroundTheme1, relief=SOLID)
    ItemUpdateNameEntry.place(x=100, y=10)
    ItemUpdateCodeEntry = Entry(UpdateAndDeleteHolder, font=Font7, bg=TreeviewBackgroundTheme1, relief=SOLID)
    ItemUpdateCodeEntry.place(x=100, y=80)
    ItemUpdateRateEntry = Entry(UpdateAndDeleteHolder, font=Font7, bg=TreeviewBackgroundTheme1, relief=SOLID)
    ItemUpdateRateEntry.place(x=100, y=150)
    ItemUpdateStocksEntry = Entry(UpdateAndDeleteHolder, font=Font7, bg=TreeviewBackgroundTheme1, relief=SOLID)
    ItemUpdateStocksEntry.place(x=100, y=220)
    GetSelectionIntoEntryButton = Button(UpdateAndDeleteHolder, text="Get Selection", font=Font7,
                                         bg=TreeviewBackgroundTheme1,
                                         activebackground=TreeviewBackgroundTheme1, relief=SOLID,
                                         command=lambda: GetTextIntoEntry(ItemUpdateNameEntry, ItemUpdateCodeEntry,
                                                                          ItemUpdateRateEntry, ItemUpdateStocksEntry,
                                                                          InventoryTree))
    GetSelectionIntoEntryButton.place(x=450, y=10)
    ClearSelectionIntoEntryButton = Button(UpdateAndDeleteHolder, text=" Clear Boxes ", font=Font7,
                                           bg=TreeviewBackgroundTheme1,
                                           activebackground=TreeviewBackgroundTheme1, relief=SOLID,
                                           command=lambda: (ItemUpdateNameEntry.delete(0, END),
                                                            ItemUpdateCodeEntry.delete(0, END),
                                                            ItemUpdateRateEntry.delete(0, END),
                                                            ItemUpdateStocksEntry.delete(0, END)))
    ClearSelectionIntoEntryButton.place(x=450, y=75)
    UpdateItemAllButton = Button(UpdateAndDeleteHolder, font=Font7, text="     Update    ",
                                 bg=TreeviewBackgroundTheme1,
                                 activebackground=TreeviewBackgroundTheme1, relief=SOLID,
                                 command=lambda: UpdateItemByAll(new_name=ItemUpdateNameEntry.get(),
                                                                 new_code=ItemUpdateCodeEntry.get(),
                                                                 new_rate=ItemUpdateRateEntry.get(),
                                                                 new_stocks=ItemUpdateStocksEntry.get(),
                                                                 TreeviewName=InventoryTree))
    UpdateItemAllButton.place(x=450, y=140)
    DeleteItemButton = Button(UpdateAndDeleteHolder, font=Font7, text=" Delete Item ",
                              bg=TreeviewBackgroundTheme1,
                              activebackground=TreeviewBackgroundTheme1, relief=SOLID,
                              command=lambda: DeleteSelectedItems(InventoryTree))
    DeleteItemButton.place(x=450, y=205)


def ManageUsersFrameWidgets(window_name):
    TreeHolder = LabelFrame(window_name, text="Users", bg=ManageUsersFrameTheme, width=800, height=800)
    TreeHolder.pack(side=LEFT, padx=(5, 0), pady=(0, 5))
    TreeHolder.pack_propagate(False)
    StyleTTK(window_name)
    Columns = ("sno", "name", "type")
    UserTree = ttk.Treeview(TreeHolder, columns=Columns, show="headings", style="mystyle3.Treeview")
    UserTree.tag_configure('nonstylized', background=ManageUsersFrameTheme)
    UserTree.column("sno", anchor=CENTER)
    UserTree.column("name", anchor=CENTER)
    UserTree.column("type", anchor=CENTER)
    UserTree.heading("sno", text="Serial No.")
    UserTree.heading("name", text="Username")
    UserTree.heading("type", text="User Type")
    UserTree.pack(fill="both", expand=True, side=TOP, padx=10, pady=(5, 5))
    UserTree.pack_propagate(False)

    ResetUsersButtonFunction(UserTree)

    ButtonHoldFrame = Frame(TreeHolder)
    ButtonHoldFrame.pack(side=BOTTOM)

    ReturnBtn = Button(ButtonHoldFrame, text="Return To Billing Page", font=Font4, bg=ManageUsersFrameTheme,
                       relief=SOLID,
                       command=lambda: FrameRaise(BillingFrame))
    ReturnBtn.grid(row=0, column=0)

    RetBtn = Button(ButtonHoldFrame, text="Return To Previous Tab", font=Font4, bg=ManageUsersFrameTheme, relief=SOLID,
                    command=lambda: FrameRaise(PreviousTopFrame))
    RetBtn.grid(row=0, column=1)
    # ================================================================================================================ #
    SearchHolder = LabelFrame(window_name, text="Search", bg=ManageUsersFrameTheme, height=262, width=550)
    SearchHolder.pack(padx=(2, 5))
    SearchHolder.pack_propagate(False)
    Label(SearchHolder, bg=ManageUsersFrameTheme, text="Select a Search Criteria: ", font=Font6).place(x=30, y=5)
    ComboBoxVar = StringVar()
    ChoiceBoxOptions = ("Username", "Usertype")
    ChoiceBox = ttk.OptionMenu(SearchHolder, ComboBoxVar, ChoiceBoxOptions[0], *ChoiceBoxOptions,
                               style='mystyle.TMenubutton')
    ChoiceBox.place(x=330, y=5)
    Label(SearchHolder, bg=ManageUsersFrameTheme, text="Enter Query: ", font=Font6).place(x=30, y=70)
    QueryEntry = Entry(SearchHolder, font=Font6, relief=SOLID, bg=TreeviewBackgroundTheme3)
    QueryEntry.place(x=207, y=73)
    SearchButton = Button(SearchHolder, font=Font6, text="Search", bg=TreeviewBackgroundTheme3,
                          activebackground=ManageUsersFrameTheme,
                          relief=SOLID,
                          command=lambda: SearchUsersButton(UserTree, QueryEntry.get(), ComboBoxVar.get()))
    SearchButton.place(x=150, y=150)

    ClearButton = Button(SearchHolder, font=Font6, text=" Reset ", bg=TreeviewBackgroundTheme3,
                         activebackground=ManageUsersFrameTheme, relief=SOLID,
                         command=lambda: ResetUsersButtonFunction(UserTree))
    ClearButton.place(x=270, y=150)
    # ================================================================================================== #
    AddHolder = LabelFrame(window_name, text="Add User", bg=ManageUsersFrameTheme, height=262, width=550)
    AddHolder.pack(padx=(2, 5))
    AddHolder.pack_propagate(False)
    Label(AddHolder, bg=ManageUsersFrameTheme, text="Add New User: ", font=Font6).place(x=11, y=20)
    NewUserNameEntry = Entry(AddHolder, font=Font6, relief=SOLID, bg=TreeviewBackgroundTheme3)
    NewUserNameEntry.place(x=213, y=23)
    UserTypeChoiceVar = StringVar()
    Label(AddHolder, bg=ManageUsersFrameTheme, text="Select User Type: ", font=Font6).place(x=10, y=80)
    UserTypeChoiceOptions = ("Admin", "Employee")
    UsertypeChoice = ttk.OptionMenu(AddHolder, UserTypeChoiceVar, UserTypeChoiceOptions[1], *UserTypeChoiceOptions,
                                    style='mystyle.TMenubutton')
    UsertypeChoice.place(x=282, y=80)
    CreateUserBtn = Button(AddHolder, font=Font6, text="Create User", bg=TreeviewBackgroundTheme3,
                           activebackground=ManageUsersFrameTheme,
                           command=lambda: (
                               AddUserBtn(username=NewUserNameEntry.get(), window_name=None, staysignedin=False,
                                          Admin=UserTypeChoiceVar.get()),
                               InsertIntoUserTree(FetchAllUsers(), UserTree), NewUserNameEntry.delete(0, END)),
                           relief=SOLID)
    CreateUserBtn.place(x=200, y=150)
    # ================================================================================================== #
    ManageHolder = LabelFrame(window_name, text="Manage", bg=ManageUsersFrameTheme, height=252, width=550)
    ManageHolder.pack(padx=(2, 5))
    ManageHolder.pack_propagate(False)
    UserDeleteBtn = Button(ManageHolder, font=Font6, text="     Delete     ", bg=TreeviewBackgroundTheme3, relief=SOLID,
                           command=lambda: DeleteUserButton(UserTree))
    UserDeleteBtn.place(x=80, y=130)
    UserDeleteBtn = Button(ManageHolder, font=Font6, text="View Activity", bg=TreeviewBackgroundTheme3, relief=SOLID,
                           command=lambda: ManageViewActivityButton(UserTree, ActivityTree))
    UserDeleteBtn.place(x=80, y=30)
    UserDeleteBtn = Button(ManageHolder, font=Font6, text="     Promote    ", bg=TreeviewBackgroundTheme3, relief=SOLID,
                           command=lambda: PromoteUserButton(UserTree))
    UserDeleteBtn.place(x=270, y=30)
    UserDeleteBtn = Button(ManageHolder, font=Font6, text="  De-Promote  ", bg=TreeviewBackgroundTheme3, relief=SOLID,
                           command=lambda: DePromoteUserButton(UserTree))
    UserDeleteBtn.place(x=270, y=130)


def StyleTTK(window_name):
    style = ttk.Style()
    style.theme_use("alt")
    if window_name == BillingFrame or window_name == InventoryFrame:
        style.configure("mystyle1.Treeview.Heading", font=Font5, background=TreeviewHeadingBackground1,
                        foreground=TreeviewHeadingForeground1)
        style.map("mystyle1.Treeview.Heading", background=[('selected', TreeviewHeadingBackground1)])
        style.configure("mystyle1.Treeview", background=TreeviewBackgroundTheme1, foreground=TreeviewForegroundTheme1,
                        rowheight=50,
                        fieldbackground=BillingFrameTheme, font=Font4)
        style.map('mystyle1.Treeview', background=[('selected', SelectionBackground1)],
                  foreground=[('selected', "white")])
        style.configure("mystyle2.TMenubutton", background=LoginPageTheme2, font=Font5)
        style.map("mystyle2.TMenubutton", background=[("selected", LoginPageTheme2)])
    elif window_name == ActivityLogFrame:
        style.configure("mystyle2.Treeview.Heading", background=TreeviewHeadingBackground2,
                        foreground=TreeviewHeadingForeground2, font=Font5)
        style.map("mystyle2.Treeview.Heading", background=[("selected", TreeviewHeadingBackground2)])
        style.configure("mystyle2.Treeview", background=TreeviewBackgroundTheme2, foreground=TreeviewForegroundTheme2,
                        rowheight=50,
                        fieldbackground=ActivityLogFrameTheme, font=Font4)
        style.map('mystyle2.Treeview', background=[('selected', SelectionBackground2)],
                  foreground=[('selected', "white")])
        style.configure("mystyle3.TMenubutton", background=ActivityLogFrameTheme, font=Font6)
        style.map("mystyle3.TMenubutton", background=[('selected', ActivityLogFrameTheme)])
    elif window_name == ManageUsersFrame:
        style.configure("mystyle3.Treeview.Heading", font=Font5, background=TreeviewHeadingBackground3,
                        foreground=TreeviewHeadingForeground3)
        style.map("mystyle3.Treeview.Heading", background=[('selected', TreeviewHeadingBackground3)])
        style.configure("mystyle3.Treeview", background=TreeviewBackgroundTheme3, foreground=TreeviewForegroundTheme3,
                        rowheight=50, fieldbackground=ManageUsersFrameTheme, font=Font4)
        style.map('mystyle3.Treeview', background=[('selected', SelectionBackground3)],
                  foreground=[('selected', "white")])
        style.configure("mystyle.TMenubutton", background=TreeviewBackgroundTheme3, font=Font5)
        style.map("mystyle.TMenubutton", background=[("selected", TreeviewBackgroundTheme3)])


def FrameRaise(FrameName):
    global PreviousTopFrame, CurrentTopFrame
    PreviousTopFrame = CurrentTopFrame
    FrameName.tkraise()
    CurrentTopFrame = FrameName


def CallUpdateActivity():
    if Start_Time is not None:
        if ActivityUpdatable:
            username = CurrentUser
            components = Start_Time.split()
            date = components[0]
            logintime = components[1].split(".")[0]
            UpdateActivity(username, logintime, date, turnover=GetTurnover())


def ChangePassBtn(window_name, username, old_pass, new_pass):
    var = EligibilityCheck(password=new_pass, OnlyCheckPass=True)
    if var:
        var2 = ChangePassword(username, old_pass, new_pass)
        if not var2:
            messagebox.showerror("Change Password", "Old Password is incorrect")
            window_name.focus_force()
        elif var2:
            messagebox.showinfo("Change Password", "Password Changed Successfully")
            window_name.destroy()
    else:
        window_name.focus_force()


def ChangePassWindow():
    window = Toplevel()
    window.focus_force()
    window.title("Change Password")
    window.config(bg=LoginPageTheme1)
    window_width = 470
    window_height = 290
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    xCoordinate = int(screen_width / 2 - window_width / 2)
    yCoordinate = int(screen_height / 2 - window_height / 2)
    window.geometry(f'{window_width}x{window_height}+{xCoordinate}+{yCoordinate}')
    window.resizable(False, False)
    window.iconbitmap(Icon)

    Label(window, text="  Old Password:", font=Font5, bg=LoginPageTheme1, fg=TreeviewHeadingBackground1).place(x=10,
                                                                                                               y=50)
    Label(window, text="New Password:", font=Font5, bg=LoginPageTheme1, fg=TreeviewHeadingBackground1).place(x=10,
                                                                                                             y=120)
    OldPass = Entry(window, font=Font5, relief=SOLID, show="*")
    OldPass.place(x=190, y=50)

    NewPass = Entry(window, font=Font5, relief=SOLID, show="*")
    NewPass.place(x=190, y=120)

    ShowPassVar = IntVar()
    ShowPassBtn = Checkbutton(window, text="Show Password", font=Font5, bg=LoginPageTheme1, variable=ShowPassVar,
                              activebackground=LoginPageTheme1, activeforeground=LoginPageTheme2, fg=LoginPageTheme2,
                              command=lambda: show_password((NewPass, OldPass), ShowPassVar))
    ShowPassBtn.place(x=150, y=170)
    ChangeButton = Button(window, text="Change", font=Font5, bg=LoginPageTheme1, activebackground=LoginPageTheme1,
                          fg=LoginPageTheme2, activeforeground=LoginPageTheme2, relief=RIDGE, bd=2,
                          command=lambda: ChangePassBtn(window, CurrentUser, OldPass.get(), NewPass.get()))
    ChangeButton.place(x=182, y=225)


def ChangeUsernameBtn(window_name, username):
    global CurrentUser
    var = EligibilityCheck(username=username, OnlyCheckUsername=True)
    if var:
        var2 = ChangeUsername(CurrentUser, username)
        if var2:
            messagebox.showinfo("Username", "Username was changed successfully")
            CurrentUser = username
            window_name.destroy()
    else:
        window_name.focus_force()


def ChangeUsernameWindow():
    UsernameChangeWindow = Toplevel()
    UsernameChangeWindow.focus_force()
    UsernameChangeWindow.title("Change Username")
    UsernameChangeWindow.config(bg=LoginPageTheme1)
    window_width = 470
    window_height = 120
    screen_width = UsernameChangeWindow.winfo_screenwidth()
    screen_height = UsernameChangeWindow.winfo_screenheight()
    xCoordinate = int(screen_width / 2 - window_width / 2)
    yCoordinate = int(screen_height / 2 - window_height / 2)
    UsernameChangeWindow.geometry(f'{window_width}x{window_height}+{xCoordinate}+{yCoordinate}')
    UsernameChangeWindow.resizable(False, False)
    UsernameChangeWindow.iconbitmap(Icon)

    Label(UsernameChangeWindow, text="New Username:", font=Font5, bg=LoginPageTheme1,
          fg=TreeviewHeadingBackground1).place(x=15, y=20)
    NewUsername = Entry(UsernameChangeWindow, font=Font5, relief=SOLID)
    NewUsername.place(x=195, y=20)

    ChangeButton = Button(UsernameChangeWindow, text="Change", font=Font5, bg=LoginPageTheme1,
                          activebackground=LoginPageTheme1,
                          fg=LoginPageTheme2, activeforeground=LoginPageTheme2, relief=RIDGE, bd=2,
                          command=lambda: ChangeUsernameBtn(UsernameChangeWindow, NewUsername.get()))
    ChangeButton.place(x=182, y=70)


def AddItemToInsertIntoBillButton(item_code, TreeviewName, varname, LabelName):
    Added = AddIntoBill(item_code)
    if Added == "Exists":
        messagebox.showinfo("Bill", "Item already exists")
        RefreshBillTree(TreeviewName)
    elif Added:
        RefreshBillTree(TreeviewName)
    else:
        messagebox.showinfo("Bill", "No matching records were found")
    varname.delete(0, END)
    RefreshGrandTotal(LabelName)


def RefreshBillTree(TreeviewName):
    for row in TreeviewName.get_children():
        TreeviewName.delete(row)
    bill = ReturnBill()
    if not bill:
        pass
    else:
        for item in bill:
            index = bill.index(item) + 1
            item = [index] + item
            if index % 2 == 0:
                TreeviewName.insert(parent="", index="end", values=item)
            else:
                TreeviewName.insert(parent="", index="end", values=item, tags="nonstylized")


def RefreshGrandTotal(LabelName):
    GrandTotal = CalculateTotal()
    LabelName['text'] = str(GrandTotal) + "0"


def DeleteSelectionsFromBillButton(TreeviewName, LabelName):
    records = TreeviewSelectionValueObtain(TreeviewName)
    if records is None:
        pass
    else:
        for item in records:
            item_code = item[1]
            DeleteFromBill(item_code)
    RefreshBillTree(TreeviewName)
    RefreshGrandTotal(LabelName)


def ClearBillButton(TreeviewName, LabelName):
    ClearBill()
    RefreshBillTree(TreeviewName)
    RefreshGrandTotal(LabelName)


def SetQuantityButton(value, TreeviewName, LabelName):
    try:
        value = int(value)
        records = TreeviewSelectionValueObtain(TreeviewName)
        item_codes = []
        if records is not None:
            for item in records:
                item_codes.append(item[1])
        for item in item_codes:
            ok = CheckStocks(item, value)
            if ok:
                SetQuantity(value, item)
                RefreshBillTree(TreeviewName)
                RefreshGrandTotal(LabelName)
            else:
                messagebox.showerror("Stocks", "Insufficient stocks available")
        return item_codes
    except ValueError:
        messagebox.showerror("Quantity", "Quantity should be of integer type")


def QuantityIncreaseButton(varname, TreeviewName, LabelName):
    try:
        existing_value = int(varname.get())
        new_value = existing_value + 1
        item_codes = SetQuantityButton(new_value, TreeviewName, LabelName)
        ok = False
        for item in item_codes:
            if CheckStocks(item, new_value):
                ok = True

        if item_codes and ok:
            varname.delete(0, END)
            varname.insert(0, str(new_value))
        children = TreeviewName.get_children()
        code_list = []
        code_item_list = []
        for value in children:
            code_list.append(TreeviewName.item(value)['values'][1])
            code_item_list.append(value)
        range_limit = len(code_list)
        for i in range(range_limit):
            if code_list[i] in item_codes:
                TreeviewName.selection_add(code_item_list[i])
        RefreshGrandTotal(LabelName)
    except ValueError:
        messagebox.showerror("Quantity", "Quantity should be of integer type")


def QuantityDecreaseButton(varname, TreeviewName, LabelName):
    new_value = "1"
    try:
        existing_value = int(varname.get())
        if existing_value >= 2:
            new_value = existing_value - 1
        else:
            messagebox.showinfo("Quantity", "Quantity cannot be lesser than 1")
        item_codes = SetQuantityButton(new_value, TreeviewName, LabelName)
        if item_codes:
            varname.delete(0, END)
            varname.insert(0, str(new_value))
        children = TreeviewName.get_children()
        code_list = []
        code_item_list = []
        for value in children:
            code_list.append(TreeviewName.item(value)['values'][1])
            code_item_list.append(value)
        range_limit = len(code_list)
        for i in range(range_limit):
            if code_list[i] in item_codes:
                TreeviewName.selection_add(code_item_list[i])
    except ValueError:
        messagebox.showerror("Quantity", "Quantity should be of integer type")


def DeselectAllButtonFunction(TreeviewName):
    for item in TreeviewName.selection():
        TreeviewName.selection_remove(item)


def generate_grocery_bill_string(customer_id, items):
    bill_string = "=============================================\n"
    bill_string += "          GROCERY STORE BILL\n"
    bill_string += "Customer ID: " + customer_id + "\n"
    bill_string += "=============================================\n"
    bill_string += "{:<10} {:<20} {:<10} {:<10} {:<10}\n".format("Item Code", "Item Name", "Rate", "Quantity", "Total")
    bill_string += "---------------------------------------------\n"

    total_price = 0.0

    for item in items:
        item_code, item_name, rate, quantity, total = item
        total_price += float(total)
        bill_string += "{:<10} {:<20} ${:<9.2f} {:<10} ${:<9.2f}\n".format(item_code, item_name, float(rate),
                                                                           int(quantity), float(total))

    bill_string += "=============================================\n"
    bill_string += "Total: ${:.2f}\n".format(total_price)

    return bill_string


def CreateBillWindow(TreeviewName, LabelName):
    current_bill = ReturnBill()
    if len(current_bill) > 0:
        BillWindow = Toplevel()
        BillWindow.focus_force()
        BillWindow.title("Create Bill")
        BillWindow.config(bg=LoginPageTheme1)
        window_width = 1920
        window_height = 1080
        screen_width = BillWindow.winfo_screenwidth()
        screen_height = BillWindow.winfo_screenheight()
        xCoordinate = int(screen_width / 2 - window_width / 2)
        yCoordinate = int(screen_height / 2 - window_height / 2)
        BillWindow.geometry(f'{window_width}x{window_height}+{xCoordinate}+{yCoordinate}')
        BillWindow.resizable(False, False)
        BillWindow.iconbitmap(Icon)

        Label(BillWindow, text="Customer Name:", font=Font5, bg=LoginPageTheme1,
              fg=TreeviewHeadingBackground1).place(x=15, y=20)
        Label(BillWindow, text="Customer ID:", font=Font5, bg=LoginPageTheme1,
              fg=TreeviewHeadingBackground1).place(x=15, y=80)
        CustomerNameEntry = Entry(BillWindow, font=Font5, relief=SOLID)
        CustomerNameEntry.place(x=195, y=20)
        IdLabel = Label(BillWindow, font=Font5, fg="Black", bg=LoginPageTheme1)
        IdLabel.place(x=195, y=80)
        output = GenerateCustomerId()
        IdLabel['text'] = output
        billstring = generate_grocery_bill_string(output,current_bill)
        print(billstring)
        ##############################################
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(billstring)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Convert the PIL Image to a PhotoImage
        photo = ImageTk.PhotoImage(qr_img)

        # Create a label to display the QR code in the parent window
        qr_label = Label(BillWindow, image=photo)
        qr_label.photo = photo  # To prevent it from being garbage collected
        qr_label.place(x=300,y=150)
        ###################################
        CreateFinalBillButton = Button(BillWindow, text="Create", font=Font5, bg=LoginPageTheme1,
                                       activebackground=LoginPageTheme1,
                                       fg=LoginPageTheme2, activeforeground=LoginPageTheme2, relief=RIDGE, bd=2,
                                       command=lambda: CreateFinalBillButtonFunction(BillWindow,
                                                                                     CustomerNameEntry.get(),
                                                                                     TreeviewName, LabelName, output))
        CreateFinalBillButton.place(x=185, y=455)
    else:
        messagebox.showerror("Bill", "Bill cannot be empty")


def CreateFinalBillButtonFunction(window_name, name, TreeviewName, LabelName, output):
    if name == "":
        messagebox.showerror("Create Bill", "Name cannot be empty")
        window_name.focus_force()
    else:
        SetCustomerName(name)
        WriteBill()
        messagebox.showinfo("Bill", "Bill Created")
        DestroyWindow(window_name)
        ClearTreeview(TreeviewName)
        ResetItemsBtn(InventoryTree)
        formatted_grand_total = "{:.2f}".format(Grand_Total)

        # Update the Label with the formatted value
        LabelName['text'] = formatted_grand_total


def ViewBillFrameWidgets(FrameName):
    global ActivityTree
    ViewBillHolder = LabelFrame(FrameName, text="View Bills", width=1000, bg=LoginPageTheme1)
    ViewBillHolder.pack(fill="both", side=RIGHT)
    ViewBillHolder.pack_propagate(False)
    StyleTTK(FrameName)
    Columns = ("sno", "icode", "iname", "rate", "qty", "price")
    ViewBillTree = ttk.Treeview(ViewBillHolder, columns=Columns, show="headings", style="mystyle1.Treeview")
    ViewBillTree.tag_configure('nonstylized', background=LoginPageTheme1)
    ViewBillTree.column("sno", anchor=CENTER, width=40)
    ViewBillTree.column("icode", anchor=CENTER, width=40)
    ViewBillTree.column("iname", anchor=CENTER, width=40)
    ViewBillTree.column("rate", anchor=CENTER, width=40)
    ViewBillTree.column("qty", anchor=CENTER, width=40)
    ViewBillTree.column("price", anchor=CENTER, width=40)
    ViewBillTree.heading("sno", text="Serial No.")
    ViewBillTree.heading("icode", text="Item_Code")
    ViewBillTree.heading("iname", text="Item_Name")
    ViewBillTree.heading("rate", text="Rate")
    ViewBillTree.heading("qty", text="Quantity")
    ViewBillTree.heading("price", text="Price")

    ViewBillTree.pack(fill="both", expand=True, side=TOP, padx=10, pady=(5, 5))

    ButtonHoldFrame = Frame(ViewBillHolder)
    ButtonHoldFrame.pack(side=BOTTOM)

    ReturnBtn = Button(ButtonHoldFrame, text="Return To Billing Page", font=Font4, bg=LoginPageTheme1,
                       relief=SOLID,
                       command=lambda: FrameRaise(BillingFrame))
    ReturnBtn.grid(row=0, column=0)

    RetBtn = Button(ButtonHoldFrame, text="Return To Previous Tab", font=Font4, bg=LoginPageTheme1, relief=SOLID,
                    command=lambda: FrameRaise(PreviousTopFrame))
    RetBtn.grid(row=0, column=1)
    # ================================================================================================================ #
    WidgetHolder = LabelFrame(FrameName, text="Search by ID", width=1000, bg=LoginPageTheme1)
    WidgetHolder.pack(side=LEFT, fill="both")
    Label(WidgetHolder, text="Search Bill", font=Font1, bg=TreeviewBackgroundTheme1, relief=SOLID, width=15).place(
        x=-20, y=50)
    IDEntry = Entry(WidgetHolder, font=Font3, relief=SOLID, bg=TreeviewBackgroundTheme1)
    IDEntry.place(x=20, y=200)
    IDSearchButton = Button(WidgetHolder, text="Search", font=Font3, bg=TreeviewBackgroundTheme1,
                            activebackground=LoginPageTheme1, relief=SOLID,
                            command=lambda: GetBillButton(IDEntry.get(), ViewBillTree, NameLabel, IDLabel, TimeLabel,
                                                          GrandTotalLabel))
    IDSearchButton.place(x=370, y=190)
    Label(WidgetHolder, text="Customer Name: ", font=Font3, bg=LoginPageTheme1).place(x=20, y=320)
    Label(WidgetHolder, text="Customer ID: ", font=Font3, bg=LoginPageTheme1).place(x=20, y=400)
    Label(WidgetHolder, text="Creation Time: ", font=Font3, bg=LoginPageTheme1).place(x=20, y=480)
    Label(WidgetHolder, text="Grand Total: ", font=Font3, bg=LoginPageTheme1).place(x=20, y=560)
    NameLabel = Label(WidgetHolder, text="", font=Font3, bg=LoginPageTheme1)
    NameLabel.place(x=250, y=320)
    IDLabel = Label(WidgetHolder, text="", font=Font3, bg=LoginPageTheme1)
    IDLabel.place(x=250, y=400)
    TimeLabel = Label(WidgetHolder, text="", font=Font3, bg=LoginPageTheme1)
    TimeLabel.place(x=250, y=480)
    GrandTotalLabel = Label(WidgetHolder, text="", font=Font3, bg=LoginPageTheme1)
    GrandTotalLabel.place(x=250, y=560)
    ResetViewBillButton = Button(WidgetHolder, text="Reset", font=Font3, bg=TreeviewBackgroundTheme1,
                                 activebackground=LoginPageTheme1, relief=SOLID,
                                 command=lambda: (
                                     ClearTreeview(ViewBillTree), NameLabel.config(text=""), IDLabel.config(text=""),
                                     GrandTotalLabel.config(text=""), TimeLabel.config(text="")))
    ResetViewBillButton.place(x=200, y=650)


def GetBillButton(tablename, TreeviewName, NameLabel, IDLabel, GrandTotalLabel, TimeLabel):
    billcursor.execute('SHOW TABLES')
    tables = billcursor.fetchall()
    for item in tables:
        if item[0] == tablename.lower() or item[0] == tablename.upper():
            data = GetBill(tablename)
            InsertIntoViewBillTree(TreeviewName, data)
            mycursor.execute("SELECT * FROM customername WHERE customerid LIKE %s", (tablename,))
            customer_data = mycursor.fetchall()[0]
            NameLabel['text'] = customer_data[0]
            IDLabel['text'] = customer_data[1]
            GrandTotalLabel['text'] = customer_data[2]
            TimeLabel['text'] = customer_data[3]
            return None
    else:
        messagebox.showinfo("Bill", "ID not found")


def InsertIntoViewBillTree(TreeviewName, records):
    for i in TreeviewName.get_children():
        TreeviewName.delete(i)
    for item in records:
        if int(item[0]) % 2 == 0:
            TreeviewName.insert(parent="", index="end", values=item)
        else:
            TreeviewName.insert(parent="", index="end", values=item, tags="nonstylized")


def GetTextIntoEntry(NameLabel, CodeLabel, RateLabel, StocksLabel, TreeviewName):
    records = TreeviewSelectionValueObtain(TreeviewName)
    print(records)
    if records is None:
        pass
    elif len(records) > 1:
        messagebox.showinfo("Selection", "Only one record can be selected at a time")
    else:
        value_list = records[0]
        NameLabel.delete(0, END)
        CodeLabel.delete(0, END)
        RateLabel.delete(0, END)
        StocksLabel.delete(0, END)
        NameLabel.insert(0, value_list[2])
        CodeLabel.insert(0, value_list[1])
        RateLabel.insert(0, value_list[3])
        StocksLabel.insert(0, value_list[4])




def generate_and_display_qr_code(parent_window, text):
    # Create a QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convert the PIL Image to a PhotoImage
    photo = ImageTk.PhotoImage(qr_img)

    # Create a label to display the QR code in the parent window
    qr_label = Label(parent_window, image=photo)
    qr_label.photo = photo  # To prevent it from being garbage collected
    qr_label.pack()