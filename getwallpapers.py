import click
import requests
from calendar import month_name
from bs4 import BeautifulSoup
import re


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


def download_image(url):
    img_name = re.findall(r'[^/]*$', url)[0]  # i.e. 'jan-18-open-the-doors-of-the-new-year-cal-640x480.png'
    request_image = requests.get(url)
    if request_image.status_code == 200:
        with open(f'wallpapers/{img_name}', 'wb') as file:
            file.write(request_image.content)
            click.echo(f'{img_name} downloaded successfully.')


@click.command()
@click.argument('date', type=str)
@click.argument('resolution', type=str)
def getwallpapers(date, resolution):
    """ download desktop wallpapers in requested resolution """

    validate_date_input(date)
    validate_resolution_input(resolution)

    url = make_custom_url(date)

    image_count = 0
    for image_url in get_image_url_list(url, resolution):
        download_image(image_url)
        image_count += 1
    click.echo(f'Process finished. Success for {image_count} images in {resolution} resolution')


if __name__ == '__main__':
    getwallpapers()
