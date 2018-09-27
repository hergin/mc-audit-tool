import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os
import sys
from selenium import webdriver
from selenium.webdriver.support.select import Select
from datetime import date, datetime

WAIT_TIME = 2

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
        try:
            options = webdriver.ChromeOptions()

            WAIT_TIME = int(self.waittime.get().strip())

            options.add_argument('headless')

            # set the window size
            options.add_argument('window-size=1200x900')

            # initialize the driver
            driver = webdriver.Chrome(chrome_options=options)

            driver.get('https://mc.manuscriptcentral.com/sosym')

            # wait up to 10 seconds for the elements to become available
            driver.implicitly_wait(WAIT_TIME)

            # use css selectors to grab the login inputs
            email = driver.find_element_by_css_selector('input[name=USERID]')
            password = driver.find_element_by_css_selector('input[type=password]')
            login = driver.find_element_by_css_selector('a[id="logInButton"]')

            email.send_keys(self.username.get().strip())
            password.send_keys(self.password.get().strip())


            #driver.get_screenshot_as_file('main-page.png')

            # login
            login.click()


            driver.implicitly_wait(WAIT_TIME)
            # navigate to my profile
            #driver.get('https://www.facebook.com/profile.php?id=100009447446864')

            # take another screenshot
            #driver.get_screenshot_as_file('mc-main.png')

            adminCenter = driver.find_element_by_link_text('Manage')
            adminCenter.click()

            adminCenter = driver.find_element_by_link_text('Administration Center')
            adminCenter.click()

            driver.implicitly_wait(WAIT_TIME)
            #driver.get_screenshot_as_file('mc-admin.png')


            manuscriptID = driver.find_element_by_css_selector('input[name="MS_SEARCH_QUICK_MANUSCRIPT_ID"]')
            manuscriptID.send_keys(self.sosymid.get().strip())

            manuscriptID.send_keys(u'\ue007')

            #driver.get_screenshot_as_file('manuscript.png')

            

            manuscriptSelect = Select(driver.find_element_by_css_selector('select[name*="SEL_MANUSCRIPT_DETAILS_JUMP_TO_TAB"]'))

            manuscriptSelect.select_by_visible_text('View Audit Trail')

            driver.implicitly_wait(WAIT_TIME)
            #driver.get_screenshot_as_file('audittrail.png')



            auditDate = driver.find_element_by_css_selector('input[name=EMAIL_DATE_SENT]')
            auditDate.send_keys(date.today().strftime('%d-%b-%Y'))

            auditTo = driver.find_element_by_css_selector('input[name=EMAIL_TO]')
            auditTo.send_keys(self.toentry.get().strip())

            auditFrom = driver.find_element_by_css_selector('input[name=EMAIL_FROM]')
            auditFrom.send_keys(self.fromentry.get().strip())

            auditSubject = driver.find_element_by_css_selector('input[name=EMAIL_SUBJECT]')
            auditSubject.send_keys(self.subjectentry.get().strip())

            auditBody = driver.find_element_by_css_selector('textarea[name=EMAIL_BODY]')
            auditBody.send_keys(self.bodyentry.get("1.0","end").strip())


            emailHourSelect = Select(driver.find_element_by_css_selector('select[name="EMAIL_HOUR_SENT"]'))
            emailHourSelect.select_by_visible_text(str(int(datetime.now().strftime('%I'))))

            emailMinuteSelect = Select(driver.find_element_by_css_selector('select[name="EMAIL_MINUTE_SENT"]'))
            emailMinuteSelect.select_by_visible_text(datetime.now().strftime('%M'))

            emailAMPMSelect = Select(driver.find_element_by_css_selector('select[name="EMAIL_AM_PM_SENT"]'))
            emailAMPMSelect.select_by_visible_text(datetime.now().strftime('%p'))


            driver.get_screenshot_as_file('audittrail_filled.png')

            addAuditTrailButton = driver.find_element_by_css_selector('td.dataentry > a[href*=\'MANUSCRIPT_DETAILS\']')

            result = messagebox.askokcancel("Finally","Everything seems to be working fine. Do you really want to add this audit entry?")

            if result:
                addAuditTrailButton.click()
                messagebox.showinfo("Success","Audit trail successfully added!")
            else:
                os.system('start audittrail_filled.png')

        except:
            messagebox.showerror("Error","Something happened on the way. Here are the details: " + str(sys.exc_info()))



root = tk.Tk()
root.title("Add Audit Trail")
app = Application(master=root)
app.mainloop()
