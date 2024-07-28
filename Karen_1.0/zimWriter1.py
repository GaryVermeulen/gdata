from libzim.writer import Creator, Item, StringProvider, FileProvider, Hint


class MyItem(Item):
    def __init__(self, title, path, content = "", fpath = None):
        super().__init__()
        self.path = path
        self.title = title
        self.content = content
        self.fpath = fpath

    def get_path(self):
        return self.path

    def get_title(self):
        return self.title

    def get_mimetype(self):
        return "text/html"

    def get_contentprovider(self):
        if self.fpath is not None:
            return FileProvider(self.fpath)
        return StringProvider(self.content)

    def get_hints(self):
        return {Hint.FRONT_ARTICLE: True}


content = """<html><head><meta charset="UTF-8"><title>Web Page Title</title></head>
<body><h1>Welcome to this ZIM</h1><p>Kiwix</p></body></html>"""

content2 = """<html><head><meta charset="UTF-8"><title>Web Page Title</title></head>
<body><h1>Welcome to this ZIM2</h1><p>Kiwix23</p></body></html>"""

item = MyItem("Hello Kiwix", "home", content)
#item2 = MyItem("Bonjour Kiwix", "home/fr", None, "home-fr.html")
item2 = MyItem("Bonjour Kiwix", "home/fr", content2)

with Creator("test.zim").config_indexing(True, "eng") as creator:
    creator.set_mainpath("home")
    creator.add_item(item)
    creator.add_item(item2)
    #illustration = pathlib.Path("icon48x48.png").read_bytes()
    #creator.add_illustration(48, illustration)
    for name, value in {
        "creator": "python-libzim",
        "description": "Created in python",
        "name": "my-zim",
        "publisher": "You",
        "title": "Test ZIM",
        "language": "eng",
        "date": "2024-06-30"
    }.items():

        creator.add_metadata(name.title(), value)
