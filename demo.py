import dmhy

keyword = input("Keyword: ")
print("Searching result for", keyword)

for topic in dmhy.search(keyword):
    print(topic.date + ' - ' + topic.title)
    print(topic.magnet[:64])
