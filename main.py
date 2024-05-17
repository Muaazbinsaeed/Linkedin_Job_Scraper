import logging
import sys
from job_scraper.scraper import JobScraper
from job_scraper.config import URL, LOG_LEVEL
from job_scraper.utils import is_ipython

def main():
    logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

    url = URL
    if not is_ipython():  # Running not in IPython Notebook
        if len(sys.argv) > 1:
            url = sys.argv[1]

    try:
        scraper = JobScraper(url, verbose=True)
        job_data = scraper.scrape()
        scraper.to_csv("job_data.csv", mode='a')
        # scraper._print_job_data(output_format='pandas')
        scraper._print_job_data(output_format='print')
    except Exception as e:
        logging.error(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
