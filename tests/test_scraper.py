import unittest
import os
from job_scraper.scraper import JobScraper
from job_scraper.config import URL

class TestJobScraper(unittest.TestCase):
    def setUp(self):
        self.url = URL
        self.scraper = JobScraper(self.url)

    def test_fetch_page(self):
        self.scraper._fetch_page()
        self.assertIsNotNone(self.scraper.soup)

    def test_extract_job_data(self):
        self.scraper._fetch_page()
        self.scraper.scrape()
        self.assertTrue(all(key in self.scraper.job_data for key in [
            'Date', 'Job_Description', 'Job_Link', 'Job_Title', 'Location', 'Company_Name', 'Company_Link', 'Job_Posted',
            'Job_Type', 'Job_Mode', 'Recruiter_Name', 'Recruiter_Title', 'Recruiter_Link'
        ]))

    def test_to_csv(self):
        self.scraper._fetch_page()
        self.scraper.scrape()
        self.scraper.to_csv("job_data.csv")
        self.assertTrue(os.path.exists("job_data.csv"))

    def test_scrape(self):
        job_data = self.scraper.scrape()
        self.assertIsInstance(job_data, dict)
        self.assertTrue(all(key in job_data for key in [
            'Date', 'Job_Description', 'Job_Link', 'Job_Title', 'Location', 'Company_Name', 'Company_Link', 'Job_Posted',
            'Job_Type', 'Job_Mode', 'Recruiter_Name', 'Recruiter_Title', 'Recruiter_Link'
        ]))

if __name__ == "__main__":
    unittest.main()
