import logging
import sys

def extract_element_text(element, default="") -> str:
    try:
        return element.text.strip() if element else default
    except Exception as e:
        logging.error(f"Error extracting element text: {e}")
        return default

def extract_element_href(element, default="") -> str:
    try:
        return element["href"] if element else default
    except Exception as e:
        logging.error(f"Error extracting element href: {e}")
        return default

def is_ipython():
    return 'ipykernel' in sys.modules
