from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import sqlite3

# --- Database Insertion Functions ---
def insert_company(name, primary_link, db_name="companies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO companies (name, primary_link) VALUES (?, ?)", (name, primary_link))
    company_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return company_id

def insert_secondary_link(company_id, secondary_link, db_name="companies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO secondary_links (company_id, secondary_link) VALUES (?, ?)", (company_id, secondary_link))
    conn.commit()
    conn.close()

def main():
    # 1) Setup ChromeDriver with webdriver_manager
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    # 2) Open the target page for initial (primary) links
    driver.get("https://code.europa.eu/p2b/contrib-versions")

    # 3) Wait until the anchor elements with the given class appear and store them in an array
    wait = WebDriverWait(driver, 10)
    anchor_selector = "a.tree-item-link.gl-inline-flex.gl-min-w-0.gl-max-w-full"
    anchors = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, anchor_selector)))
    
    # 4) Extract and store each primary link's href and title in a list of dictionaries
    primary_links = []
    print("Primary Links:")
    for link in anchors:
        href = link.get_attribute("href")
        name = link.get_attribute("title")
        primary_links.append({"name": name, "href": href})
        print(f"Name: {name}, URL: {href}")
    
    # 5) For each primary link, visit the page and extract additional (secondary) link(s)
    #    The company_links dictionary below is now used for printing purposes only.
    #    All scraped data is inserted into the SQLite database.
    company_links = {}
    
    for primary in primary_links:
        name = primary["name"]
        parent_link = primary["href"]
        print(f"\nProcessing primary link for company: {name}\nURL: {parent_link}")
        
        # Insert the primary company data into the database
        company_id = insert_company(name, parent_link)
        
        driver.get(parent_link)
        try:
            # Using the same CSS selector to find the secondary links on the child page
            additional_anchor_selector = "a.tree-item-link.gl-inline-flex.gl-min-w-0.gl-max-w-full"
            additional_anchors = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, additional_anchor_selector)))
            additional_links = [elem.get_attribute("href") for elem in additional_anchors if elem.get_attribute("href")]
            for link in additional_links:
                print("  Secondary link: " + link)
                insert_secondary_link(company_id, link)
        except Exception as e:
            print(f"  No secondary links found on: {parent_link}. Error: {e}")
            additional_links = []
        
        # Map company name to its list of secondary links (for display only)
        company_links[name] = additional_links

    # 6) Display the organized data for easy retrieval
    print("\nOrganized Company Links:")
    for company, links in company_links.items():
        print(f"Company: {company}")
        for link in links:
            print(f"  Secondary link: {link}")
    
    driver.quit()

if __name__ == "__main__":
    main()
