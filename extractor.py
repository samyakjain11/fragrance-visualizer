# purpose: scraping fragrantica, and creating Fragrance objects?
# need to start using parfumo, easier to scrape!
import requests
from bs4 import BeautifulSoup as bs
from fragrance import Fragrance
from typing import Dict
import os
from dotenv import load_dotenv, dotenv_values 
from googleapiclient.discovery import build
import json


load_dotenv()
GSEARCH_API_KEY = os.getenv('GSEARCH_API')
GSEARCH_CUSTOM_ENGINE = os.getenv("GSEARCH_CUSTOM_ENGINE")

def parseInformationFromFragrance(fragrance_input: str) -> Fragrance:
    name, brand, website_link = searchNameBrandLink(fragrance_input)
    print(name, brand, website_link)
    saved_html_file = saveHTMLfile(website_link)
    all_notes = extractAllNotes(saved_html_file)

    parsedFrag = Fragrance(brand=brand, name=name, unparsed_name=fragrance_input, website_link=website_link, notes=all_notes)
    return parsedFrag

def searchNameBrandLink(fragrance_input: str) -> list[str]:
    service = build("customsearch", "v1", developerKey=GSEARCH_API_KEY)
    [item] = service.cse().list(q=fragrance_input, cx=GSEARCH_CUSTOM_ENGINE,num=1).execute()['items']
    link, title = (item['link'], item['title'])
    actualTitle = title.split("»")[0]
    [name, brand] = actualTitle.split(' by ')
    brand = brand.split('(')[0]
    return [name, brand, link]

def extractAllNotes(saved_html_file) -> Dict[Fragrance.NoteTypes, list[str]]:
    html_content = None
    with open(saved_html_file, 'r') as html_file:
        html_content = html_file.read()
    soup = bs(html_content, 'html.parser')
    notes_super_div = soup.find_all("div", {'class': "notes_list mb-2"})
    assert(len(notes_super_div) == 1)
    notes_super_div = notes_super_div[0]

    top_notes = extractNotesGivenDiv(notes_super_div.find_all("div", {'class' : "pyramid_block nb_t w-100 mt-2"}) )
    heart_notes = extractNotesGivenDiv(notes_super_div.find_all("div", {'class' : "pyramid_block nb_m w-100 mt-2"}) )
    base_notes = extractNotesGivenDiv(notes_super_div.find_all("div", {'class' : "pyramid_block nb_b w-100 mt-2"}) )

    notes : dict = {    Fragrance.NoteTypes.TOP : top_notes,
                        Fragrance.NoteTypes.MIDDLE : heart_notes, 
                        Fragrance.NoteTypes.BASE : base_notes
                    }
    
    return notes



def extractNotesGivenDiv(notesDiv):
    assert(len(notesDiv) == 1)
    notesDiv = notesDiv[0]
    images = notesDiv.find_all('img')
    return [img.get('alt', '') for img in images][1:] # first alt tag is just "top notes"

def saveHTMLfile(website_link: str):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(website_link, headers=headers)
    if response.status_code == 200:
        with open("output.html", "w") as file:
            file.write(response.text)
    
    return "output.html"

fragrance : Fragrance = parseInformationFromFragrance("ojar wood whisper")
print(fragrance.fetchNotes(Fragrance.NoteTypes.BASE))