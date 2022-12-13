import datetime
from tkinter import *
import tkinter.messagebox as mb
from tkinter import ttk
from tkcalendar import DateEntry
import sqlite3

#Creating the universal font variables
headlabelfont = ("Calibri", 15, 'bold')
labelfont = ('Calibri', 14)
entryfont = ('Calibri', 12)

#Connecting to the Database where all information will be stored
#Creating DB
connector = sqlite3.connect('DonorsDataBase.db')
cursor = connector.cursor()
connector.execute(
"CREATE TABLE IF NOT EXISTS DONORS_MANAGEMENT (DONORS_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, NAME TEXT, EMAIL TEXT, PHONE_NO TEXT, STATUS TEXT, DOD TEXT, MONEY TEXT, TYPE TEXT)")


#Functios For Reset, View, Display, Insert, Delete DB, Delete Record

def reset_fields():
   global name_strvar, email_strvar, contact_strvar, status_strvar, dod, money_strvar, type_strvar
   for i in ['name_strvar', 'email_strvar', 'contact_strvar', 'status_strvar', 'money_strvar', 'type_strvar']:
       exec(f"{i}.set('')")
   dod.set_date(datetime.datetime.now().date())

def reset_form():
   global tree
   tree.delete(*tree.get_children())
   reset_fields()

def display_records():
   tree.delete(*tree.get_children())
   curr = connector.execute('SELECT * FROM DONORS_MANAGEMENT')
   data = curr.fetchall()
   for records in data:
       tree.insert('', END, values=records)

def add_record():
   global name_strvar, email_strvar, contact_strvar, status_strvar, dod, money_strvar, type_strvar
   name = name_strvar.get()
   email = email_strvar.get()
   contact = contact_strvar.get()
   status = status_strvar.get()
   DOD = dod.get_date()
   money = money_strvar.get()
   type = type_strvar.get()
   if not name or not email or not contact or not status or not DOD or not money or not type:
       mb.showerror('Error!', "Please fill all the missing fields!")
   else:
       try:
           connector.execute(
           'INSERT INTO DONORS_MANAGEMENT (NAME, EMAIL, PHONE_NO, STATUS, DOD, MONEY, TYPE) VALUES (?,?,?,?,?,?,?)', (name, email, contact, status, DOD, money, type))
           connector.commit()
           mb.showinfo('Record added', f"Record of {name} was successfully added")
           reset_fields()
           display_records()
       except:
           mb.showerror('Wrong type', 'The type of the values entered is not accurate. Pls note that the contact field can only contain numbers')


def remove_record():
   if not tree.selection():
       mb.showerror('Error!', 'Please select an item from the database')
   else:
       current_item = tree.focus()
       values = tree.item(current_item)
       selection = values["values"]
       tree.delete(current_item)
       connector.execute('DELETE FROM DONORS_MANAGEMENT WHERE DONORS_ID=%d' % selection[0])
       connector.commit()
       mb.showinfo('Done', 'The record you wanted deleted was successfully deleted.')
       display_records()


def view_record():
   global name_strvar, email_strvar, contact_strvar, status_strvar, dod, money_strvar, type_strvar
   current_item = tree.focus()
   values = tree.item(current_item)
   selection = values["values"]
   date = datetime.date(int(selection[5][:4]), int(selection[5][5:7]), int(selection[5][8:]))
   name_strvar.set(selection[1]); email_strvar.set(selection[2])
   contact_strvar.set(selection[3]); status_strvar.set(selection[4])
   dod.set_date(date); money_strvar.set(selection[6]); type_strvar.set(selection[4])

def update_record():
   global name_strvar, email_strvar, contact_strvar, status_strvar, dod, money_strvar, type_strvar
   current_item = tree.focus()
   values = tree.item(current_item)
   selection = values["values"]

   global name_strvar, email_strvar, contact_strvar, status_strvar, dod, money_strvar, type_strvar
   name = name_strvar.get()
   email = email_strvar.get()
   contact = contact_strvar.get()
   status = status_strvar.get()
   DOD = dod.get_date()
   money = money_strvar.get()
   type = type_strvar.get()
   if not name or not email or not contact or not status or not DOD or not money or not type:
       mb.showerror('Error!', "Please fill all the missing fields!")
   else:
       try:
           connector.execute(
           'UPDATE DONORS_MANAGEMENT SET NAME = ?, EMAIL = ?, PHONE_NO = ?, STATUS = ?, DOD = ?, MONEY = ?, TYPE=?  WHERE DONORS_ID = ?', (name, email, contact, status, DOD, money, type, selection[0]))
           connector.commit()
           mb.showinfo('Record updated', f"Record of {name} was successfully added")
           reset_fields()
           display_records()
       except:
           mb.showerror('Wrong type', 'The type of the values entered is not accurate. Please note that the contact field can only contain numbers')

def search_record():
    global name_userID
    userID = name_userID.get()
    if not userID:
        mb.showerror('Error!', 'No user ID Input')
    else:
        try:
            tree.delete(*tree.get_children())
            curr = connector.execute('SELECT * FROM DONORS_MANAGEMENT WHERE DONORS_ID = ?', (userID,))

            connector.commit()
            reset_fields()
            data = curr.fetchall()
            for records in data:
                tree.insert('', END, values=records)
            #display_records()
        except:
            mb.showerror('Wrong type',
                         'The type of the values entered is not accurate. Please note that the contact field can only contain numbers')

#Initializing the GUI window
main = Tk()
main.title('Donors Management')
main.geometry('1600x1000')
main.resizable(0,0)
main.iconbitmap(r'DonateIcon.ico')


#Creating the background and foreground color variables
lf_bg = '#DCE2EC'
cf_bg = '#E4E9F1'

#Creating the StringVar or IntVar variables
name_strvar = StringVar()
email_strvar = StringVar()
contact_strvar = StringVar()
status_strvar = StringVar()
money_strvar = StringVar()
type_strvar = StringVar()
name_userID = StringVar()

#Placing the components in the main window
Label(main, text="DONORS MANAGEMENT SYSTEM", font=headlabelfont, bg='#0d324d', fg='White').pack(side=TOP, fill=X)
left_frame = Frame(main, bg=lf_bg)
left_frame.place(x=0, y=30, relheight=1, relwidth=0.2)
center_frame = Frame(main, bg=cf_bg)
center_frame.place(relx=0.2, y=30, relheight=1, relwidth=0.2)
right_frame = Frame(main, bg="Gray35")
right_frame.place(relx=0.4, y=30, relheight=1, relwidth=0.6)


#Placing components in the left frame

#Label Text
Label(left_frame, text="Full Name", font=labelfont, bg=lf_bg).place(relx=0.100, rely=0.010)
Label(left_frame, text="Email Address", font=labelfont, bg=lf_bg).place(relx=0.100, rely=0.07)
Label(left_frame, text="Contact number", font=labelfont, bg=lf_bg).place(relx=0.100, rely=0.13)
Label(left_frame, text="Status", font=labelfont, bg=lf_bg).place(relx=0.100, rely=0.39)
Label(left_frame, text="Donors Donation", font=labelfont, bg=lf_bg).place(relx=0.100, rely=0.20)
Label(left_frame, text="Date of donation", font=labelfont, bg=lf_bg).place(relx=0.100, rely=0.33)
Label(left_frame, text="Money Donation", font=labelfont, bg=lf_bg).place(relx=0.100, rely=0.267)

#Text Entry
Entry(left_frame, width=19, textvariable=name_strvar, font=entryfont).place(x=20, rely=0.04)
Entry(left_frame, width=19, textvariable=contact_strvar, font=entryfont).place(x=20, rely=0.16)
Entry(left_frame, width=19, textvariable=email_strvar, font=entryfont).place(x=20, rely=0.10)
Entry(left_frame, width=19, textvariable=money_strvar, font=entryfont).place(x=20, rely=0.30)
OptionMenu(left_frame, status_strvar, 'Delivered', 'Delivering','In-Stock').place(x=20, rely=0.423, relwidth=0.5)
OptionMenu(left_frame, type_strvar, 'Can Goods', 'Clothings', 'Both').place(x=20, rely=0.230, relwidth=0.5)
dod = DateEntry(left_frame, font=("Arial", 12), width=15)
dod.place(x=20, rely=0.36)
Button(left_frame, text='Register', font=labelfont, command=add_record, width=18).place(relx=0.025, rely=0.85)


#Placing components in the center frame (Tree View)
Button(center_frame, text='Delete Record', font=labelfont, command=remove_record, width=15).place(relx=0.1, rely=0.50)
Button(center_frame, text='View Record', font=labelfont, command=view_record, width=15).place(relx=0.1, rely=0.10)
Button(center_frame, text='Reset Fields', font=labelfont, command=reset_fields, width=15).place(relx=0.1, rely=0.15)
Button(center_frame, text='Delete database', font=labelfont, command=reset_form, width=15).place(relx=0.1, rely=0.45)
Button(center_frame, text='Display Records', font=labelfont, command=display_records, width=15).place(relx=0.1, rely=0.33)
Button(center_frame, text='Update Record', font=labelfont, command=update_record, width=15).place(relx=0.1, rely=0.05)
Entry(center_frame, width=19, textvariable=name_userID, font=entryfont).place(relx=0.1, rely=0.30)
Button(center_frame, text='Search', font=labelfont, command=search_record, width=15).place(relx=0.1, rely=0.25)



#Placing components in the right frame (Tree View)
Label(right_frame, text='Donors Records', font=headlabelfont, bg='#313639', fg='White').pack(side=TOP, fill=X)
tree = ttk.Treeview(right_frame, height=100, selectmode=BROWSE,
                   columns=('DONORS ID', "Name", "Email Address", "Contact Number", "Status", "Date of Donation", "Money", 'Type'))
X_scroller = Scrollbar(tree, orient=HORIZONTAL, command=tree.xview)
Y_scroller = Scrollbar(tree, orient=VERTICAL, command=tree.yview)
X_scroller.pack(side=BOTTOM, fill=X)
Y_scroller.pack(side=RIGHT, fill=Y)
tree.config(yscrollcommand=Y_scroller.set, xscrollcommand=X_scroller.set)
tree.heading('DONORS ID', text='ID', anchor=CENTER)
tree.heading('Name', text='Name', anchor=CENTER)
tree.heading('Email Address', text='Email ID', anchor=CENTER)
tree.heading('Contact Number', text='Phone No', anchor=CENTER)
tree.heading('Status', text='Status', anchor=CENTER)
tree.heading('Date of Donation', text='Date of donation', anchor=CENTER)
tree.heading('Money', text='Amount of Money', anchor=CENTER)
tree.heading('Type', text='Type', anchor=CENTER)

tree.column('#0', width=0, stretch=NO)
tree.column('#1', width=40, stretch=NO)
tree.column('#2', width=140, stretch=NO)
tree.column('#3', width=200, stretch=NO)
tree.column('#4', width=80, stretch=NO)
tree.column('#5', width=80, stretch=NO)
tree.column('#6', width=150, stretch=NO)
tree.column('#7', width=150, stretch=NO)
tree.column('#8', width=80, stretch=NO)

tree.place(y=30, relwidth=1, relheight=0.9, relx=0)
display_records()

#Finalizing the GUI window
main.update()
main.mainloop()