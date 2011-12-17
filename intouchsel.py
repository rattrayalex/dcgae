from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import logging
import smtplib
from getpass import getpass
import csv

import time, re, sys, datetime
import easygui as eg
import wx

class frameclass(wx.Frame):

    def __init__(self,parent,id):
        wx.Frame.__init__(self,parent,id,"Frame aka Window", size=(300,200))

def send_email(receiver, subject, body):
    s = smtplib.SMTP('smtp.gmail.com', )
    myGmail = 'intouch.registrator@gmail.com'
    myGMPasswd = 'iamarobot'
##    myGmail, myGMPasswd = eg.multenterbox(
##        msg='Enter your Gmail information',
##        title='Gmail send',
##        fields=['Username', 'Password']
##        )
    s.ehlo()
    s.starttls()
    s.login(myGmail, myGMPasswd)
    msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n%s" 
        %(myGmail, receiver, subject, body))
    s.sendmail(myGmail, [receiver], msg)
    s.quit()

def set_PennKey():
    headers = ('login', 'password', 'email')
    login = str(raw_input("PENNKEY: "))
    password = str(getpass("PASSWORD: "))
    your_email = str(raw_input("YOUR EMAIL (so you're notified):"))
    PennKey = {'login': login, 'password': password, 'email': your_email}
    with open('pkinfo.csv', 'w') as pkinfo:
        writer = csv.DictWriter(pkinfo, headers)
        writer.writerow(PennKey)
    return PennKey

def get_PennKey():
    headers = ('login', 'password', 'email')
    try:
        doc = open('pkinfo.csv')
        doc.close()
    except:
        return set_PennKey()
    with open('pkinfo.csv', 'r') as pkinfo:
        reader = csv.DictReader(pkinfo, headers)
        try:
            row1 = reader.next()
            if (headers[0] and headers[1]) in row1:
                print 'shits in here!'
                return row1
            else:
                print 'found nuthin'
                return set_PennKey()
        except: return set_PennKey()

def set_Courses():
    headers = ('Subject', 'Course', 'Section')
    
    more = True
    course_list = []
    while more == True:
        subject = str(raw_input("SUBJECT (ie; psyc):")).upper()
        course = str(raw_input("COURSE (ie; 001):"))
        section = str(raw_input("SECTION (ie; 403):"))
        full_course = {headers[0]: subject, headers[1]: course, headers[2]: section}
        course_list.append(full_course)
        continueq = str(raw_input("Add another course? [y/n]: ")).upper()[0]
        if continueq != 'Y': more = False

    with open('courses.csv', 'a') as f:
        writer = csv.DictWriter(f, headers)
        for full_course in course_list:
            writer.writerow(full_course)
    return course_list

def get_Courses():
    headers = ('Subject', 'Course', 'Section')
    courses = []
    try: open('courses.csv')
    except: set_Courses()
    with open('courses.csv', 'r') as f:
        reader = csv.DictReader(f, headers)
        try:
            for row in reader:
##                print 'trying to read row: %s' % row
                if (headers[0] and headers[1] and headers[2]) in row:
                    courses.append(row)
                else: print 'found row, didn\'t match'
            if len(courses) == 0:
                return set_Courses()
            else: return courses
        except:
            return set_Courses()

def delete_Course(course):
    print 'trying to delete course: ', course
    headers = ('Subject', 'Course', 'Section')
    courses = []
    with open('courses.csv', 'r') as f:
        reader = csv.DictReader(f, headers)
        for row in reader:
            if course != row:
                courses.append(row)
            else:
                print 'found the naughty one! %s' % row
    with open('courses.csv', 'w') as f:
        writer = csv.DictWriter(f, headers)
        for full_course in courses:
            writer.writerow(full_course)
    return course

def get_num_courses():
    print 'gettin number o courses'
    num = 0
    with open('courses.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 3:
                num +=1
                print num
    return num

def register_for_course(PennKey, Courses):
##    eg.msgbox("starting shit")
    logging.basicConfig(filename="InTouchAutomate.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info("starting a new attempt")

    username = PennKey['login']
    password = PennKey['password']
    your_email = PennKey['email']
    
    signinurl = 'https://weblogin.pennkey.upenn.edu/login?factors=UPENN.EDU,UPENN.EDU-PORTAL&cosign-isc-seo-portal_prod-0&https://medley11.isc-seo.upenn.edu/pennInTouch/jsp/fast2.do?bhcp=1'
    base_url = "https://medley11.isc-seo.upenn.edu/pennInTouch/jsp/fast2.do?fastButtonId="

    driver = webdriver.Firefox()

##    subject = str(raw_input("SUBJECT (ie; psyc):")).upper()
##    course = str(raw_input("COURSE (ie; 001):"))
##    section = str(raw_input("SECTION (ie; 403):"))
##    your_email = str(raw_input("YOUR EMAIL (so you're notified):"))

    driver.implicitly_wait(3)
    
    #The below while loop is for when the program tries to run
    #when the computer is not connected to the internet.
    #it may be worth considering implementing this in later portions as well.
    #it would also be worth making sure this is how this should be done.
    online = False
    while online == False:
        try:
            print 'tryin'
            driver.get(signinurl)
            login = driver.find_element_by_name("login")
            pw = driver.find_element_by_name("password")

            login.send_keys(username)
            pw.send_keys(password)

            driver.find_element_by_name("loginform").submit()
            online = True
        except:
            print 'failin, gonna try again'
            online = False
    # we have to wait for the page to refresh, the last thing that seems to be updated is the title
    # when there are data loads or the application is otherwise unavailable, we should test that here.
    try:
        WebDriverWait(driver, 10).until(lambda driver : driver.title.startswith("Penn InTouch"))
        link_to_register = driver.find_element_by_xpath('//table/tbody/tr/td/ul/li/ul/li[4]/a')
    except:
        print 'I think there are "loads from the warehouse" or some bull. Quitting, gonna try again in an hour'
        driver.quit()
        return

    
    link_js = link_to_register.get_attribute("onclick")
    logging.debug(link_js)
    link_code = re.search(r'fast2\.do\?fastButtonId=(\w{8})', str(link_js)).group(1)
    logging.debug(link_code)
    driver.get(base_url + link_code)
    logging.debug(driver.title)

##    subject_options = Select(driver.find_element_by_name("subjectPrimary"))
##    course_options = Select(driver.find_element_by_name("courseNumberPrimary"))
##    section_options = Select(driver.find_element_by_name("sectionNumberPrimary"))


    for c in Courses:
        print 'working on ', c
        course = c['Course']
        section = c['Section']
        subject = c['Subject']

        try:
            subject_options = Select(driver.find_element_by_name("subjectPrimary"))
            course_options = Select(driver.find_element_by_name("courseNumberPrimary"))
            section_options = Select(driver.find_element_by_name("sectionNumberPrimary"))
            subject_options.select_by_value(subject)
            course_options.select_by_value(course)
            section_options.select_by_value(section)
            submit_button = driver.find_element_by_xpath("//html/body/table/tbody/tr[2]/td/div[5]/table/tbody/tr/td/form/div/table[2]/tbody/tr[3]/td[2]/button[2]")
            submit_button.click()
##            submit_button.submit()
            time.sleep(3)
            check = driver.find_element_by_xpath("//span[contains(text(), '%s-%s-%s')]"% (subject, course, section))
            #re.search('<span class="fastButtonLinkText">%s-%s-%s</span>' % (subject, course, section), driver.read())
            if check:
                print check.text
                delete_Course(c)
            else:
                print 'shit was super close!! checking failed though'
                #need to send an email! 
            logging.info("I think it worked!! course registered. check to make sure! [%s %s %s]"% (subject, course, section)) 
            send_email(your_email, "You registered for %s-%s-%s!!"% (subject, course, section), "YAAAAY \n (double check to make sure) \n [%s-%s-%s]"% (subject, course, section)) 
        except:
            the_future = datetime.datetime.now() + datetime.timedelta(hours=1)
            next_try = 'Will try again at %s' % (the_future.strftime("%I:%M %p"))
            print next_try
            logging.info("%s-%s-%s not available! bummer"% (subject, course, section))
            send_email(your_email, "%s-%s-%s not available"% (subject, course, section), "bummer, %s-%s-%s isn't available \n %s"% (subject, course, section, next_try))

    driver.quit()

def main():
    PennKey = get_PennKey()
    Courses = get_Courses()
    num_courses = get_num_courses()
    while num_courses > 0:
        register_for_course(PennKey, Courses)
        num_courses = get_num_courses()
        if num_courses == 0:
            break
        else:
            
            time.sleep(3600)

if __name__ == "__main__":
    main()
