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
    
    # 2) Open the target page for initial links
    driver.get("https://code.europa.eu/p2b/contrib-versions")

    # 3) Wait until the anchor elements with that class appear and store them in an array
    wait = WebDriverWait(driver, 10)
    anchor_selector = "a.tree-item-link.gl-inline-flex.gl-min-w-0.gl-max-w-full"
    anchors = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, anchor_selector)))
    
    # 4) Extract and store each href in an array
    initial_links = [link.get_attribute("href") for link in anchors]
    print("Initial Links:")
    for link in initial_links:
        print(link)
    
    # 5) For each initial link, visit the page and extract additional link(s)
    #    The additional link is assumed to be the anchor element immediately preceding the anchor
    #    with the class "tree-item-link gl-inline-flex gl-min-w-0 gl-max-w-full".
    #    We store the result in a dictionary with the initial link as key and the list of additional links as value.
    company_links = {}  # This dictionary will map each parent (company) link to its additional links
    
    for parent_link in initial_links:
        print(f"\nProcessing parent link: {parent_link}")
        driver.get(parent_link)
        try:
            # Using XPath to find the anchor element that immediately precedes the target element
            wait1 = WebDriverWait(driver, 10)
            additional_anchor_selector = "a.tree-item-link.gl-inline-flex.gl-min-w-0.gl-max-w-full"
            additional_anchors = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, additional_anchor_selector)))
            additional_links = [elem.get_attribute("href") for elem in additional_anchors if elem.get_attribute("href")]
            for i in additional_links:
                print("secondary link:" + i)

        except Exception as e:
            print(f"  No additional links found on: {parent_link}. Error: {e}")
            additional_links = []
        
        # Store the ordered additional links for the current parent link
        company_links[parent_link] = additional_links

    # 6) Display the organized data for easy retrieval
    print("\nOrganized Links:")
    for parent, add_links in company_links.items():
        print(f"Parent link: {parent}")
        for add_link in add_links:
            print(f"  Additional link: {add_link}")
    
    driver.quit()

if __name__ == "__main__":
    main()
