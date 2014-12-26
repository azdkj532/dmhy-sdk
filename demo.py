import dmhy
keyword = input("Keyin keywords:")
print("Searching result of", keyword)
for topic in  dmhy.Search(keyword):
    print(topic.title)
    print(topic.magnet[:40])
