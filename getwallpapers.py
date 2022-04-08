import click
import requests
from calendar import month_name


def getwallpapers(date, img_resolution):
    month, year = date[:2], date[2:]
    name_of_month = month_name(int(month))
    request = requests.request(f'https://www.smashingmagazine.com/{year}/{month}/'
                               f'desktop-wallpaper-calendars-{name_of_month}-{year}/')
