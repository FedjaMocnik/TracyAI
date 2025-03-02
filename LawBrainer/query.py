import sqlite3

def query_company(company_name, db_name="companies.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Retrieve company data based on the name
    cursor.execute("SELECT id, primary_link FROM companies WHERE name=?", (company_name,))
    result = cursor.fetchone()
    if result:
        company_id, primary_link = result
        #print(f"Company: {company_name}\nPrimary URL: {primary_link}")
        print("Company: " + company_name)
        # Retrieve associated secondary links
        cursor.execute("SELECT secondary_link FROM secondary_links WHERE company_id=?", (company_id,))
        secondary_links = cursor.fetchall()
        print("Links to files:")
        for link in secondary_links:
            print("  " + link[0])
    else:
        print("Company not found.")
    
    conn.close()

if __name__ == "__main__":
    # Replace 'Your Company Name' with an actual company name from your database.
    company_to_query = input("Enter the company name to query: ")
    query_company(company_to_query)
