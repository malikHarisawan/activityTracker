from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Set up the WebDriver
driver = webdriver.Chrome()

# Open Google
driver.get("https://www.google.com")

# Find the search box and enter a query
search_box = driver.find_element("name", "q")
search_box.send_keys("Selenium automation")
search_box.send_keys(Keys.RETURN)

# Wait and close the browser
driver.quit()
