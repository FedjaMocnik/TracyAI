from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel, load_tool, tool
import datetime
import requests
import pytz
import yaml
from tools.final_answer import FinalAnswerTool
from Gradio_UI import GradioUI
from typing import List, Dict

COURTLISTENER_API_KEY = "insert_API_key"  
API_BASE = "https://www.courtlistener.com/api/rest/v4/"

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
    tools=[final_answer, search_court_cases, check_citation_status], #orodja
    max_steps=6,
    verbosity_level=1,
    grammar=None,
    planning_interval=None,
    name="Legal Research Assistant",
    description="Specializes in US federal and state court decisions analysis",
    prompt_templates=prompt_templates
)

GradioUI(agent).launch() #launch za UI

