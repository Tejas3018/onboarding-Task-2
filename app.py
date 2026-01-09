import requests
import csv
import logging

# LOGGING
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# FUNCTIONS 
def read_ips(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()]

def get_ip_details(ip):
    url = f"https://ipinfo.io/{ip}/geo"
    try:
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            logging.info(f"SUCCESS: Fetched data for {ip}")
            return response.json()
        else:
            logging.error(f"FAILED: {ip} returned {response.status_code}")
            return None

    except Exception as e:
        logging.error(f"ERROR: {ip} - {e}")
        return None

def extract_city(data):
    if data and "city" in data:
        return data["city"]
    return "Unknown"

def save_to_csv(results, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["IP Address", "City"])

        for ip, city in results:
            writer.writerow([ip, city])

# MAIN 
def main():
    ips = read_ips("ips.txt")
    results = []

    for ip in ips:
        data = get_ip_details(ip)
        city = extract_city(data)
        results.append((ip, city))

    save_to_csv(results, "ip_city.csv")
    print("✅ Data saved to ip_city.csv")

if __name__ == "__main__":
    main()
