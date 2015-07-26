from gtk import gdk
from datetime import timedelta, datetime
from random import randint
from urllib import urlretrieve
from re import compile, IGNORECASE, MULTILINE
from urllib import urlretrieve
from urlparse import urlparse
from textwrap import wrap
from PIL import Image, ImageColor, ImageEnhance, ImageFont, ImageDraw, ImageOps
import requests
import os, subprocess, ConfigParser

class NasaApod:
    def __init__(self, download_path = "~/wallpapers", font="OpenSans-Regular.ttf",
            font_size=18, font_margin=50, font_color=(255,255,255,255), opacity=0.8,
            end_date=datetime.today(), start_date=datetime(1995, 06, 20),
            screen_width=gdk.screen_width(), screen_height=gdk.screen_height(),
            **kwargs):
        self._read_config()

        self.FONT_SIZE = font_size
        self.FONT_COLOR = font_color
        self.FONT = ImageFont.truetype(font, self.FONT_SIZE)
        self.FONT_HEIGHT = self.FONT.getsize("a")[1]
        self.FONT_WIDTH = self.FONT.getsize("a")[0]
        self.FONT_MARGIN = font_margin

        self.START_DATE = start_date
        self.END_DATE = end_date

        self.OPACITY = opacity

        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height

        self.DOWNLOAD_PATH = os.path.expanduser(download_path)
        if not os.path.exists(self.DOWNLOAD_PATH):
            os.makedirs(self.DOWNLOAD_PATH)


    def _read_config(self):
        config = ConfigParser.RawConfigParser()
        config.read("config.ini")
        if config.has_section("apod") and config.has_option("apod", "api_key"):
            self.API_KEY = config.get("apod","api_key")
            self.API_URL = "https://api.nasa.gov/planetary/apod?api_key=%s&format=JSON" % self.API_KEY
        else:
            raise Error("Config.ini must contain [apod] section with 'api_key'")


    def call_api(self, d):
        url = "%s&date=%s" % (self.API_URL, self._format_date(d))
        print "Downloading %s in %sX%s from %s" % (self._format_date(d), self.SCREEN_WIDTH, self.SCREEN_HEIGHT, url)

        r = requests.get(url);
        return r.json();

    def download_random(self):
        rdate = self._random_date(self.START_DATE, self.END_DATE).date()
        self.download_single(rdate)

    def download_all(self):
        for single_date in self._date_range(self.START_DATE, self.END_DATE):
           self.download_single(single_date)

    def download_single(self, d):
        t = self.call_api(d)
        media_type = t["media_type"]
        if media_type == "image":
            file = os.path.join(self.DOWNLOAD_PATH, self._format_date(d)+"_"+self._image_name(t["url"]))
            print "Downloading image: %s" % file
            urlretrieve(t["url"], file)
            size = (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)

            print "Resizing to %sx%s" % size
            img = Image.open(file)
            img_w, img_h = img.size
            img.thumbnail(size, Image.ANTIALIAS)

            background = Image.new('RGB', size, (0,0,0,0))
            offset = ((self.SCREEN_WIDTH - img_w) / 2, (self.SCREEN_HEIGHT - img_h) / 2)
            background.paste(img, offset)

            self._write_explanation(background, file, t["explanation"])
        else:
            print "Media type %s not saveable" % media_type

    def _write_explanation(self, img, file, msg):
        margin = self.FONT_MARGIN
        msg_width = self.SCREEN_WIDTH/self.FONT_WIDTH*1.15
        lines = wrap(msg, msg_width)
        msg_height = len(lines) * self.FONT_HEIGHT
        background_height = msg_height + (margin *2)
        offset = background_height - msg_height - (margin*1.5)

        text_bg = Image.new("RGBA", (self.SCREEN_WIDTH, background_height), "gray")

        draw = ImageDraw.Draw(text_bg)
        for t in lines:
            draw.text((margin, offset), t, self.FONT_COLOR, self.FONT)
            offset += self.FONT_HEIGHT

        background_offset = self.SCREEN_HEIGHT - msg_height - margin
        #img.paste(self.reduce_opacity(text_bg), (0, background_offset))
        self.watermark(img, text_bg, (0, background_offset), self.OPACITY).save(file)
        #img.save(file)

    def watermark(self, im, mark, position, opacity=1):
        """Adds a watermark to an image."""
        if opacity < 1:
            mark = self.reduce_opacity(mark, opacity)
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        # create a transparent layer the size of the image and draw the
        # watermark in that layer.
        layer = Image.new('RGBA', im.size, (0,0,0,0))
        if position == 'tile':
            for y in range(0, im.size[1], mark.size[1]):
                for x in range(0, im.size[0], mark.size[0]):
                    layer.paste(mark, (x, y))
        elif position == 'scale':
            # scale, but preserve the aspect ratio
            ratio = min(
                float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
            w = int(mark.size[0] * ratio)
            h = int(mark.size[1] * ratio)
            mark = mark.resize((w, h))
            layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
        else:
            layer.paste(mark, position)
        # composite the watermark with the layer
        return Image.composite(layer, im, layer)

    def reduce_opacity(self, im, opacity):
        """Returns an image with reduced opacity."""
        assert opacity >= 0 and opacity <= 1
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        else:
            im = im.copy()
        alpha = im.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        im.putalpha(alpha)
        return im

    def _format_date(self, d):
        return d.strftime("%Y-%m-%d")

    def _date_range(self, start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def _random_date(self, start, end):
        return start + timedelta(
            seconds=randint(0, int((end - start).total_seconds())))

    def _image_name(self, url):
        path = urlparse(url).path
        return path.split("/")[-1]



if __name__ == '__main__':
    NasaApod(start_date=datetime(2015, 01, 01)).download_random()
    #NasaApod().download_single(datetime(2014,06,25))
    #NasaApod(start_date=datetime(2015, 02, 24)).download_all()
