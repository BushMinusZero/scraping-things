import itertools
import os
from typing import Dict, List

from bs4 import BeautifulSoup
import requests
import pandas as pd


# Resident Adviser scraper
# https://www.residentadvisor.net/dj.aspx?area=218&country=1


class ResidentAdvisorParams:
    amsterdam = 'https://www.residentadvisor.net/dj.aspx?area=29&country=6'
    barcelona = 'https://www.residentadvisor.net/dj.aspx?area=20&country=5'
    berlin = 'https://www.residentadvisor.net/dj.aspx?area=34&country=12'
    chicago = 'https://www.residentadvisor.net/dj.aspx?area=17&country=2'
    cologne = 'https://www.residentadvisor.net/dj.aspx?area=143&country=12'
    detroit = 'https://www.residentadvisor.net/dj.aspx?area=19&country=2'
    hamburg = 'https://www.residentadvisor.net/dj.aspx?area=148&country=12'
    ibiza = 'https://www.residentadvisor.net/dj.aspx?area=25&country=5'
    italy = 'https://www.residentadvisor.net/dj.aspx?area=172&country=20'
    madrid = 'https://www.residentadvisor.net/dj.aspx?area=41&country=5'
    new_york = 'https://www.residentadvisor.net/dj.aspx?area=8&country=2'
    paris = 'https://www.residentadvisor.net/dj.aspx?area=44&country=15'
    london = 'https://www.residentadvisor.net/dj.aspx?area=13&country=3'
    los_angeles = 'https://www.residentadvisor.net/dj.aspx?area=23&country=2'
    san_francisco = 'https://www.residentadvisor.net/dj.aspx?area=218&country=1'
    top_1000 = 'https://www.residentadvisor.net/dj.aspx'
    pages_to_scrape = {'amsterdam': amsterdam, 'barcelona': barcelona, 'berlin': berlin, 'chicago': chicago,
                       'cologne': cologne, 'detroit': detroit, 'hamburg': hamburg, 'ibiza': ibiza, 'italy': italy,
                       'madrid': madrid, 'new_york': new_york, 'paris': paris, 'london': london,
                       'los_angeles': los_angeles, 'san_francisco': san_francisco, 'top_1000': top_1000}

    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'artists.csv')


def scrape_artists_on_page(name: str, url: str) -> List[Dict[str, str]]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features='html.parser')

    artists = []
    for a_tag in soup.find_all('a', href=True):
        if a_tag['href'].startswith("/dj/"):
            if a_tag.text.strip() and 'Following' not in a_tag.text:
                href = a_tag['href']
                artist = a_tag.text.strip()
                artist_info = {'page_name': name, 'artist': artist, 'href': href, 'url': url}
                artists.append(artist_info)
    return artists


def scrape_artists_on_pages(urls: Dict[str, str]) -> List[Dict[str, str]]:
    all_artists = []
    for name, url in urls.items():
        artists = scrape_artists_on_page(name, url)
        all_artists.append(artists)
    return list(itertools.chain.from_iterable(all_artists))


def main():
    artists = scrape_artists_on_pages(ResidentAdvisorParams.pages_to_scrape)
    artists_df = pd.DataFrame(artists)
    artists_df.dropna(inplace=True)
    artists_df.drop_duplicates(subset='artist', inplace=True)
    artists_df.to_csv(ResidentAdvisorParams.output_path, index=False)
    print(f"Saved {len(artists_df.index)} artists to {ResidentAdvisorParams.output_path}")


if __name__ == '__main__':
    main()
