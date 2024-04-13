# simple example on how to use selenium. Does not use scrapy

from selenium import webdriver
import time

# replace 'chromedriver_path' with the path of your actual chromedriver.exe file
driver = webdriver.Chrome()

# open the web page in the browser:
driver.get("https://www.linkedin.com/login")

# find the elements on the login page:
username = driver.find_element('name', 'session_key')
password = driver.find_element('name', 'session_password')

# enter username and password:
username.send_keys('my_email')
password.send_keys('my_passowrd')

# for security reason, it's better not to hard-code your credentials in the script,
# consider using getpass or environment variables

# submit the form:
login_button = driver.find_element('class name', 'btn__primary--large')
login_button.click()

driver.get('https://www.linkedin.com/company/iqvia?trk=public_jobs_jserp-result_job-search-card-subtitle')
html = driver.page_source
time.sleep(120)  # pause to allow you to inspect the browser

driver.quit()  # close the browser window
