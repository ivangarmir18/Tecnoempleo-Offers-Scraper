import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import sqlite3
import time

# CONFIGURATION DICTIONARY
# Base URLs without the page number so we can dynamically append it
TARGET_SEARCHES = {
    "Valencia": "https://www.tecnoempleo.com/ofertas-trabajo/?te=python&pr=,279,&pagina=",
    "España Remoto": "https://www.tecnoempleo.com/ofertas-trabajo/?te=python&en_remoto=,1,&pagina="
}

MAX_PAGES = 5
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36 OPR/130.0.0.0"
}

job_offers = []

# STEP 1: SCALABLE EXTRACTION
print("--- Starting Web Scraping ---")

for search_name, base_url in TARGET_SEARCHES.items():
    print(f"\nTarget: {search_name}")
    
    for page in range(1, MAX_PAGES + 1):
        url = f"{base_url}{page}"
        print(f" Scraping page {page}...")
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            job_cards = soup.find_all('div', class_="p-3 border rounded mb-3 bg-white")
            
            if not job_cards:
                print("    No more jobs found on this page. Moving to next target.")
                break # Stops searching pages if we hit an empty page
                
            for card in job_cards:
                title_tag = card.find('h3', class_="fs-5 mb-2")
                company_tag = card.find('a', class_="text-primary link-muted")
                right_box = card.find('div', class_="col-12 col-lg-3 text-gray-700 pt-2 text-right hidden-md-down")
                
                date = "No Date"
                salary = "No Salary"
                
                if right_box:
                    raw_texts = list(right_box.stripped_strings)
                    if len(raw_texts) > 0:
                        date = raw_texts[0]
                        
                    for text in raw_texts:
                        if "€" in text:
                            salary = text
                            break
                
                offer = {
                    "Search_Category": search_name, # Keeps track of where we found it
                    "Title": title_tag.text.strip() if title_tag else "No Title",
                    "Company": company_tag.text.strip() if company_tag else "Hidden Company",
                    "Date": date,
                    "Salary": salary
                }
                job_offers.append(offer)
                
            # Wait 1 seconds before asking for the next page
            time.sleep(1)
            
        else:
            print(f"Access denied. Status code: {response.status_code}")
            break

print(f"\nFinished scraping! Total raw jobs collected: {len(job_offers)}")


# STEP 2: DATAFRAME & DUPLICATE REMOVAL
print("\n--- Cleaning Data ---")
df = pd.DataFrame(job_offers)

# Remove duplicate jobs
df.drop_duplicates(subset=['Title', 'Company'], keep='first', inplace=True)
print(f"Total jobs after removing duplicates: {len(df)}")


# STEP 3: DATA NORMALIZATION
placeholders = ["No Salary", "No Date", "Hidden Company", "No Title"]
df.replace(placeholders, np.nan, inplace=True)

def clean_salary_text(salary_string):
    if pd.isna(salary_string):
        return pd.Series([np.nan, np.nan])
    try:
        cleaned_list = salary_string.replace("€", "").replace("b/a", "").replace(" ", "").replace(".", "").strip().split("-")
        if len(cleaned_list) == 2:
            return pd.Series([float(cleaned_list[0]), float(cleaned_list[1])])
        else:
            return pd.Series([float(cleaned_list[0]), float(cleaned_list[0])])
    except Exception:
        return pd.Series([np.nan, np.nan])

df[['Min_Salary', 'Max_Salary']] = df['Salary'].apply(clean_salary_text)
df.drop(columns=['Salary'], inplace=True)


# STEP 4: SQL STORAGE
print("\n--- Saving to Database ---")
connection = sqlite3.connect("job_market.db")

df.to_sql(
    name="python_jobs",       
    con=connection,           
    if_exists="replace",      
    index=False               
)

connection.close()
print("Success! Data perfectly saved in job_market.db")