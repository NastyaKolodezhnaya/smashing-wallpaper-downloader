import unittest
import getwallpapers
import requests


class TestGetWallpapers(unittest.TestCase):

    def test_validate_date_input(self):
        date = 'date'
        with self.assertRaises(ValueError):
            getwallpapers.validate_date_input(date)

    def test_validate_resolution_input(self):
        resolution = '000000'
        with self.assertRaises(ValueError):
            getwallpapers.validate_resolution_input(resolution)

    def test_make_custom_url(self):
        date = '012018'
        result_url = getwallpapers.make_custom_url(date)
        request = requests.get(result_url)
        self.assertEqual(request.status_code, 200)

    def test_get_image_url_list(self):
        url = 'https://www.smashingmagazine.com/2020/01/desktop-wallpaper-calendars-february-2020/'
        resolution = '0'
        self.assertEqual(getwallpapers.get_image_url_list(url, resolution), [])


unittest.main()
