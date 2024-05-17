# job_scraper/scraper.py
import requests
from bs4 import BeautifulSoup
import html2text
import re
import os
import logging
import pandas as pd
import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Dict
from .utils import extract_element_text, extract_element_href, is_ipython

if is_ipython():
    from IPython.display import display

class JobScraper:
    def __init__(self, url: str, verbose: bool = False):
        self.url = url
        self.verbose = verbose
        self.job_data: Dict[str, str] = self._initialize_job_data()

    def _initialize_job_data(self) -> Dict[str, str]:
        return {
            'Date': datetime.datetime.today().strftime('%Y-%m-%d'),
            'Job_Description': '',
            'Job_Link': '',
            'Job_Title': '',
            'Location': '',
            'Company_Name': '',
            'Company_Link': '',
            'Job_Posted': '',
            'Job_Type': '',
            'Job_Mode': '',
            'Recruiter_Name': '',
            'Recruiter_Title': '',
            'Recruiter_Link': ''
        }

    def scrape(self) -> Dict[str, str]:
        try:
            self._fetch_page()
            with ThreadPoolExecutor() as executor:
                futures = [
                    executor.submit(self._extract_description),
                    executor.submit(self._extract_job_link),
                    executor.submit(self._extract_job_title),
                    executor.submit(self._extract_location),
                    executor.submit(self._extract_company_name),
                    executor.submit(self._extract_company_link),
                    executor.submit(self._extract_job_posted),
                    executor.submit(self._extract_job_type),
                    executor.submit(self._extract_job_mode),
                    executor.submit(self._extract_recruiter_info),
                ]
                for future in futures:
                    future.result()
            return self.job_data
        except Exception as e:
            logging.error(f"Error scraping {self.url}: {e}")
            return {}

    def _fetch_page(self) -> None:
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.soup = BeautifulSoup(response.content, 'html.parser')
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching page: {e}")
            raise

    def _extract_description(self) -> None:
        try:
            body_html = self.soup.find('body')
            main_body_html = body_html.find('main', id="main-content")
            description_html = main_body_html.find('div', class_='description__text--rich')
            if description_html:
                for tag in description_html.find_all(['button', 'icon']):
                    tag.extract()
                converter = html2text.HTML2Text()
                converter.body_width = 0
                job_description_formatted_text = converter.handle(str(description_html))
                job_description = re.sub(r'\n{2,}', '\n', job_description_formatted_text)
            else:
                job_description = ""
        except Exception as e:
            logging.error(f"Error extracting job description: {e}")
            job_description = ""
        self.job_data['Job_Description'] = job_description

    def _extract_job_link(self) -> None:
        self.job_data['Job_Link'] = self.url

    def _extract_job_title(self) -> None:
        job_title_element = self.soup.find("h3", class_="sub-nav-cta__header")
        self.job_data['Job_Title'] = extract_element_text(job_title_element)

    def _extract_location(self) -> None:
        location_element = self.soup.find("span", class_="sub-nav-cta__meta-text")
        self.job_data['Location'] = extract_element_text(location_element)

    def _extract_company_name(self) -> None:
        company_name_element = self.soup.find("a", class_="sub-nav-cta__optional-url")
        self.job_data['Company_Name'] = extract_element_text(company_name_element)

    def _extract_company_link(self) -> None:
        company_link_element = self.soup.find("a", class_="sub-nav-cta__optional-url")
        self.job_data['Company_Link'] = extract_element_href(company_link_element)

    def _extract_job_posted(self) -> None:
        job_posted_element = self.soup.find('span', {'class': 'posted-time-ago__text topcard__flavor--metadata'})
        self.job_data['Job_Posted'] = extract_element_text(job_posted_element)

    def _extract_job_type(self) -> None:
        try:
            job_type_element_ul = self.soup.find_all('ul', class_='description__job-criteria-list')
            job_type_element = job_type_element_ul[0].find('h3', text=re.compile('Employment type')) if job_type_element_ul else None
            job_type = extract_element_text(job_type_element.find_next_sibling('span')) if job_type_element else None
        except Exception as e:
            logging.error(f"Error extracting job type: {e}")
            job_type = None
        self.job_data['Job_Type'] = job_type

    def _extract_job_mode(self) -> None:
        job_mode = "Remote"
        apply_button = self.soup.find('button', class_='apply-button apply-button--default btn-md btn-primary')
        if apply_button and 'data-tracking-control-name="public_jobs_apply-link-onsite"' in str(apply_button):
            job_mode = 'Onsite'
        self.job_data['Job_Mode'] = job_mode

    def _extract_recruiter_info(self) -> None:
        recruiter_div = self.soup.find("div", class_="message-the-recruiter")
        if recruiter_div:
            recruiter_name_element = recruiter_div.find("h3", class_="base-main-card__title")
            recruiter_title_element = recruiter_div.find("h4", class_="base-main-card__subtitle")
            recruiter_link_element = recruiter_div.find("a", class_="base-card__full-link")
            self.job_data['Recruiter_Name'] = extract_element_text(recruiter_name_element)
            self.job_data['Recruiter_Title'] = extract_element_text(recruiter_title_element)
            self.job_data['Recruiter_Link'] = extract_element_href(recruiter_link_element)
        else:
            self.job_data['Recruiter_Name'] = ""
            self.job_data['Recruiter_Title'] = ""
            self.job_data['Recruiter_Link'] = ""

    def to_csv(self, filename: str, mode: str = 'w') -> None:
        try:
            df = pd.DataFrame([self.job_data])
            if mode == 'w':
                df.to_csv(filename, index=False)
            else:
                if not os.path.isfile(filename):
                    df.to_csv(filename, index=False)
                else:
                    df.to_csv(filename, mode='a', header=False, index=False)
        except Exception as e:
            logging.error(f"Error saving to CSV: {e}")
            raise

    def _print_job_data(self, output_format='print') -> None:
        if output_format == 'print':
            for key, value in self.job_data.items():
                print(f"{key}: {value}")
        elif output_format == 'pandas':
            df = pd.DataFrame([self.job_data])
            if is_ipython():
                display(df)
            else:
                print(df)
        else:
            raise ValueError("Invalid output format. Use 'print' or 'pandas'.")
