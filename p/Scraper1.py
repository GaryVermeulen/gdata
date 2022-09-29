from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os

word = input('Enter the word to find the meaning : ')

req = Request(
    url = "https://www.vocabulary.com/dictionary/" + word + "",
    headers={'User-Agent': 'Mozilla/5.0'}
)

htmlfile = urlopen(req).read()
soup = BeautifulSoup(htmlfile, 'html.parser')

soup1 = soup.find(class_="short")

try:
    soup1 = soup1.get_text()
except AttributeError:
    print('Cannot find such word! Check spelling.')
    exit()

# Print short meaning
print ('-' * 25 + '->',word,"<-" + "-" * 25)
print ("SHORT MEANING: \n\n",soup1)
print ('-' * 65)

# Print long meaning
soup2 = soup.find(class_="long")
soup2 = soup2.get_text()
print ("LONG MEANING: \n\n",soup2)

print ('-' * 65)

# Print instances like Synonyms, Antonyms, etc.
soup3 = soup.find(class_="instances") 
txt = soup3.get_text()
txt1 = txt.rstrip()

print (' '.join(txt1.split()))

print ('-' * 65)

soup4 =soup.find(class_="word-definitions")
text = soup4.get_text()

text = os.linesep.join([s for s in text.splitlines() if s])

print('text:')
print(text)

