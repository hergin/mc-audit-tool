import sys
from selenium import webdriver
from selenium.webdriver.support.select import Select
from datetime import date, datetime

def add(username, passwd, sosym_id, audit_to, audit_from, audit_subject, audit_body, WAIT_TIME = 3):

    try:
        options = webdriver.ChromeOptions()
    
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

        email.send_keys(username.strip())
        password.send_keys(passwd.strip())

        login.click()

        driver.implicitly_wait(WAIT_TIME)

        adminCenter = driver.find_element_by_link_text('Manage')
        adminCenter.click()

        adminCenter = driver.find_element_by_link_text('Administration Center')
        adminCenter.click()

        driver.implicitly_wait(WAIT_TIME)

        manuscriptID = driver.find_element_by_css_selector('input[name="MS_SEARCH_QUICK_MANUSCRIPT_ID"]')
        manuscriptID.send_keys(sosym_id.strip())

        manuscriptID.send_keys(u'\ue007')

        manuscriptSelect = Select(driver.find_element_by_css_selector('select[name*="SEL_MANUSCRIPT_DETAILS_JUMP_TO_TAB"]'))

        manuscriptSelect.select_by_visible_text('View Audit Trail')

        driver.implicitly_wait(WAIT_TIME)

        auditDate = driver.find_element_by_css_selector('input[name=EMAIL_DATE_SENT]')
        auditDate.send_keys(date.today().strftime('%d-%b-%Y'))

        auditTo = driver.find_element_by_css_selector('input[name=EMAIL_TO]')
        auditTo.send_keys(audit_to.strip())

        auditFrom = driver.find_element_by_css_selector('input[name=EMAIL_FROM]')
        auditFrom.send_keys(audit_from.strip())

        auditSubject = driver.find_element_by_css_selector('input[name=EMAIL_SUBJECT]')
        auditSubject.send_keys(audit_subject.strip())

        auditBody = driver.find_element_by_css_selector('textarea[name=EMAIL_BODY]')
        auditBody.send_keys(audit_body.strip())


        emailHourSelect = Select(driver.find_element_by_css_selector('select[name="EMAIL_HOUR_SENT"]'))
        emailHourSelect.select_by_visible_text(str(int(datetime.now().strftime('%I'))))

        emailMinuteSelect = Select(driver.find_element_by_css_selector('select[name="EMAIL_MINUTE_SENT"]'))
        emailMinuteSelect.select_by_visible_text(datetime.now().strftime('%M'))

        emailAMPMSelect = Select(driver.find_element_by_css_selector('select[name="EMAIL_AM_PM_SENT"]'))
        emailAMPMSelect.select_by_visible_text(datetime.now().strftime('%p'))


        driver.get_screenshot_as_file('audittrail_filled.png')
        addAuditTrailButton = driver.find_element_by_css_selector('td.dataentry > a[href*=\'MANUSCRIPT_DETAILS\']')
        addAuditTrailButton.click()

        return "Success"
        
    except:
        return "Error: " + str(sys.exc_info())


