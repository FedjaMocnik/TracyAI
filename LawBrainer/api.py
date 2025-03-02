from flask import Flask, jsonify, request
import sqlite3
import requests

app = Flask(__name__)
DATABASE = "companies.db"  # Ensure this points to your existing database

def get_company_by_name(company_name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # Retrieve company information by name (ignoring primary_link)
    cursor.execute("SELECT id, name FROM companies WHERE name = ?", (company_name,))
    row = cursor.fetchone()
    if row:
        company_id, name = row
        # Retrieve all secondary links for this company
        cursor.execute("SELECT secondary_link FROM secondary_links WHERE company_id = ?", (company_id,))
        secondary_links = [r[0] for r in cursor.fetchall()]
        conn.close()
        return {
            "name": name,
            "secondary_links": secondary_links
        }
    else:
        conn.close()
        return None

@app.route("/company/<company_name>", methods=["GET"])
def get_company(company_name):
    """
    Return company details along with its secondary links (links to markdown files).
    """
    company = get_company_by_name(company_name)
    if company:
        return jsonify(company)
    else:
        return jsonify({"error": "Company not found"}), 404

@app.route("/company/<company_name>/content", methods=["GET"])
def get_company_content(company_name):
    """
    Fetch content from the first secondary link for the given company.
    This endpoint assumes that the secondary link points to a markdown file.
    """
    company = get_company_by_name(company_name)
    if not company:
        return jsonify({"error": "Company not found"}), 404

    secondary_links = company.get("secondary_links", [])
    if not secondary_links:
        return jsonify({"error": "No secondary links found for this company"}), 404

    # For simplicity, use the first secondary link
    url = secondary_links[0]
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return jsonify({"url": url, "content": response.text})
        else:
            return jsonify({"error": f"Failed to fetch content, status code {response.status_code}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Run the API on localhost:5000 in debug mode.
    app.run(debug=True)
