from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

# 1) Set up Selenium with the ChromeDriver
driver = webdriver.Chrome(ChromeDriverManager().install())

# 2) Navigate to the dynamic GitLab page
driver.get("https://code.europa.eu/p2b/contrib-versions")

# 3) Wait for JavaScript to load the table items
time.sleep(5)  # or use WebDriverWait for more robust waiting

# 4) Locate the <tr> elements with class "tree-item"
tree_items = driver.find_elements(By.CSS_SELECTOR, "tr.tree-item")

# 5) Print the text from each row
for item in tree_items:
    print(item.text)

# 6) Quit the driver
driver.quit()
