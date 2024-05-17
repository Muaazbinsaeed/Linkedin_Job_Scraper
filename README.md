# Job Scraper

This project contains a web scraper for extracting job data from a given URL. The extracted data can be saved to a CSV file or displayed in a pandas DataFrame.

## Project Structure

    ```plaintext
    linedin_job_scraper/
    ├── job_scraper/
    │   ├── __init__.py
    │   ├── scraper.py
    │   ├── utils.py
    │   ├── config.py
    ├── tests/
    │   ├── __init__.py
    │   ├── test_scraper.py
    ├── main.py
    ├── requirements.txt
    ├── README.md
    ```


## Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/Muaazbinsaeed/Linkedin_Job_Scraper.git
    cd linkedin_job_scraper
    ```

2. **Create a virtual environment**:

    ```bash
    python3 -m venv temp_env
    source temp_env/bin/activate  # On Windows use: temp_env\Scripts\activate
    ```

3. **Upgrade pip**:

    ```bash
    pip install --upgrade pip
    ```

4. **Install dependencies using pip**:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Project

To run the project, execute the following command:
```bash
python main.py https://www.example.com
```

## Running the Unit Test
Run the unit tests:
```bash
python -m unittest discover -s tests
```

## Configuration

Modify the `job_scraper/config.py` file to change the URL and logging level.

## Output

The job data will be saved to `job_data.csv` and displayed in the console.

### .gitignore

A .gitignore file is included to exclude the virtual environment and other unnecessary files from being tracked by Git.
```plaintext
temp_env/
__pycache__/
*.pyc
*.pyo
*.pyd
*.csv
*.log
*.DS_Store
```

## Developed by

Muaaz Bin Saeed

This project is now an open-source repo.
