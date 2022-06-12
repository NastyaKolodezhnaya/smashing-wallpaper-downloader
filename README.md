# Smashing wallpaper downloader
A CLI-utility that helps you download wallpapers from [smashingmagazine.com](https://www.smashingmagazine.com/category/wallpapers/) right from your terminal

## Running
```
git clone git@github.com:NastyaKolodezhnaya/smashing-wallpaper-downloader.git
docker build -t smashing_wallpaper .
docker run -it smashing_wallpaper
```
inside Docker container:

```
python getwallpapers.py <date> <resolution>
```

## Arguments format
- DATE: `012018` for January 2018 
- RESOLUTION: `800x480`
