#!/usr/bin/env python
# coding: utf-8

# ## Imports

# In[1]:

import pickle
import requests
from bs4 import BeautifulSoup
from time import sleep


# ## Helper functions

# In[ ]:


def get_pars(link, parser='html.parser'):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, parser)
    return soup

def get_sub_categories(soup,selector):
    # get sub categories
    sub_categories = soup.select(selector)

    list_of_subcategories = []
    for each_category in sub_categories:
        list_of_subcategories.append(['https://www.digikala.com' + each_category.get('href'), each_category.get_text()])
#         print('https://www.digikala.com' + each_category.get('href'), each_category.get_text())
    return list_of_subcategories

def check_url(link):
    if not 'digikala.com' in link:
        return 'https://digikala.com' + link
    else:
        return link


# ## Page related configs

# In[ ]:


categories_selector = "body header nav div div ul li ul li div div ul li a"
sub_categories_selector = "div article div section div ul li a"
product_in_subcategories_selector = "div div div div div article div ul li div div div div a"


# ## Main

# In[ ]:


# get categories
soup = get_pars("https://digikala.com")
categories = soup.select(categories_selector)
l =[]
list_of_categories = []
for each in categories:
    if each.get('href') not in l:
        l.append(each.get('href'))
        list_of_categories.append([each.get('href'),each.get_text().strip()])
del l
# list_of_categories


# In[ ]:


list_of_search_pages =[]
for each_category in list_of_categories:
    if '/main/' in each_category[0]:
        link = check_url(each_category[0])
        soup = get_pars(link)
        temp_sub = get_sub_categories(soup,sub_categories_selector)
        for i in temp_sub:
            list_of_search_pages.append(i[0])
    elif '/search' in each_category[0]:
        link = check_url(each_category[0])
        list_of_search_pages.append(link)
    else:
        print(each_category)


# In[ ]:


# list_of_search_pages


# In[ ]:


modified_list_of_search_pages = []
for each in list_of_search_pages:
    for i in range(1,6):
        modified_list_of_search_pages.append(each + '?pageno={}&sortby=4'.format(i))
list_of_search_pages = modified_list_of_search_pages
del modified_list_of_search_pages


# In[ ]:


# list_of_search_pages


# In[ ]:

list_of_all_products = []
for each_search_page in list_of_search_pages:
    soup = get_pars(each_search_page)
    products = soup.select(product_in_subcategories_selector)
    list_of_page_products = []
    for each_product in products:
        list_of_page_products.append(['https://www.digikala.com' + each_product.get('href'),each_product.get_text()])
        print('https://www.digikala.com' + each_product.get('href'),each_product.get_text())
    list_of_all_products.append(list_of_page_products)
    sleep(5)

    with open('data.pkl','wb') as f:
        pickle.dump(list_of_all_products,f)
