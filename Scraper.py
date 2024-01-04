import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


url = "https://s23.a2zinc.net/clients/WPA/SZ2022/Public/Exhibitors.aspx"
site_id = 'https://s23.a2zinc.net/clients/WPA/SZ2022/Public/eBooth.aspx?IndexInList=986&FromPage=Exhibitors.aspx&ParentBoothID=&ListByBooth=true&BoothID={}&fromFeatured=1'
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, 'lxml')
linked_html = soup.find_all('tr')
list_sam = []
id_list = []
web_links = []

for i in linked_html:
    check_linked = re.findall('LinkedIn URL', str(i))
    if bool(check_linked) == True:
        linked_web_child = i.find('a', class_='exhibitorName')     
        dic_l = {}
        dic_l['LinkedId_linked'] = linked_web_child
        list_sam.append(dic_l)
    else:
        pass
for x in list_sam[1:]:
    id = re.search('[0-9][0-9][0-9][0-9][0-9][0-9]', str(x))
    id2 = id.group()
    id_list.append(id2)

for sites in id_list:
    site_links = 'https://s23.a2zinc.net/clients/WPA/SZ2022/Public/eBooth.aspx?IndexInList=986&FromPage=Exhibitors.aspx&ParentBoothID=&ListByBooth=true&BoothID='+ str(sites) +'&fromFeatured=1'
    web_links.append(site_links)

master_list = []
master_list
counter = 1
print(len(web_links), "Sites were found that have LinkedIn Profiles")
print("Starting Data Scraping...")
for link in web_links[:10]:
    data_dict = {}
    response_1 = requests.get(link)
    html_1 = response_1.text
    soup_1 = BeautifulSoup(html_1, 'lxml')
    try:
        company_name = soup_1.find('h1').text.strip()
        data_dict['Company_Name'] = re.sub('\r|\n|&nbsp', '', company_name)

    except:
        pass

    try:
        linkedld1 = soup_1.find('a', id='ctl00_ContentPlaceHolder1_ctrlCustomField_Logos_dlCustomFieldList_ctl01_lnkCustomField')
        data_dict['linkedld_url'] = linkedld1.get('href')

    except:
        pass

    try:
        data_dict['company_website_url'] = soup_1.find('span', class_='BoothContactUrl').text.strip()

    except:
        pass

    try:
        city_with_comma = soup_1.find('span', class_='BoothContactCity').text.strip()
        state_unfil = soup_1.find('span', class_='BoothContactState').text.strip()
        state = re.sub(',|\r|\n|Â| ', '', state_unfil)
        city = re.sub('\r|\n|Â|                ', '', city_with_comma)
        data_dict['Location'] = city+state
        

    except:
        pass
  
    try:
        description = soup_1.find_all('p')
        description_full = ''
        for x in description:
            ld = re.findall('Questions?|Copyright |For Technical|BoothBrands|caption', str(x))
            if bool(ld) == False:
                des = x.text.strip()
                description_full += ' ' + str(des)
            else:
                pass
        try:
            description_full = re.sub('\xa0', ' ', description_full)

        except:
            pass
        data_dict['Description'] = description_full.strip()
    except:
        pass

    try:
        brands = soup_1.find('p', class_='BoothBrands').text.strip()
        data_dict['Brands'] = re.sub('\r|\n|Brands:', ' ', brands)

    except:
        pass
    master_list.append(data_dict)
    percent = str(float((counter / len(web_links)*100)))
    m = percent.split(".")
    n = str(m[0].strip())+"."+str(m[1].strip())[1]
    print(n+"% Completed")
    counter += 1


df = pd.DataFrame(master_list)
df.to_csv('Scraped_data.csv', index=False)
