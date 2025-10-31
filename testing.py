import pandas as pd
from bs4 import BeautifulSoup
import requests
import csv



gtfs_routes = pd.read_csv("resource/latest/routes.txt")
train_list = gtfs_routes[["route_short_name"]].drop_duplicates().reset_index(drop=True)


def scrape_zug(train_number):
    url = f"https://www.zugfinder.net/en/train?train={train_number}"
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        return False
    soup = BeautifulSoup(r.text, "html.parser")
    if "No train found" in r.text or "not available" in r.text:
        return False
    return True

def main():
    for(index, row) in train_list.iterrows():
        train_number = row["route_short_name"]  
        available = scrape_zug(train_number)
        print(f"Train {train_number}, available: {available}")
    train_list["available_on_zugfinder"] = train_list["route_short_name"].apply(scrape_zug)
    coverage = train_list["available_on_zugfinder"].mean()
    print(f"Coverage rate: {coverage*100:.1f}% of trains found on ZugFinder")

    
    



if __name__ == "__main__":
    main()
