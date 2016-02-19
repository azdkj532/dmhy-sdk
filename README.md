# dmhy

## Desciption

a really simple library for dmhy ( http://share.dmhy.org/ )

## Functions

### search

keywords
it needs one parameter which can be a string or a list.
note that when using string type, all keywords should split by space.
return a list contains all topics in first page of searching result.

## Class

### AnimateEntry

This class contains fields such `title`, `date`, `url`, `magnet` whch
represents an animate search record.

## Installation

```
pip3 install git+https://github.com/azdkj532/dmhy-sdk.git
```

## Usage

```python
import dmhy

for record in dmhy.search('shinsekai'):
    print('%s - %s\n%s' % (record.date, record.title, record.url))
```

## Dependency

- BeautifulSoup4
- requests
