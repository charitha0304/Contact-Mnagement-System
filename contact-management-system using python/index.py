from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
root = Tk()
root.title("Contact List")
width = 700
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="yellow")

FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()

def Database():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS member (mem_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, gender TEXT, age TEXT, address TEXT, contact TEXT)")
    cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SubmitData():
    if not (FIRSTNAME.get() and LASTNAME.get() and GENDER.get() and AGE.get() and ADDRESS.get() and CONTACT.get()):
        tkMessageBox.showwarning('', 'Please Complete The Required Fields', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO member (firstname, lastname, gender, age, address, contact) VALUES (?, ?, ?, ?, ?, ?)",
                       (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), ADDRESS.get(), CONTACT.get()))
        conn.commit()
        cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        clear_fields()

def UpdateData():
    if not GENDER.get():
        tkMessageBox.showwarning('', 'Please Complete The Required Fields', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("contacts.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE member SET firstname = ?, lastname = ?, gender = ?, age = ?, address = ?, contact = ? WHERE mem_id = ?",
                       (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), ADDRESS.get(), CONTACT.get(), mem_id))
        conn.commit()
        cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        clear_fields()

def clear_fields():
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")

def OnSelected(event):
    global mem_id, UpdateWindow
    curItem = tree.focus()
    contents = tree.item(curItem)
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    clear_fields()
    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    GENDER.set(selecteditem[3])
    AGE.set(selecteditem[4])
    ADDRESS.set(selecteditem[5])
    CONTACT.set(selecteditem[6])
    UpdateWindow = Toplevel()
    UpdateWindow.title("Update Contact")
    width = 400
    height = 300
    x = ((screen_width / 2) + 450) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    UpdateWindow.resizable(0, 0)
    if 'NewWindow' in globals():
        NewWindow.destroy()

    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(UpdateWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('serif', 14)).pack(side=LEFT)
    Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('serif', 14)).pack(side=LEFT)
    
    Label(FormTitle, text="Updating Contacts", font=('serif', 16), bg="#3d85c6", width=300).pack(fill=X)
    Label(ContactForm, text="Firstname", font=('serif', 14), bd=5).grid(row=0, sticky=W)
    Label(ContactForm, text="Lastname", font=('serif', 14), bd=5).grid(row=1, sticky=W)
    Label(ContactForm, text="Gender", font=('serif', 14), bd=5).grid(row=2, sticky=W)
    Label(ContactForm, text="Age", font=('serif', 14), bd=5).grid(row=3, sticky=W)
    Label(ContactForm, text="Address", font=('serif', 14), bd=5).grid(row=4, sticky=W)
    Label(ContactForm, text="Contact", font=('serif', 14), bd=5).grid(row=5, sticky=W)

    Entry(ContactForm, textvariable=FIRSTNAME, font=('serif', 14)).grid(row=0, column=1)
    Entry(ContactForm, textvariable=LASTNAME, font=('serif', 14)).grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    Entry(ContactForm, textvariable=AGE, font=('serif', 14)).grid(row=3, column=1)
    Entry(ContactForm, textvariable=ADDRESS, font=('serif', 14)).grid(row=4, column=1)
    Entry(ContactForm, textvariable=CONTACT, font=('serif', 14)).grid(row=5, column=1)

    Button(ContactForm, text="Update", width=50, command=UpdateData).grid(row=6, columnspan=2, pady=10)

def DeleteData():
    if not tree.selection():
        tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = tree.item(curItem)
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("contacts.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM member WHERE mem_id = ?", (selecteditem[0],))
            conn.commit()
            cursor.close()
            conn.close()

def AddNewWindow():
    global NewWindow
    clear_fields()
    NewWindow = Toplevel()
    NewWindow.title("Add New Contact")
    width = 400
    height = 300
    x = ((screen_width / 2) - 455) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    NewWindow.resizable(0, 0)
    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()


    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('serif', 14)).pack(side=LEFT)
    Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('serif', 14)).pack(side=LEFT)
    
    Label(FormTitle, text="Adding New Contacts", font=('serif', 16), bg="#66ff66", width=300).pack(fill=X)
    Label(ContactForm, text="Firstname", font=('serif', 14), bd=5).grid(row=0, sticky=W)
    Label(ContactForm, text="Lastname", font=('serif', 14), bd=5).grid(row=1, sticky=W)
    Label(ContactForm, text="Gender", font=('serif', 14), bd=5).grid(row=2, sticky=W)
    Label(ContactForm, text="Age", font=('serif', 14), bd=5).grid(row=3, sticky=W)
    Label(ContactForm, text="Address", font=('serif', 14), bd=5).grid(row=4, sticky=W)
    Label(ContactForm, text="Contact", font=('serif', 14), bd=5).grid(row=5, sticky=W)

    Entry(ContactForm, textvariable=FIRSTNAME, font=('serif', 14)).grid(row=0, column=1)
    Entry(ContactForm, textvariable=LASTNAME, font=('serif', 14)).grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    Entry(ContactForm, textvariable=AGE, font=('serif', 14)).grid(row=3, column=1)
    Entry(ContactForm, textvariable=ADDRESS, font=('serif', 14)).grid(row=4, column=1)
    Entry(ContactForm, textvariable=CONTACT, font=('serif', 14)).grid(row=5, column=1)

    Button(ContactForm, text="Save", width=50, command=SubmitData).grid(row=6, columnspan=2, pady=10)

Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500, bg="yellow")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg="yellow")
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)

Label(Top, text="Contact Details", font=('serif', 16), width=500).pack(fill=X)

Button(MidLeft, text="Add New Contact Info", bg="green", fg="white",command=AddNewWindow).pack()
Button(MidRight, text="Delete Contact Info", bg="red",fg="white", command=DeleteData).pack(side=RIGHT)

scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("MemberID", "Firstname", "Lastname", "Gender", "Age", "Address", "Contact"), height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)


style = ttk.Style()

style.configure("Treeview",

                borderwidth=2,

                relief="solid")

style.configure("Treeview.Heading",

                borderwidth=2,

                relief="solid")

style.configure("Treeview",

                background="#f0f0f0",

                foreground="black",

                fieldbackground="#f0f0f0")

style.map('Treeview',

          background=[('selected', '#d9ead3')],

          foreground=[('selected', 'black')])

tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Firstname', text="Firstname", anchor=W)
tree.heading('Lastname', text="Lastname", anchor=W)
tree.heading('Gender', text="Gender", anchor=W)
tree.heading('Age', text="Age", anchor=W)
tree.heading('Address', text="Address", anchor=W)
tree.heading('Contact', text="Contact", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0,  anchor=W)
tree.column('#1', stretch=NO, minwidth=0, width=0, anchor=W)
tree.column('#2', stretch=NO, minwidth=0, width=80, anchor=W)
tree.column('#3', stretch=NO, minwidth=0, width=120, anchor=W)
tree.column('#4', stretch=NO, minwidth=0, width=90, anchor=W)
tree.column('#5', stretch=NO, minwidth=0, width=80,anchor=W)
tree.column('#6', stretch=NO, minwidth=0, width=120, anchor=W)
tree.column('#7', stretch=NO, minwidth=0, width=120, anchor=W)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

if __name__ == '__main__':
    Database()
    root.mainloop()
