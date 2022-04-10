# import click
import requests
from calendar import month_name
from bs4 import BeautifulSoup


def getwallpapers(date, img_resolution='640x480'):
    # format user input data to url format
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
    request = requests.get(url)
    with open(f'smashing_{date}.html', 'w') as html_file:
        html_file.write(request.text)

    # get <a> page elements (with image href) with requested resolution
    soup = BeautifulSoup(request.text)
    img_list = soup.find_all('a', string=img_resolution)
    url_list = [item.attrs['href'] for item in img_list]

    # download wallpapers from each link
    # for image_url in url_list:
    #     img_page = requests.get(image_url)
    #     image = img_page.find('img')
    #     with open() as html_file:
    #


if __name__ == '__main__':
    getwallpapers('012018')
