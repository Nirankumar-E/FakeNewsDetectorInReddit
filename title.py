import requests
from bs4 import BeautifulSoup

url = 'https://www.reddit.com/r/news/comments/1kekn7v/steelmaker_cleveland_cliffs_to_idle_3_steel/'

# Fetch and follow redirects
response = requests.get(url, allow_redirects=True)

# Parse HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Find <h1> with slot="title"
h1 = soup.find('h1', attrs={'slot': 'title'})

if h1:
    print(h1.text.strip())
else:
    print("No <h1 slot='title'> tag found.")
