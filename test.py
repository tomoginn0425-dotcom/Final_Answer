from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.google.com")
time.sleep(3)
driver.quit()