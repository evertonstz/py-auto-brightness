from setuptools import setup
from pyautobrightness import __version__

setup(
    name='pyautobrightness',
    version=__version__,
    author='Everton Correia',
    author_email='evertonjcorreia@gmail.com',
    packages=['pyautobrightness'],
    keywords=['Brightness', 'Auto', 'Webcam'],
    url='https://github.com/evertonstz/py-auto-brightness',
    platforms='Unix',
    download_url='https://github.com/evertonstz/py-auto-brightness/tarball/0.2',
    license='GNU',
    description='A very simple software to change the screen brightness using a webcam as light sensor.',
    entry_points={'console_scripts': ['pyautobrightness = pyautobrightness.pyautobrightnessmain:main']}
)
