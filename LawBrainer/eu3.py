from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Set up the ChromeDriver with webdriver_manager
driver = webdriver.Chrome(ChromeDriverManager().install())

# Open the listing page
driver.get("https://code.europa.eu/p2b/contrib-versions")

# Wait for the dynamic content to load
wait = WebDriverWait(driver, 10)
rows = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr.tree-item")))

if rows:
    # Select the first row as an example
    first_row = rows[0]
    try:
        # Within the row, locate the <td> with the file name
        td = first_row.find_element(By.CSS_SELECTOR, "td.tree-item-file-name.gl-relative.gl-cursor-default")
        # Find the <a> inside this <td>
        link = td.find_element(By.TAG_NAME, "a")
        detail_url = link.get_attribute("href")
        print("Detail URL:", detail_url)
        # Click the link to navigate to the detail page
        link.click()
    except Exception as e:
        print("Error accessing the detail link:", e)
        driver.quit()
        exit()
else:
    print("No tree-item rows found.")
    driver.quit()
    exit()

# Now on the detail page, wait for the PDF link to appear.
# This assumes that the PDF link is an <a> with an href that ends with ".pdf"
pdf_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href$='.pdf']")))
pdf_url = pdf_link.get_attribute("href")
print("Found PDF URL:", pdf_url)

# Optional: You could also click the PDF link if needed.
# pdf_link.click()

driver.quit()
