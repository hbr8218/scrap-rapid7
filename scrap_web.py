import requests
from bs4 import BeautifulSoup
import csv

base_url = 'https://www.rapid7.com/db/?type=nexpose'

file_name = 'information.csv' # Stores in information.csv file
file = open(file_name,'w')
writer = csv.writer(file)
file = writer.writerow(["Vulnerability", "PublishedDate", "Severity"]) # Header of csv file

###### Extracting from first page #########
source = requests.get(base_url).text
soup = BeautifulSoup(source,'html.parser')

section = soup.findAll('div', class_='resultblock__info')

# vul = section.find('div', class_='resultblock__info-title').text
# vul = vul.replace('\n','').replace(' ','')

# pub_sev = section.find('div', class_="resultblock__info-meta").text
# # section = soup.find('a', class_="")
# l = pub_sev.replace(' ','').split('|') # Seperating published date and severity

# l_pub = l[0].replace('\n','').split(':') # remove \n from published date
# pub_date = l_pub[1].replace('\r','') # filter out everything from published date

# l_sev = l[1].replace('\n','').split(':') # remove \n from severity
# sev = l_sev[1].replace('\r','') # filter out everything from severity
# print("Vulnerability {}, Severity {}, Published_date {}".format(vul, sev, pub_date))

for i in section:
    info_list = []
    # Extracting vulnerability
    try:
        vul = i.find('div', class_='resultblock__info-title').text
        vul = vul.replace('\n','').replace(' ','')
        info_list.append(vul)
    except:
        info_list.append(None)

    # Extracting Published_date and severity
    try:
        pub_sev = i.find('div', class_="resultblock__info-meta").text
        l = pub_sev.replace(' ','').split('|') # Seperating published date and severity

        l_pub = l[0].replace('\n','').split(':') # remove \n from published date
        pub_date = l_pub[1].replace('\r','') # filter out everything from published date
        info_list.append(pub_date)
    except:
        info_list.append(None)

    try:
        l_sev = l[1].replace('\n','').split(':') # remove \n from severity
        sev = l_sev[1].replace('\r','') # filter out everything from severity
        info_list.append(sev)
    except:
        info_list.append(None)
    
    writer.writerow(info_list)


######## Extracting from other pages ############
page_count = 1
pages = 10 # scrapping 10 pages
while page_count < pages:
    source = requests.get(base_url+"&page="+str(page_count)).text
    soup = BeautifulSoup(source,'html.parser')
    section = soup.findAll('div', class_='resultblock__info')
    for i in section:
        info_list = []
    # Extracting vulnerability
    try:
        vul = i.find('div', class_='resultblock__info-title').text
        vul = vul.replace('\n','').replace(' ','')
        info_list.append(vul)
    except:
        info_list.append(None)

    # Extracting Published_date and severity
    try:
        pub_sev = i.find('div', class_="resultblock__info-meta").text
        l = pub_sev.replace(' ','').split('|') # Seperating published date and severity

        l_pub = l[0].replace('\n','').split(':') # remove \n from published date
        pub_date = l_pub[1].replace('\r','') # filter out everything from published date
        info_list.append(pub_date)
    except:
        info_list.append(None)

    try:
        l_sev = l[1].replace('\n','').split(':') # remove \n from severity
        sev = l_sev[1].replace('\r','') # filter out everything from severity
        info_list.append(sev)
    except:
        info_list.append(None)
    
    writer.writerow(info_list)
    page_count = page_count + 1

    