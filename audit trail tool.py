import tkinter as tk
from tkinter import *
from tkinter import messagebox
import audit_trail_adder

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Send it"
        self.hi_there["command"] = self.do_tha_thing
        self.hi_there["width"]=120
        self.hi_there.grid(row=10,column=0,columnspan=2)

        self.waittime = tk.Entry(self, width=100, textvariable=StringVar(self,'2'))
        self.waittime.grid(row=0,column=1,padx=5,pady=5)
        self.waittimelabel = tk.Label(self, width=20, text="Wait time")
        self.waittimelabel.grid(row=0,column=0)

        self.username = tk.Entry(self, width=100)
        self.username.grid(row=1,column=1,padx=5,pady=5)
        self.usernamelabel = tk.Label(self, width=20, text="User name")
        self.usernamelabel.grid(row=1,column=0)

        self.password = tk.Entry(self, width=100, show='*')
        self.password.grid(row=2,column=1,padx=5,pady=5)
        self.passwordlabel = tk.Label(self, width=20, text="Password")
        self.passwordlabel.grid(row=2,column=0)

        self.sosymid = tk.Entry(self, width=100)
        self.sosymid.grid(row=3,column=1,padx=5,pady=5)
        self.sosymlabel = tk.Label(self, width=20, text="SoSyM Manuscript ID")
        self.sosymlabel.grid(row=3,column=0)

        self.fromentry = tk.Entry(self, width=100)
        self.fromentry.grid(row=4,column=1,padx=5,pady=5)
        self.fromlabel = tk.Label(self, width=20, text="From")
        self.fromlabel.grid(row=4,column=0)

        self.toentry = tk.Entry(self, width=100)
        self.toentry.grid(row=5,column=1,padx=5,pady=5)
        self.tolabel = tk.Label(self, width=20, text="To")
        self.tolabel.grid(row=5,column=0)

        self.subjectentry = tk.Entry(self, width=100)
        self.subjectentry.grid(row=6,column=1,padx=5,pady=5)
        self.subjectlabel = tk.Label(self, width=20, text="Subject")
        self.subjectlabel.grid(row=6,column=0)

        self.bodyentry = tk.Text(self, width=100,height=10, wrap=None)
        self.bodyentry.grid(row=7,column=1,padx=5,pady=5)
        self.bodylabel = tk.Label(self, width=20, text="Body")
        self.bodylabel.grid(row=7,column=0)

    def do_tha_thing(self):

        result=audit_trail_adder.add(self.username.get().strip(),self.password.get().strip(),self.sosymid.get().strip(),self.toentry.get().strip(),self.fromentry.get().strip(),self.subjectentry.get().strip(),self.bodyentry.get("1.0","end").strip())
        messagebox.showinfo("Message",result)



root = tk.Tk()
root.title("Add Audit Trail")
app = Application(master=root)
app.mainloop()
