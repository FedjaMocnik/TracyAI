from bs4 import BeautifulSoup
import requests

listing_url = requests.get("https://code.europa.eu/p2b/contrib-versions")
soup = BeautifulSoup(listing_url.text, "lxml")

# Use the named argument for class
links = soup.find_all("div", class_="tree-item")
print(links)
