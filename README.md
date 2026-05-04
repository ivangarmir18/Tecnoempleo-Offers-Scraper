# Tecnoempleo Offers Scraper

A lightweight Python scraper and data analyzer to extract real job market data from the Spanish IT job board, Tecnoempleo. 

## The Problem
Most job offers hide their salaries. I wanted to get a realistic, data-driven look at what companies are actually paying Python developers in Spain (specifically in Valencia and Remote roles), rather than relying on generic market estimations.

## How it works

The project is split into two straightforward scripts to separate extraction from analysis:

1. **`data_extraction.py`**: 
   - Uses `requests` and `BeautifulSoup` to navigate through Tecnoempleo's search pages.
   - Extracts job titles, companies, dates, and raw salary text.
   - Uses `pandas` to clean the data: drops duplicate jobs and parses messy string ranges (like "27.000€ - 33.000€ b/a") into clean numeric floats (`Min_Salary` and `Max_Salary`).
   - Saves the clean dataset into a local `SQLite` database.

2. **`data_analysis.py`**:
   - Connects to the SQLite database.
   - Filters out all job offers that don't disclose the salary.
   - Calculates real market averages and uses `matplotlib` to generate a bar chart comparing the top paying companies.

## Quick Finding
In a recent run focusing on Python roles (Valencia + Remote Spain), the script scraped ~200 raw offers. After cleaning duplicates and filtering out the ones with hidden salaries, the data showed an average minimum salary of **34,680€** for these roles.

## Extensibility
This script isn't hardcoded just for Python or Valencia. It uses a base configuration dictionary. You can easily swap the target URLs in `TARGET_SEARCHES` to scrape Data Analyst, Machine Learning, or any other roles in different cities to compare their market value.

## Tech Stack
* Python 3
* Pandas & NumPy
* Requests & BeautifulSoup4
* SQLite3
* Matplotlib