import requests
from bs4 import BeautifulSoup

# Gets user input for song details
print('Enter the details of a song you want the guitar tabs for!')
songArtist = input("Artist: ")
songTitle = input("Title: ")

searchRequest = ""

# formats user input into a url (to search the website)
for c in songArtist:
    if c == ' ':
        c = '+'
    searchRequest += c
searchRequest += '+'
for c in songTitle:
    if c == ' ':
        c = '+'
    searchRequest += c

# fetches url
initialURL = 'https://www.guitaretab.com/fetch/?type=tab&query=' + searchRequest
initialPage = requests.get(initialURL)

initialParser = BeautifulSoup(initialPage.content, 'html.parser')

# checks for 0 results
try:
    links = initialParser.find_all('div', class_='gt-list__cell gt-list__cell-title')[0]
except:
    print('We could not find a guitar tab for', songTitle, 'by', songArtist, 'on guitaretab.com')
    exit()

urlExtension = ''
for a in links.find_all('a', href=True):
    urlExtension = (a['href'])

tabURL = "https://www.guitaretab.com" + urlExtension
tabPage = requests.get(tabURL)

# finds tablurature in HTML
tabParser = BeautifulSoup(tabPage.content, 'html.parser')
tab = tabParser.find_all('section', class_='js-tab')

guitartabs = []
for line in tab:
    guitartabs.append(line.find('div', class_='gt-tab-content whitebg js-tab-container'))

# saves tab as text file
formattedTabs = guitartabs[0].get_text(separator='\n')
fileName = songArtist + " - " + songTitle + '.txt'
with open(fileName, 'w') as f:
    f.write(formattedTabs)
    print(fileName, ' has been successfully downloaded!')