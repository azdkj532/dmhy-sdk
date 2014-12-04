from setuptools import setup

setup(name='dmhy',
      version='1.0',
      description='a parser for dmhy',
      url='http://github.com/azdkj532/dmhy/',
      author='azdkj AZ',
      author_email='azdkj532@gmail.com',
      license='?',
      packages=['dmhy'],
      install_requires=[
          'BeautifulSoup4',
          'urllib3'
      ],
      zip_safe=False)
