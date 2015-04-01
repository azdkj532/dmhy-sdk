dmhy
====
##Desciption
a CLI tool for dmhy ( http://share.dmhy.org/ )

##Functions
###Search
it needs one parameter which can be a string or a list.
note that when using string type, all keywords should split by space.
return a list contains all topics in first page of searching result.
##Class
###dmhy
This class can create an instance which contains some attribute of each topics, 
includes title, url and magnet. Maybe I will add other attribute in the future.

Note that attribute 'magnet' won't contain any data before calling the setter of the 'magnet'.
When something went wrong while getting the magnet link, magnet will be set to None.

##Usage
go to your working directory and clone this repo
```
git clone https://github.com/azdkj532/dmhy-sdk.git
```
install dependent package
```
python dmhy-sdk/setup.py install
```
open python file and import this package.
```python
import dmhy
```
that's all.
##Dependency


* BeautifulSoup4
* requests
