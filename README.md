# nasa-apod
Utilizes NASA APOD API to generate wallpapers with explanations. 
Will download images (single, random or all in date range), does not support other media types (such as video).
By default, adds explanation of daily images in watermarked footer.

# Install
## Configuration
Get your NASA API key [here](https://api.nasa.gov/index.html#apply-for-an-api-key)
Set `NASA_API_KEY` environment variable

## Dependencies
TODO
* PIL
* gtk
* requests

# Usage
`download_path` defaults to `~/wallpapers`

## Initialize
TODO

## Download single date
``` python
import NasaApod
NasaApod().download_single(datetime(2015, 07, 01))
```

## Download random
Defaults to `start_date=1995-06-20`, the first day NASA began posting regular pics
``` python
import NasaApod
NasaApod().download_random()
```
# Credit
NASA APOD access via [Bowshock](https://github.com/emirozer/bowshock) wrapper library
Open Sans font from [Font Squirrel](http://www.fontsquirrel.com/)
