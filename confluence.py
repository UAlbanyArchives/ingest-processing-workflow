import time
from getpass import getpass
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import chromedriver_binary

#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

#binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
#driver = webdriver.Firefox(firefox_binary=binary)

user = input("Username: ")
pw = getpass()
pageID = input("pageID: ")

page1 = "https://wiki.albany.edu/login.action"
driver = webdriver.Chrome()

driver.get(page1)
print ("waiting")

time.sleep(2)
print ("looking for element")

driver.find_element_by_id("os_username").send_keys(user)
driver.find_element_by_id("os_password").send_keys(pw)

driver.find_element_by_id("loginButton").click()


def download(driver, pageCount):
    #time.sleep(2)
    pageCount += 1
    print ("Page " + str(pageCount))
    for link in driver.find_elements_by_css_selector("a.filename"):
        title = link.get_attribute("title")
        if len(title) > 0 and not title.lower().endswith(".jpg") and not title.lower().endswith(".png"):
            href = link.get_attribute("href")
            print (href)
            link.click()
        
    next = driver.find_elements_by_xpath("//*[contains(text(), 'Next')]")[0]
    if not next.get_attribute("href") is None:
        next.click()
        #print ("next page")
        download(driver, pageCount)
    else:
        print ("Done!")


time.sleep(2)
page2 = "https://wiki.albany.edu/pages/viewpageattachments.action?pageId=" + pageID
driver.get(page2)

pageCount = 0
download(driver, pageCount)