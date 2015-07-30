"""
apod-wallpaper
--------------

Utilizes NASA APOD API to generate wallpapers with explanations.
* Will download images (single, random or all in date range)
* Only supports image media types (no video).
* Uses tkinter to attempt to size wallpaper if not specified.
* By default, adds explanation of daily images in watermarked footer.

Install
-------
pip install apod-wallpaper

Configuration
-------------
Get your `NASA API key <https://api.nasa.gov/index.html#apply-for-an-api-key>`

Set NASA_API_KEY environment variable to your key.

Download single date
````````````````````
.. code:: python
from apod_wallpaper import apod
from datetime import date

apod.download_single(single_date=date(2015, 07, 01))

Download random
* Defaults to `start_date=date(1995, 6, 20)` (the first day NASA began posting daily pics), and  `end_date=date.today()`
```````````````
.. code:: python

from apod_wallpaper import apod

apod.download_random()

Download bulk
* Select range of APOD (good for catching up on recent misses)
```````````````
.. code:: python

from apod_wallpaper import apod
from datetime import date

apod.download_bulk(start_date=date(2015, 07, 01), end_date=date(2015, 07, 05))

# All NASA APOD images (BE NICE: you probably don't need this)
from apod_wallpaper import apod

apod.download_bulk()

Optional arguments
``````````````````
download_path: (optional) File location to store downloaded image (default ~/wallpapers).
screen_width: (optional) Pixels of width to make image. Large than original will add a black background. If not specified, OS detection of screen width will be attempted.
screen_height: (optional) Pixels of height to make image. Large than original will add a black background. If not specified, OS detection of screen width will be attempted.
font: (optional) TrueType font to apply in image footer (default OpenSans-Regular.ttf).
font_size: (optional) Size of TrueType font in image footer (default 18).
margin: (optional) Pixels around image footer text (default 50).
font_color: (optional) RGBA tuple for color of font (default white).
background_color: (optional) RBGA tuple for color of background (default black).
opacity: (optional) Opacity for image footer (default 0.8).

Development
```````````
`Github <http://github.com/jasonh-n-austin/nasa-apod-wallpaper>`
"""

from io import open
import os, sys, re, ast
from setuptools import setup
from pip.req import parse_requirements

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('apod_wallpaper/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


install_reqs = parse_requirements("requirements.txt")
reqs = [str(ir.req) for ir in install_reqs]

if sys.argv[-1] == 'publish':
    for cmd in [
            'python setup.py register sdist upload',
            'git tag {}'.format(version),
            'git push origin master --tag']:
        subprocess.check_call(cmd, shell=True)
    sys.exit(0)

setup(
    name='apod-wallpaper',
    version=version,
    url='https://github.com/jasonh-n-austin/python-apod-wallpaper',
    description='NASA APOD wallpaper download',
    long_description=__doc__,
    author='Jason Harmon',
    author_email='jason.harmon@gmail.com',
    packages = ['apod_wallpaper'],    
    include_package_data=True,
    zip_safe=False,
    platforms='any',    
    package_dir={'apod_wallpaper': 'apod_wallpaper'},
    install_requires=reqs,
    license='Apache 2.0',
    classifiers=(
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
        'Topic :: Software Development :: Libraries :: Python Modules'
    )
)
