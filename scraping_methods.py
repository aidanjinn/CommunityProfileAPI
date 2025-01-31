import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
api = os.getenv('API_KEY')

genai.configure(api_key=api)
model = genai.GenerativeModel("gemini-1.5-flash")

def gemini_prompt(area, text):
    prompt = f"""Using the following Wikipedia text about {area}, create a community profile:

{text}

Please create a professional community profile that includes:
1. A qualitative account of what the county/parish is known for
2. Racial demographics
3. Other relevant demographic and community data

Format this as a clean, professional summary without any preamble. 150 to 250 words for the introduction
and then th rest of the community profile requirments entitled above after the introduction"""

    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        return summary
    except Exception as e:
        return f"An error occurred while summarizing the article: {str(e)}"


def gemini_prompt2(text):
    prompt = f"""Using the following Wikipedia text, create a grid mix profile:

{text}

Please create a professional community profile that uses only the data provided:
1. Create a grix mix profile that details what percentage of from what fuel source/energy type
the grid is deriving its power from for this location.

Format this as a clean, professional summary without any preamble. """

    try:
        response = model.generate_content(prompt)
        summary = response.text.strip()
        return summary
    except Exception as e:
        return f"An error occurred while summarizing the article: {str(e)}"

def wiki_demo_scrape(area):
    url = "https://en.wikipedia.org/wiki/" + area

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Get main content div
        content = soup.find(id='mw-content-text')
        
        # Initialize text storage
        text = ''
        
        # Get all paragraphs, headings, and tables
        for element in content.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table']):

            if element.name.startswith('h'): 
                text += f"\n{element.get_text().strip()}\n"

            elif element.name == 'table':  
              
                for row in element.find_all('tr'):
                    row_text = ' | '.join([cell.get_text().strip() for cell in row.find_all(['th', 'td'])])
                    if row_text:
                        text += f"{row_text}\n"

            else:
                text += f"{element.get_text().strip()}\n"

        community_profile = gemini_prompt(area, text)

        return {
            "wiki_link": url,
            "area_name": area,
            "area_information": community_profile
        }
        
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}


def eia_profile_scrape(state_code):
    url = f"https://www.eia.gov/state/print.php?sid={state_code}#tabs-2"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Get main content div (more specific selector)
        content = soup.find('div', {'class': 'main_col'})
        if not content:
            return {"error": "Could not find main content"}

        # Initialize text storage
        text = ''
        
        # Get all text content
        for element in content.stripped_strings:
            text += element + '\n'

        grid_mix = gemini_prompt2(text)

        return {
            "eia_link": url,
            "state_name": state_code,
            "state_information": grid_mix
        }

    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred while fetching the data: {e}"}


