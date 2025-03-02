from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, load_tool, tool
import datetime
import requests
import pytz
import yaml
from tools.final_answer import FinalAnswerTool
from Gradio_UI import GradioUI
from typing import List, Dict
from bs4 import BeautifulSoup

COURTLISTENER_API_KEY = "API_KEY"  
API_BASE = "https://www.courtlistener.com/api/rest/v4/"

#ISKANJE LINKA Z API
@tool
def search_terms_of_service(company_name: str) -> Dict:
    """Search for a company's Terms of Service link
    
    Args:
        company_name: Name of the organization/company to search for
    
    Returns:
        Dictionary containing company name and link to their Terms of Service
    """
    
    try:
        # API URL
        api_base = "https://05bf-176-76-227-247.ngrok-free.app"  # lokalno ga runnamo
        
        # API request naredimo
        url = f"{api_base}/company/{company_name}"
        
        print(f"Request URL: {url}")
        
        response = requests.get(url)
        
        print(f"Response status: {response.status_code}")
        print(f"Response body preview: {response.text[:200]}...")
        
        if response.status_code == 404: #HTTP error!  
            return {"error": f"Company '{company_name}' not found in the database"}
        
        response.raise_for_status()
        
        data = response.json()
        
        # ali obstaja več linkov?
        if not data.get('secondary_links') or len(data['secondary_links']) == 0:
            return {"error": f"No Terms of Service links found for {company_name}"}
        
       # returnamo ime in link, lahko jih več
        result = {
            "company_name": data["name"],
            "tos_link": data["secondary_links"][0],  # prvi link
            "all_links": data["secondary_links"]  # več linkov
        }
        
        return result
    
    except requests.exceptions.RequestException as e:
        error_msg = f"API Error: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            error_msg += f" (Status code: {e.response.status_code})"
            if hasattr(e.response, 'text'):
                error_msg += f" - {e.response.text[:200]}"
        print(error_msg)  # debug, da prizna, če se zmoti
        return {"error": error_msg}
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(error_msg)  # debug, da AI prizna, če se zmoti
        return {"error": error_msg}

#DOBIMO DEJANSKI TOS in link
@tool
def extract_tos_content(company_name: str) -> Dict:
    """
    Search for a company's Terms of Service, access the link, and extract raw content from GitLab repository.
    
    Args:
        company_name: Name of the organization/company to search for
    
    Returns:
        Dictionary containing company name, link, and extracted content
    """
    
    tos_info = search_terms_of_service(company_name)
    
    # error
    if "error" in tos_info:
        return tos_info
    
    try:
        # link od zgoraj
        tos_link = tos_info["tos_link"]
        
        print(f"Accessing TOS link: {tos_link}")
        
        # Gitlab repo
        if "code.europa.eu" in tos_link and "/-/blob/" in tos_link:
            # spremeni '/-/blob/' z '/-/raw/'
            raw_url = tos_link.replace("/-/blob/", "/-/raw/")
            
            
            if "?" in raw_url:
                raw_url = raw_url.split("?")[0]
                
            print(f"Accessing raw content URL: {raw_url}")
            
            # request za raw data iz GItlabaa
            response = requests.get(raw_url)
            response.raise_for_status()
            
            return {
                "company_name": tos_info["company_name"],
                "tos_link": tos_link,
                "raw_url": raw_url,
                "content": response.text,  # cel raw data fajl
                "content_type": "markdown" if raw_url.endswith(".md") else "text"
            }
        
        response = requests.get(tos_link)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        content = ""
        
        pre_element = soup.find('pre')
        if pre_element:
            content = pre_element.get_text()
        else:
            main_content = soup.find('main') or soup.find('article') or soup.find('body')
            if main_content:
                content = main_content.get_text(strip=True)
        
        return {
            "company_name": tos_info["company_name"],
            "tos_link": tos_link,
            "content": content,
            "note": "Content extracted from HTML page"
        }
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Error accessing TOS link: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            error_msg += f" (Status code: {e.response.status_code})"
            if hasattr(e.response, 'text'):
                error_msg += f" - {e.response.text[:200]}"
        print(error_msg)
        return {"error": error_msg}
        
    except Exception as e:
        error_msg = f"Unexpected error while processing content: {str(e)}"
        print(error_msg)
        return {"error": error_msg}

# POIŠČE USTREZNI CASE na podlagi: ključnih besed, datuma in pristojnost
@tool
def search_court_cases(keyword: str, jurisdiction: str = None, 
                      date_range: tuple = None) -> List[Dict]:
    
    """Search court cases by keyword and jurisdiction
    Args:
        keyword: Legal concepts or case terms to search
        jurisdiction: Court jurisdiction (e.g., 'scotus' for Supreme Court)
        date_range: Tuple of (start_date, end_date) in UTC
    """
    
    try:
        # API
        api_base = "https://www.courtlistener.com/api/rest/v4/"
        
        # zgradimo query
        params = {
            "q": keyword,
            "type": "o",  # 'o' opinion oz. mnenje
            "page_size": 5
        }
        
        
        if jurisdiction:
            if jurisdiction.lower() == "scotus":
                params["court"] = "scotus"
            else:
                params["court"] = jurisdiction
        
        # Datum in format
        if date_range:
            params["date_filed__gte"] = date_range[0].strftime("%Y-%m-%d")
            params["date_filed__lte"] = date_range[1].strftime("%Y-%m-%d")
        
        headers = {"Authorization": f"Token {COURTLISTENER_API_KEY}"}
        
        print(f"Request URL: {api_base}search/")
        print(f"Params: {params}")
        
        response = requests.get(f"{api_base}search/", params=params, headers=headers)
        
        print(f"Response status: {response.status_code}")
        print(f"Response body preview: {response.text[:200]}...")
        
        # Handle HTTP errors
        if response.status_code == 403:
            return "Authentication failed: Please check your API key"
        
        response.raise_for_status()
        
        data = response.json()
        
        if 'results' not in data or len(data['results']) == 0:
            return "No matching cases found in the database"
        
        cases = []
        for result in data['results']:
            case_info = {
                "case_name": result.get('caseName', result.get('case_name', 'Unknown')),
                "citation": result.get('citation', 'No citation available'),
                "court": result.get('court_full_name', result.get('court', 'Unknown')),
                "date_filed": result.get('date_filed', 'Unknown date'),
                "summary": result.get('text', result.get('snippet', ''))[:200] + '...' if result.get('text') or result.get('snippet') else "No summary available"
            }
            cases.append(case_info)
        
        return cases
    
    except requests.exceptions.RequestException as e:
        error_msg = f"API Error: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            error_msg += f" (Status code: {e.response.status_code})"
            if hasattr(e.response, 'text'):
                error_msg += f" - {e.response.text[:200]}"
        print(error_msg)  # debug
        return error_msg
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(error_msg)  # debug
        return error_msg


#POGLEDA NEK DAN CITAT!
@tool
def check_citation_status(citation_id: str) -> Dict:
    """Check the current status and treatment of a legal citation
    Args:
        citation_id: The citation ID (e.g., "403 U.S. 713")
    """
    try:
        # Use the correct API base URL with v4
        api_base = "https://www.courtlistener.com/api/rest/v4/"
        
        # API vrne z oklepaji mi rabimo brez!
        if "(" in citation_id:
            citation_id = citation_id.split("(")[0].strip()
        
        print(f"Looking up citation: {citation_id}")
        
        # API
        headers = {"Authorization": f"Token {COURTLISTENER_API_KEY}"}
        
        params = {
            "cite": citation_id,
            "court": "scotus"  
        }
        
        print(f"Request URL: {api_base}opinions/")
        print(f"Params: {params}")
        
        # API request, ki ga pošiljamo COurtListnereju
        response = requests.get(f"{api_base}opinions/", params=params, headers=headers)
        
        # debugiranje
        print(f"Response status: {response.status_code}")
        print(f"Response body preview: {response.text[:200]}...")
        
        response.raise_for_status()
        
        # JSON
        data = response.json()
        
        if 'results' in data and len(data['results']) > 0:
            result = data['results'][0]
            return {
                "status": result.get('status', 'Unknown'),
                "citation": result.get('citation', citation_id),
                "court": result.get('court_full_name', 'Unknown'),
                "precedential_status": result.get('precedential_status', 'Unknown'),
                "date_filed": result.get('date_filed', 'Unknown'),
                "case_name": result.get('case_name', 'Unknown')
            }
        else:
            return {"error": f"No citation found for {citation_id}"}
        
    except requests.exceptions.RequestException as e:
        error_msg = f"API Error: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            error_msg += f" (Status code: {e.response.status_code})"
            if hasattr(e.response, 'text'):
                error_msg += f" - {e.response.text[:200]}"
        print(error_msg)  # debugging
        return {"error": error_msg}
    
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        print(error_msg)  # debugging
        return {"error": error_msg} 
     

final_answer = FinalAnswerTool()

#kateri model in kje se povežemo!
model = HfApiModel(
    max_tokens=2096,
    temperature=0.3,  
    model_id='https://pflgm2locj2t89co.us-east-1.aws.endpoints.huggingface.cloud/',
    custom_role_conversions=None,
)

#prompti za agenta
with open("prompts.yaml", 'r') as stream:
    prompt_templates = yaml.safe_load(stream)

#param za agenta
agent = CodeAgent(
    model=model,
    tools=[final_answer,search_terms_of_service,extract_tos_content, search_court_cases, check_citation_status], #orodja
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name="Legal Research Assistant",
    description="Specializes in US federal and state court decisions analysis",
    prompt_templates=prompt_templates
)

GradioUI(agent).launch() #launch za UI

