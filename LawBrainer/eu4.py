from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def main():
    # 1) Setup ChromeDriver with webdriver_manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    # 2) Open the target page
    driver.get("https://code.europa.eu/p2b/contrib-versions")

    # 3) Wait until the anchor elements with that class appear
    wait = WebDriverWait(driver, 10)
    anchor_selector = "a.tree-item-link.gl-inline-flex.gl-min-w-0.gl-max-w-full"
    anchors = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, anchor_selector)))

    # 4) Extract and print each href
    #for link in anchors:
        #href = link.get_attribute("href")
        #print("Link found:", href)

    
    # 4) Extract and store each href in an array
    links = [link.get_attribute("href") for link in anchors]
    for i in links:
        print(i)
    driver.quit()

if __name__ == "__main__":
    main()
