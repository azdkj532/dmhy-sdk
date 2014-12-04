dmhy
====
##Desciption
a parser for dmhy ( http://share.dmhy.org/ )

##Functions
###Search
it needs one parameter which can be a string or a list.
note that when using string type, all keywords should split by space.
return a list contains all topics in first page of searching result.
###GetMagnetLink
it needs one parameter, an absolute url of topic.
return a magnet link.

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
<ul>
<li>BeautifulSoup4</li>
<li>urllib3</li>
</ul>
