from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()  # or Firefox, Edge, etc.
driver.get("https://code.europa.eu/p2b/contrib-versions")

time.sleep(5)  # wait for dynamic content to load, or use WebDriverWait

# Escape the colon in "sm:gl-table-cell" if needed in your CSS selector
tree_items = driver.find_elements(By.CSS_SELECTOR, "tr.tree-item")
for item in tree_items:
    print(item.text)

driver.quit()
