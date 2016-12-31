from io import open
from codecs import open
import os, sys, re, ast, subprocess
from setuptools import setup
from pip.req import parse_requirements
from pip import download

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')
with open('apod_wallpaper/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

with open('README.rst', 'r', 'utf-8') as f:
        readme = f.read()

install_reqs = parse_requirements("requirements.txt", session=download.PipSession())
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
    long_description=readme,
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
