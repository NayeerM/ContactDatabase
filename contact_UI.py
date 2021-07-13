from sqlite3.dbapi2 import Cursor
from tkinter import Image, Tk, Button, PhotoImage, Label, LabelFrame, W, E,N,S, Entry, END, StringVar, Scrollbar, Toplevel, font, ttk
import sqlite3

class  Contacts:
    db_filename='contacts.db'
    def __init__(self,root):
        self.root=root
        self.create_GUI()
        ttk.style=ttk.Style()
        ttk.style.configure("Treeview",font=('helvetica',10))
        ttk.style.configure("Treeview.Heading",font=('helvetica',12,'bold'))

    def execute_db_query(self,query,parameters=()):
        with sqlite3.connect(self.db_filename) as conn:
            print(conn)
            print("Successfully connected")
            cursor=conn.cursor()
            query_result=cursor.execute(query,parameters)
            conn.commit()
        return query_result

    def add_new_contact(self):
        if self.new_contact_validated():
            query='INSERT INTO contacts_list VALUES(NULL,?,?,?)'
            parameters=(self.namefield.get(),self.emailfield.get(),self.numfield.get())
            self.execute_db_query(query,parameters)
            self.message['text']='New Contact {} added'.format(self.namefield.get())
            self.namefield.delete(0,END)
            self.emailfield.delete(0,END)
            self.numfield.delete(0,END)
            self.view_contacts()

        else:
            self.message['text']='name, email and number cannot be blank'
            self.view_contacts()
        
    def view_contacts(self):
        items=self.tree.get_children()
        print(items)
        for item in items:
            self.tree.delete(item)
        query='SELECT * FROM contacts_list ORDER BY name desc'
        contact_entries=self.execute_db_query(query)
        for row in contact_entries:
            self.tree.insert('',0,text=row[1],values=(row[2],row[3]))
    
    def new_contact_validated(self):
        return len(self.namefield.get())!=0 and len(self.emailfield.get())!=0 and len(self.numfield.get())!=0
    
 

    def create_GUI(self):
        self.create_left_icon()
        self.create_label_frame()
        self.MessageDisplay()
        self.create_tree_view()
        self.create_bottom_buttons()
        self.create_scrollBar()
        self.view_contacts()

    def MessageDisplay(self):
        self.message=Label(text='',fg='red')
        self.message.grid(row=3,column=1,sticky=W)

    def create_label_frame(self):
        labelframe=LabelFrame(self.root, text='Create New Contact', bg="sky blue", font="helvetica 10")
        labelframe.grid(row=0,column=1,padx=8,pady=8,sticky='ew')
        Label(labelframe,text='Name:',bg="green",fg="white").grid(row=1,column=1,sticky=W,pady=2,padx=15)
        self.namefield=Entry(labelframe)
        self.namefield.grid(row=1,column=2,sticky=W,padx=5,pady=2)
        Label(labelframe,text='Email:',bg="brown",fg="white").grid(row=2,column=1,sticky=W,pady=2,padx=15)
        self.emailfield=Entry(labelframe)
        self.emailfield.grid(row=2,column=2,sticky=W,padx=5,pady=2)
        Label(labelframe,text='Number:',bg="black",fg="white").grid(row=3,column=1,sticky=W,pady=2,padx=15)
        self.numfield=Entry(labelframe)
        self.numfield.grid(row=3,column=2,sticky=W,padx=5,pady=2)
        Button(labelframe, text='Add Contact', command=self.on_add_button_pressed,bg="blue",fg="white").grid(row=4,column=2,sticky=E,padx=5,pady=5)

    def create_tree_view(self):
        self.tree=ttk.Treeview(height=10,columns=('email','number'),style='Treeview')
        self.tree.grid(row=6,column=0,columnspan=3)
        self.tree.heading('#0',text='Name',anchor=W)
        self.tree.heading('email',text='Email Address', anchor=W)
        self.tree.heading('number',text='Contact Number', anchor=W)

    def create_left_icon(self):
        photo=PhotoImage(file='icon/logo.gif')
        label=Label(image=photo)
        label.image=photo
        label.grid(row=0,column=0)

    def create_bottom_buttons(self):
        Button(text='Delete',command=self.on_delete_button_pressed,bg="red",fg="white").grid(row=8,column=0,sticky=W,pady=10,padx=20)
        Button(text='Modify',command=self.on_modify_button_pressed,bg="purple",fg="white").grid(row=8,column=1,sticky=W,pady=10,padx=20)

    def on_add_button_pressed(self):
        self.add_new_contact()
    
    def on_delete_button_pressed(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text']='No item selected to delete'
            return
    
    def on_modify_button_pressed(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text']='No item selected to modify'
            return
            
        self.open_modify_window()

    def create_scrollBar(self):
        self.scrollbar=Scrollbar(orient='vertical',command=self.tree.yview)
        self.scrollbar.grid(row=6,column=3,sticky='sn',rowspan=10)
    
    def delete_Contacts(self):
        self.message['text']=''
        name=self.tree.item(self.tree.selection())['text']
        query='DELETE FROM contacts_list WHERE name=?'
        self.execute_db_query(query,(name,))
        self.message['text']='Contacts for {} deleted'.format(name)
        self.view_contacts()

    def open_modify_window(self):
        name=self.tree.item(self.tree.selection())['text']
        old_number=self.tree.item(self.tree.selection())['values'][1]
        old_email=self.tree.item(self.tree.selection())['values'][0]
        self.transient=Toplevel()
        self.transient.title('Update Contact')
        Label(self.transient, text='Name:').grid(row=0, column=1)
        Entry(self.transient,textvariable=StringVar(self.transient,value=name),state='readonly').grid(row=0,column=2)
        Label(self.transient, text='Old Contact Number:').grid(row=1, column=1)
        Entry(self.transient,textvariable=StringVar(self.transient,value=old_number),state='readonly').grid(row=1,column=2)
        
        Label(self.transient,text='New Phone Number:').grid(row=2,column=1)
        new_phoneno_entry_widget=Entry(self.transient)
        new_phoneno_entry_widget.grid(row=2,column=2)
        
        Label(self.transient, text='Old Email Address:').grid(row=3, column=1)
        Entry(self.transient,textvariable=StringVar(self.transient,value=old_email),state='readonly').grid(row=3,column=2)
        
        Label(self.transient,text='New Email Address:').grid(row=4,column=1)
        new_email_entry_widget=Entry(self.transient)
        new_email_entry_widget.grid(row=4,column=2)
        
        Button(self.transient,text='Update Contact', command=lambda:self.update_contacts(new_phoneno_entry_widget.get(),old_number,name,new_email_entry_widget.get(),old_email)).grid(row=5,column=2,sticky=E)
        
        self.transient.mainloop()
    
    def update_contacts(self,newphone,old_phone,name,new_email,old_email):
        query='UPDATE contacts_list SET number=?,email=? WHERE number=? AND email=? AND name=?'
        parameters=(newphone,new_email,old_phone,old_email,name)
        self.execute_db_query(query,parameters)
        self.transient.destroy()
        self.message['text']='Phone number of {} modified'.format(name)
        self.view_contacts()
        

if __name__=='__main__':
    root=Tk()
    root.title("Nayeer's Contact List")
    application=Contacts(root)
    root.mainloop()
           