from __future__ import print_function
from __future__ import division

import os
from textwrap import wrap
from datetime import date

import bowshock
from PIL import Image, ImageColor, ImageFont, ImageDraw, ImageOps

from . import watermark
from . import date_utils
from . import file_utils

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

"""Downloads a NASA APOD image, with optional post-processing.
:param download_path: (optional) File location to store downloaded image (default ~/wallpapers).
:param screen_width: (optional) Pixels of width to make image. Large than original will add a black background. If not specified, OS detection of screen width will be attempted.
:param screen_height: (optional) Pixels of height to make image. Large than original will add a black background. If not specified, OS detection of screen width will be attempted.
:param font: (optional) TrueType font to apply in image footer (default OpenSans-Regular.ttf).
:param font_size: (optional) Size of TrueType font in image footer (default 18).
:param margin: (optional) Pixels around image footer text (default 50).
:param font_color: (optional) RGBA tuple for color of font (default white).
:param background_color: (optional) RBGA tuple for color of background (default black).
:param opacity: (optional) Opacity for image footer (default 0.8).
"""

"""
:param start_date: (optional) start of random range, uses date (default date(1995, 6, 20)).
:param end_date: (optional) end of random range, uses date (default today).
"""
def download_random(start_date=date(1995, 6, 20), end_date=date.today(), 
        **kwargs):
    rdate = date_utils.random_date(start_date, end_date)
    download_single(single_date=rdate, **kwargs)

"""
:param start_date: (optional) date to start downloading, uses date (default date(1995, 6, 20)).
:param end_date: (optional) date to end downloading, uses date (default today).
"""
def download_bulk(start_date=date(1995, 6, 20), end_date=date.today(), 
        **kwargs):
    for single_date in date_utils.date_range(start_date, end_date):
        download_single(single_date=single_date, **kwargs)
"""
:param: single_date: (optional) Specific date to download (default date.today())
"""
def download_single(single_date=date.today(), download_path="~/wallpapers", screen_width=None, screen_height=None,
        **kwargs):
    print("Downloading for date: {}".format(date_utils.format_date(single_date)))

    json = _call_api(single_date)
    media_type = json["media_type"]
    if media_type == "image":
        file = file_utils.download_url(json["url"], single_date, download_path)

        wallpaperize(file, json["explanation"],
            screen_width=screen_width, screen_height=screen_height,
            **kwargs)
    else:
        print("Media type {} not saveable".format(media_type))

def wallpaperize(file_path, msg,
        screen_width=None, screen_height=None,
        font_face=os.path.join(__location__, "OpenSans-Regular.ttf"), 
        font_size = 18, margin=50, font_color=(255,255,255,255),
        opacity=0.8, background_color=(0,0,0,0)):

    # Read font/facts
    font = ImageFont.truetype(font_face, font_size)
    font_height = font.getsize("a")[1]
    font_width = font.getsize("a")[0]

    # Default to tk if screen size not specified
    if screen_width == None or screen_height == None:
        import tkinter as tk
        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
    screen_size = (screen_width, screen_height)

    # Position calculations
    msg_width = screen_width/font_width*1.15
    lines = wrap(msg, msg_width)
    msg_height = len(lines) * font_height
    background_height = msg_height + (margin *2)
    offset = background_height - msg_height - (margin*1.5)

    # Generate background and text
    img = _resize_image(file_path, screen_width, screen_height, offset, background_color)
    text_bg = _add_text_bg(lines, screen_width, background_height, margin, offset, font, font_color, font_height)
    
    background_offset = screen_height - msg_height - margin    

    # Watermark footer and save
    final_img = watermark.watermark(img, text_bg, (0, background_offset), opacity)
    final_img.save(file_path)
    
def _resize_image(file_path, screen_width, screen_height, offset, background_color):
    screen_size = (screen_width, screen_height)
    print("Resizing to {0[0]}x{0[1]}".format(screen_size))
    
    img = Image.open(file_path)
    img_w, img_h = img.size
    img.thumbnail(screen_size, Image.ANTIALIAS)

    # Add background
    background = Image.new("RGB", screen_size, background_color)
    offset = ((screen_width - img_w) // 2, (screen_height - img_h) // 2)
    background.paste(img, offset)
    
    return background

def _add_text_bg(lines, screen_width, background_height, margin, offset, font, font_color, font_height):
    # Write  text
    text_bg = Image.new("RGBA", (screen_width, background_height), "gray")
    draw = ImageDraw.Draw(text_bg)

    for ln in lines:
        draw.text((margin, offset), ln, font_color, font)
        offset += font_height
    
    return text_bg

def _call_api(d):
    # TODO: bad connection
    return bowshock.apod.apod(date=date_utils.format_date(d)).json()

if __name__ == "__main__":
    download_single(date(2014, 4, 3))
    #download_random(start_date=date(2015, 1, 1))
    #download_all(start_date=date(2015, 7, 26))
