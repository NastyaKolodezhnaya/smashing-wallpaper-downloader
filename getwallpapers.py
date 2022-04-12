# import click
import requests
from calendar import month_name
from bs4 import BeautifulSoup
import re


def format_date_for_request(date):
    ''' format user input data to required url format '''
    pass


def getwallpapers(date, img_resolution='640x480'):
    month_posted = month_name[int(date[:2])].lower()
    year_posted = date[2:]
    if not month_posted == 'january':
        month_created = '0' + str(int(date[:2]) - 1)
        year_created = year_posted
    else:
        month_created = '12'
        year_created = str(int(year_posted) - 1)

    # request html-page from https://www.smashingmagazine.com/
    url = f'https://www.smashingmagazine.com/{year_created}/{month_created}/desktop-wallpaper-calendars-{month_posted}-{year_posted}/'

    # get <a> page elements (with image href) with requested resolution
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    img_list = soup.find_all('a', string=img_resolution)
    url_list = [item.attrs['href'] for item in img_list]

    # download wallpapers from each link
    for image_url in url_list:
        img_name = re.findall(r'[^/]*$', image_url)[0]
        request_image = requests.get(image_url)
        if request_image.status_code == 200:
            with open(img_name, 'wb') as file:
                file.write(request_image.content)
                print(f'{img_name} downloaded successfully.')
    print(f'Success for {len(url_list)} images!')


if __name__ == '__main__':
    getwallpapers('012018')
