# VERY BIG REALISATION 
# WORKS ONLY FOR VERTICALLY DISPLAYED PAGES

from bs4 import BeautifulSoup
import urllib
import requests
import webbrowser
import os
import lxml
import html.parser

def join_with_flipkart(tail, qry):
    
    fk = 'https://www.flipkart.com'
    qparam = '/search?q='
    
    # joining not as a query
    if qry==0:
        return fk+tail
    # join as a query
    else:
        return fk + qparam + tail

# asking the user what he wants to search
qry = input('What Items Do you Want to Search \n Example : \'Laptop i7\' \'Wireless Mouse\' : \n')

url = join_with_flipkart(qry, 1)

# webbrowser.open(url)

response = requests.get(url)

if response.status_code >= 400:
    print('BAD REQUEST')
    quit()

html = response.text

# either one will work 'lxml' or 'html.parser'
soup = BeautifulSoup(html, 'lxml')
# soup = BeautifulSoup(html, 'html.parser')

# everything inside the main div is a link wherever i click this redirects me to a new page containing the item
inner_links = soup.find_all('a', class_ ='_31qSD5')

for link in inner_links:
    # link to the product
    # WE ARE EXTRACTING THIS TO ADD IN CSV MODULE FURTHER
    # href = fk + link['href']
    # using the function()
    href = join_with_flipkart(link['href'], 0)

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
    mrp = (link.find('div', class_='_3auQ3N _2GcJzG'))
    # BUG_FIX
    if mrp == None:
        mrp = 'MRP for this item is not available'
    else:
        mrp = mrp.text[1:]

    # SP(selling price of the item) of the item
    sp = (link.find('div', class_='_1vC4OE _2rQ-NK').text)[1:]

    # discount span
    disc = link.find('div', class_ = 'VGWI6T')
    if disc == None:
        disc = 'No Discount On This Item'
    else:
        disc = disc.span.text

    # FRONTLINE SPECS: -- showed as an unordered list
    ul = link.find('ul', class_ = 'vFw0gD')
    # all_lis is a list of all the list item texts
    all_lis = ul.find_all('li')
    
    print()
    # PRINTING THE FRONTLINE SPECS
    print(' MAIN SPECS OF THIS ITEM ARE : ')
    for one_li in all_lis:
        print(one_li.text)

# -----------------------------------------FAIL IMAGE EXTRACTION--------------------------------
    # img_tag = link.find('img', class_='_1Nyybr')
    # print(img_tag['src'])
    # OR EVEN THIS CAN BE USED
    # img_tag = link.find('div', class_ = '_3SQWE6').img

    # if image is available
    # if img_tag == None:
    #     img_src = None
    # else:
    #     img_src = img_tag['src']
    # print(img_src)
# --------------------------------------------------------------------------------
    
    print()
    print('MRP : ', mrp)
    print('Sale Price : ', sp)
    print('Discount : ',disc )
    print('----------------------------------------\n')
