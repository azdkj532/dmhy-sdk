from setuptools import setup

setup(name='dmhy',
      version='1.1',
      description='a parser for dmhy',
      url='http://github.com/azdkj532/dmhy/',
      author='azdkj AZ',
      author_email='azdkj532@gmail.com',
      license='?',
      py_modules=['dmhy'],
      install_requires=[
          'BeautifulSoup4',
          'requests'
      ],
      zip_safe=False)
