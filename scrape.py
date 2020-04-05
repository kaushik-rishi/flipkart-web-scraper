from bs4 import BeautifulSoup
# to write into csv file
import csv
import urllib
import requests
import webbrowser
import os
import lxml
import html.parser
# we can also import the pandas for further analysis on the csv file but the import pandas as pd operation is very costly

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

# Creating a folder to store specs and navigating into that folder
os.mkdir('Specifications')
# print(os.getcwd())
os.chdir('Specifications')
# print(os.getcwd())

# csv FILE
csv_file = open('List Of Items.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['name', 'MRP', 'SP', 'Discount', 'Link to Buy'])

for link in inner_links:
    # link to the product
    # WE ARE EXTRACTING THIS TO ADD IN CSV MODULE FURTHER
    # href = fk + link['href']
    # using the function()
    href = join_with_flipkart(link['href'], 0)

    # to open all the links
    # webbrowser.open(href)

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

    print(' MAIN SPECS OF THIS ITEM ARE : ')
    # PRINTING THE FRONTLINE SPECS
    for one_li in all_lis:
        print(one_li.text)
        # pass

    try :
        file_name = name
        ctr=1
        while os.path.exists(file_name):
            file_name = name + str(ctr)
            ctr+=1
        with open(file_name, 'w') as wf:
            for one_li in all_lis:
                # writing the specs into the file
                wf.write(str(one_li.text) + '\n')
            
            wf.write(f'MRP : {mrp}\n')
            wf.write(f'Selling Price : {sp}\n')
            wf.write(f'Discount : {disc}\n')

    except:
        print(name, ' file couldnot be created because the file name was not valid')
        temp_file = input(f'please enter a name for this item {name} : \n')
        ctr = 1
        file_name = temp_file
        while os.path.exists(temp_file):
            file_name= temp_file + str(ctr)
            ctr += 1
        with open(file_name, 'w') as wf_temp:
            for one_li in all_lis:
                wf_temp.write(str(one_li.text)+'\n')
                
            wf_temp.write(f'MRP : {mrp}\n')
            wf_temp.write(f'Selling Price : {sp}\n')
            wf_temp.write(f'Discount : {disc}\n')
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

    l = [name ,mrp ,sp ,disc ,href]
    csv_writer.writerow(l)

csv_file.close()
