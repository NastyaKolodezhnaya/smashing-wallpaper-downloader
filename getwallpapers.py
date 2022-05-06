import click
import requests
from calendar import month_name
from bs4 import BeautifulSoup
import re


def validate_user_input(date, resolution):
    try:
        date = int(date)
    except ValueError:
        raise ValueError('The "date" argument provided is not a valid date (i.e. 012018)')


def make_custom_url(date):
    month_posted = month_name[int(date[:2])].lower()
    year_posted = date[2:]

    if not month_posted == 'january':
        month_created = '0' + str(int(date[:2]) - 1)
        year_created = year_posted
    else:
        month_created = '12'
        year_created = str(int(year_posted) - 1)

    url = f'https://www.smashingmagazine.com/{year_created}/{month_created}/desktop-wallpaper-calendars-{month_posted}-{year_posted}/'
    return url


def get_image_url_list(url, resolution):
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    img_list = soup.find_all('a', string=resolution)
    url_list = [item.attrs['href'] for item in img_list]
    if not url_list:
        click.echo('Requested wallpaper are not found! Try enter another date or resolution')
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

    validate_user_input(date, resolution)
    url = make_custom_url(date)

    image_count = 0
    for image_url in get_image_url_list(url, resolution):
        download_image(image_url)
        image_count += 1
    click.echo(f'Process finished. Success for {image_count} images in {resolution} resolution')


if __name__ == '__main__':
    getwallpapers()
