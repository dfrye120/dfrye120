import requests
import logging
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    filename='url_categorization.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
    
)

def categorize_urls(input_file, output_202_404, output_other_errors, timeout=10):
    try:
        with open(input_file, 'r') as file:
            urls = file.readlines()
    
    except FileNotFoundError:
        logging.error(f"Input file {input_file} not found.")
        print(f"Input file {input_file} not found.")
       
        return

    urls = [url.strip() for url in urls]

    with open(output_202_404, 'w') as file_202_404, open(output_other_errors, 'w') as file_other_errors:
      
        for url in tqdm(urls, desc="Processing URLs"):
            
            try:
                response = requests.get(url, timeout=timeout)
                status_code = response.status_code
               
                if status_code in [202, 401, 404]:
                    file_202_404.write(f"{url} - Status Code: {status_code}\n")
                    logging.info(f"{url} - Status Code: {status_code}")
               
                else:
                    file_other_errors.write(f"{url} - Status Code: {status_code}\n")
                    logging.info(f"{url} - Status Code: {status_code}")
            
            except requests.exceptions.SSLError as ssl_error:
                logging.error(f"{url} - SSL Error: {ssl_error}")       
            
            except requests.RequestException as e:
                file_other_errors.write(f"{url} - Error: {e}\n")
                logging.error(f"{url} - Error: {e}")

if __name__ == "__main__":
    input_file = 'livedomains.txt'
    output_202_404 = '202_or_404.txt'
    output_other_errors = 'other_errors.txt'
    timeout = 10  # Timeout in seconds

    categorize_urls(input_file, output_202_404, output_other_errors, timeout)
    print("URL categorization complete.")
