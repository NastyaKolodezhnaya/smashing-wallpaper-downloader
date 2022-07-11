import time

import requests
from calendar import month_name
from bs4 import BeautifulSoup
import re

import asyncio
import aiohttp


SMASHING_URL = 'https://www.smashingmagazine.com/'


def validate_date_input(date):
    date_pattern = r'\b[01]\d20(1[2-9]|[2-9]\d)\b'
    if not re.match(date_pattern, date):
        raise ValueError(
            'The "date" argument is not a valid date (i.e. 012018). The earliest date available: January 2012.'
        )


def validate_resolution_input(resolution):
    resolution_pattern = r'\b\d{3,4}x\d{3,4}\b'
    if not re.match(resolution_pattern, resolution):
        raise ValueError('The "resolution" argument is not valid')


def make_custom_url(date):
    month_posted = month_name[int(date[:2])].lower()
    year_posted = date[2:]

    if not month_posted == 'january':
        month_created = '0' + str(int(date[:2]) - 1)
        year_created = year_posted
    else:
        month_created = '12'
        year_created = str(int(year_posted) - 1)

    url = SMASHING_URL + f'{year_created}/{month_created}/desktop-wallpaper-calendars-{month_posted}-{year_posted}/'
    return url


def get_image_url_list(url, resolution):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    img_list = soup.find_all('a', string=resolution)
    url_list = [item.attrs['href'] for item in img_list]
    return url_list


async def aiohttp_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            assert response.status == 200
            return await response.content.read()


async def download_image(url):
    response = await aiohttp_get(url)

    img_name = re.findall(r'[^/]*$', url)[0]  # i.e. 'jan-18-open-the-doors-of-the-new-year-cal-640x480.png'
    with open(f'wallpapers/{img_name}', 'wb') as file:
        file.write(response)
        print('{} downloaded successfully.'.format(img_name))


async def download_wallpapers(date, resolution):
    """ download desktop wallpapers in requested resolution """

    validate_date_input(date)
    validate_resolution_input(resolution)

    url = make_custom_url(date)

    start = time.time()
    print('Start downloading..')

    futures = [download_image(image_url) for image_url in get_image_url_list(url, resolution)]
    for i, future in enumerate(asyncio.as_completed(futures)):
        result = await future
    print('Process finished. Success for {} images in {} resolution'.format(i, resolution))

    print('Async downloading process finished in {:.2f}'.format(time.time() - start))


if __name__ == '__main__':
    date_input = input('Date: ')
    resolution_input = input('Resolution: ')
    # date_input, resolution_input = ('042018', '640x480')
    asyncio.run(download_wallpapers(date_input, resolution_input))
