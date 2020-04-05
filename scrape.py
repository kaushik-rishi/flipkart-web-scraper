from bs4 import BeautifulSoup
import urllib
import requests
import webbrowser

# asking the user what he wants to search
# qry = input('What Items Do you Want to Search \n Example : \'Laptop i7\' \'Wireless Mouse\' : \n')

fk = 'https://www.flipkart.com'
# query = '/search?q='
url = 'https://www.flipkart.com/search?q=laptop%20i7'
response = requests.get(url)
html = response.text
# either one will work 'lxml' or 'html.parser'
soup = BeautifulSoup(html, 'lxml')
# soup = BeautifulSoup(html, 'html.parser')

inner_links = soup.find_all('a', class_ ='_31qSD5')

soup_links = []
no_of_sr=0

# for link in inner_links:
#     soup_links.append(BeautifulSoup(str(link), 'lxml'))
#     no_of_sr+=1

# l = inner_links[0].find_all('div', class_='_3SQWE6')
# print(l)

for link in inner_links:
    # link to the product
    href = fk + link['href']
    # name of the product -- name + proccessor
    name =(link.find('div', class_='col col-7-12')).find('div','_3wU53n').text
    try:
        idx = name.index('-')
    except Exception as e:
        pass
    else:
        name = name[:idx]
    print(name)

    # slicing the mrp and sp from index 1 is beause of the inability of python to render and inability of the terminal/powershell to print rupee symbol

    # MRP of the item
    mrp = (link.find('div', class_='_3auQ3N _2GcJzG')).text
    # SP(selling price of the item) of the item
    sp = (link.find('div', class_='_1vC4OE _2rQ-NK').text)[1:]

    print(mrp)
    print(sp)
    print('\n')
