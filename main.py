from tkinter import *
from tkinter import ttk
import tkinter as tk
from PIL import ImageTk, Image
import pyperclip
import time
import threading
import os
import hashlib
import pykeepass
from pykeepass import PyKeePass, create_database

class Window():
    def __init__(self,filename,password_user): #definition de la classe ainsi que de ses parametres(filename et passoword user)
        self.tk = Tk()
        self.tk.title("Password Manager")
        self.tk.geometry("1350x750")
        self.tk.resizable(0, 0)
        self.tk.configure(background='#2832C2')
        self.ttk = ttk.Style()
        self.ttk.theme_use('clam')
        self.ttk.configure("green.Horizontal.TProgressbar", background='#90ee90')
        
        self.filename = filename #recuperation des parametres filename password user
        self.password = password_user
        self.kp = None
        self.increment_id = 1
        
        self.trv = None
        self.secondary_window = None
        self.entry_website = None
        self.entry_categ = None
        self.entry_user = None
        self.entry_pass = None
        
        self.copier_img = ImageTk.PhotoImage(file="imgs/copy.png") #emplacement des logos graphiques
        self.ajouter_img = ImageTk.PhotoImage(file="imgs/ajouter.png")
        self.supprimer_img = ImageTk.PhotoImage(file="imgs/poubelle.png")
        
        self.create_header()
        self.display()
            
        self.tk.mainloop()
    
    def create_header(self):
        self.btn_delete= Button(self.tk,
                      command=self.delete,
                      image=self.supprimer_img,
                      borderwidth=0,
                      highlightthickness=0,
                      background="#2832C2",
                      activebackground="#0A1172")
        self.btn_delete.place(x=1290, y=20,width=40,height=40)
        
        self.btn_ajouter= Button(self.tk,
                      command=self.ajouter,
                      image=self.ajouter_img,
                      borderwidth=0,
                      highlightthickness=0,
                      background="#2832C2",
                      activebackground="#0A1172")
        self.btn_ajouter.place(x=1230, y=20,width=40,height=40)
        
        self.btn_copier= Button(self.tk,
                      command=self.copierWindow,
                      image=self.copier_img,
                      borderwidth=0,
                      highlightthickness=0,
                      background="#2832C2",
                      activebackground="#0A1172")
        self.btn_copier.place(x=1170, y=20,width=40,height=40)
    
    def copierWindow(self): 
        self.secondary_window = Toplevel()
        self.secondary_window.title("Copy")
        self.secondary_window.config(width=300, height=100)
        self.secondary_window.grab_set()
        button_user = ttk.Button(
            self.secondary_window,
            text="Copier le User",
            command=lambda: self.copier("user")
        )
        button_user.place(x=100, y=20)
        button_password = ttk.Button(
            self.secondary_window,
            text="Copier le Password",
            command=lambda: self.copier("pass")
        )
        button_password.place(x=85, y=60)
        
    def copier(self,copy):
        if(self.trv.focus()!=""):
            if(copy=="user"):
                item = self.trv.item(self.trv.focus())
                pyperclip.copy(item['values'][3])
                self.secondary_window.destroy()
                progress = ttk.Progressbar(self.tk, orient=HORIZONTAL, length=750, mode='determinate',
                                   value=0,style="green.Horizontal.TProgressbar")
                progress.place(x=300, y=720, height=20)
                for i in range(1, 16):
                    progress['value'] += 7
                    self.tk.update_idletasks()
                    time.sleep(1)
                progress.destroy()
                pyperclip.copy("")
            elif(copy=="pass"):
                item = self.trv.item(self.trv.focus())
                pyperclip.copy(item['values'][4])
                self.secondary_window.destroy()
                progress = ttk.Progressbar(self.tk, orient=HORIZONTAL, length=750, mode='determinate',
                                   value=0,style="green.Horizontal.TProgressbar")
                progress.place(x=300, y=720, height=20)
                for i in range(1, 16):
                    progress['value'] += 7
                    self.tk.update_idletasks()
                    time.sleep(1)
                progress.destroy()
                pyperclip.copy("")
        else:
            self.secondary_window.destroy()
        
    def delete(self):
        if(self.trv.focus()!=""):
            self.kp.delete_entry(self.kp.find_entries(notes=str(self.trv.focus()))[0])
            self.kp.save()
            self.trv.delete(self.trv.focus())


    def ajouter(self):
        self.secondary_window = Toplevel()
        self.secondary_window.title("Copy")
        self.secondary_window.config(width=300, height=400)
        self.secondary_window.grab_set()
        
        label_website = ttk.Label(self.secondary_window,text="Site",foreground="#000000", font=("Berlin Sans fb demi", 12))
        label_website.place(x=50, y=50)
        label_categ = ttk.Label(self.secondary_window,text="Catégorie",foreground="#000000", font=("Berlin Sans fb demi", 12))
        label_categ.place(x=50, y=100)
        label_pass = ttk.Label(self.secondary_window,text="User",foreground="#000000", font=("Berlin Sans fb demi", 12))
        label_pass.place(x=50, y=150)
        label_user = ttk.Label(self.secondary_window,text="Password",foreground="#000000", font=("Berlin Sans fb demi", 12))
        label_user.place(x=50, y=200)
        
        self.entry_website = ttk.Entry(self.secondary_window,font=("Berlin Sans fb demi", 12))
        self.entry_website.place(x=100, y=50,width=100,height=30)

        self.entry_categ = ttk.Entry(self.secondary_window,font=("Berlin Sans fb demi", 12))
        self.entry_categ.place(x=150, y=100,width=100,height=30)

        self.entry_user = ttk.Entry(self.secondary_window,font=("Berlin Sans fb demi", 12))
        self.entry_user.place(x=100, y=150,width=150,height=30)

        self.entry_pass = ttk.Entry(self.secondary_window,font=("Berlin Sans fb demi", 12))
        self.entry_pass.place(x=150, y=200,width=100,height=30)
        
        button_close = ttk.Button(
            self.secondary_window,
            text="Close",
            command=self.secondary_window.destroy
        )
        button_close.place(x=100, y=280)
        button_add = ttk.Button(
            self.secondary_window,
            text="Ajouter",
            command=self.ajouter_mdp
        )
        button_add.place(x=40, y=330,width=230,height=50)
    
    def ajouter_mdp(self):
        site = self.entry_website.get()
        categ = self.entry_categ.get()
        user = self.entry_user.get()
        password = self.entry_pass.get()
        
        if(site!="" and categ!="" and user!="" and password!=""):
            self.kp.add_entry(self.kp.root_group,categ,user,password,url=site,notes=str(self.increment_id))
            self.kp.save()
            self.trv.insert("", 'end',iid=str(self.increment_id), text=str(self.increment_id),values =(str(self.increment_id),site,categ,user,password,""))
            self.increment_id += 1
            self.secondary_window.destroy()
        
    def display(self):
        self.trv = ttk.Treeview(self.tk, selectmode ='browse',height=30)
        self.trv.grid(row=1,column=1,padx=20,pady=80)

        self.trv["columns"] = ("1", "2", "3","4","5")

        self.trv['show'] = 'headings'

        self.trv.column("1", width = 50, anchor ='c')
        self.trv.column("2", width = 500, anchor ='c')
        self.trv.column("3", width = 250, anchor ='c')
        self.trv.column("4", width = 250, anchor ='c')
        self.trv.column("5", width = 250, anchor ='c')

        self.trv.heading("1", text ="id")
        self.trv.heading("2", text ="Website/ Name")
        self.trv.heading("3", text ="Categorie")
        self.trv.heading("4", text ="User")  
        self.trv.heading("5", text ="Password")
        
        self.kp = PyKeePass(self.filename, password=self.password)
        
        for entry in self.kp.entries:
            self.trv.insert("", 'end',iid=str(self.increment_id), text=str(self.increment_id),
                   values =(str(self.increment_id),entry.url,entry.title,entry.username,entry.password,""))
            self.increment_id += 1

class Login():
    def __init__(self):
        self.tk = Tk()
        self.tk.title("Password Manager")
        self.tk.geometry("1350x750")
        self.tk.resizable(0, 0)
        self.tk.configure(background='#2832C2')
        
        self.basepath = ('./pass')
        self.Title = None
        self.user_title = None
        self.user_entry = None
        self.pass_title = None
        self.pass_entry = None
        self.error_msg = None
        self.btn_login = None
        self.exist = None
        self.error = StringVar()
        self.error.set("")
        
        self.build_interface()
        
        self.tk.mainloop()
        
    def login_user(self):
        self.user = hashlib.md5(self.user_entry.get().encode())
        self.name_user_crypt = None
        self.user_pass = self.pass_entry.get()
        for entry in os.listdir(self.basepath):
            if os.path.isfile(os.path.join(self.basepath, entry)):
                if (entry.replace(".kdbx","")==self.user.hexdigest()):
                    self.exist = True
                    self.name_user_crypt = str(self.user.hexdigest())
        if (self.exist):
            self.filename="./pass/"+ str(self.user.hexdigest()) + ".kdbx"
            try:
                self.kp = PyKeePass(self.filename, password=self.pass_entry.get())
                self.tk.destroy()
                self.kp.save()
                new = Window(self.filename,self.user_pass)
            except pykeepass.exceptions.CredentialsError:
                self.error.set("Bad password or user")
                
        else:
            self.filename="./pass/"+ str(self.user.hexdigest()) + ".kdbx"
            create_database(self.filename, password=self.pass_entry.get(), keyfile=None, transformed_key=None)
            self.tk.destroy()
            new = Window(self.filename,self.user_pass)
    
    def build_interface(self):
        self.Title = Label(self.tk, text="Login",foreground="#ffffff", font=("Berlin Sans fb demi", 50),background="#2832C2")
        self.Title.place(x=580, y=100)

        self.user_title = Label(self.tk, text="user",foreground="#000000", font=("Berlin Sans fb demi", 25),background="#2832C2")
        self.user_title.place(x=400, y=240)
        self.user_entry = Entry(bd=0,bg="#ffffff",highlightthickness=0, font=("Berlin Sans fb demi", 16))
        self.user_entry.place(x=500, y=250,width=350,height=40)

        self.pass_title = Label(self.tk, text="password",foreground="#000000", font=("Berlin Sans fb demi", 25),background="#2832C2")
        self.pass_title.place(x=300, y=300)
        self.pass_entry = Entry(bd=0,bg="#ffffff",highlightthickness=0, font=("Berlin Sans fb demi", 16),show = '*')
        self.pass_entry.place(x=500, y=310,width=350,height=40)


        self.error_msg = Label(self.tk, textvariable=self.error,foreground="#D0312D", font=("Berlin Sans fb demi", 25),background="#2832C2")
        self.error_msg.place(x=480, y=450)
        
        self.btn_login = Button(self.tk,command=self.login_user,text="Validate",borderwidth=0,highlightthickness=0,background="#3CB043",activebackground="#03C04A")
        self.btn_login.place(x=580, y=380,width=200,height=40)

login = Login()