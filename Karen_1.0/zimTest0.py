from libzim.reader import File

f = File("data/wikipedia_en_all_nopic_2024-06.zim")
article = f.get_article("article/url.html")
print(article.url, article.title)
if not article.is_redirect():
    print(article.content)
