import requests
from bs4 import BeautifulSoup
import csv
import time
import multiprocessing


start = time.perf_counter()
base_url = 'https://www.rapid7.com/db/?type=nexpose'

file_name = 'information.csv' # Stores in information.csv file
file = open(file_name,'w')
writer = csv.writer(file)
file = writer.writerow(["Vulnerability", "PublishedDate", "Severity"]) # Header of csv file

###### Extracting from first page #########
source = requests.get(base_url).text
soup = BeautifulSoup(source,'html.parser')

# section = soup.find('div', class_='resultblock__info')

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

section = soup.findAll('div', class_='resultblock__info')

def fromFirst():
    global section
    global base_url
    global file_name
    global file
    global writer
    global source
    global soup
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

def fromOther():
    # all global variables
    global section
    global base_url
    global file_name
    global file
    global writer
    global source
    global soup

    page_count = 2
    pages = 11 # scrapping 10 pages
    while page_count < pages:
        source = requests.get(base_url+"&page="+str(page_count)).text
        print(base_url+"&page="+str(page_count))
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
        print(f"Page no: = {page_count}")
        page_count = page_count + 1
        print("\n\n")

def parallelProcessing():
    process_list = []
    process_first = multiprocessing.Process(target=fromFirst)
    process_second = multiprocessing.Process(target=fromOther)
    process_first.start()
    process_second.start()

    process_first.join()
    process_second.join()
    # process_list.append(process_first)
    # for _  in range(5):
    #     other_process = multiprocessing.Process(target=fromOther)
    #     other_process.start()
    #     process_list.append(other_process)
    # for process in process_list:
    #     process.join()



if __name__ == '__main__':
    # fromFirst()
    # fromOther()
    parallelProcessing()
    end = time.perf_counter()
    print(f"Execution time: {round(end-start,2)} sec")


######## Extracting from other pages ############
# page_count = 1
# pages = 10 # scrapping 10 pages
# while page_count < pages:
#     source = requests.get(base_url+"&page="+str(page_count)).text
#     soup = BeautifulSoup(source,'html.parser')
#     section = soup.findAll('div', class_='resultblock__info')
#     for i in section:
#         info_list = []
#     # Extracting vulnerability
#     try:
#         vul = i.find('div', class_='resultblock__info-title').text
#         vul = vul.replace('\n','').replace(' ','')
#         info_list.append(vul)
#     except:
#         info_list.append(None)

#     # Extracting Published_date and severity
#     try:
#         pub_sev = i.find('div', class_="resultblock__info-meta").text
#         l = pub_sev.replace(' ','').split('|') # Seperating published date and severity

#         l_pub = l[0].replace('\n','').split(':') # remove \n from published date
#         pub_date = l_pub[1].replace('\r','') # filter out everything from published date
#         info_list.append(pub_date)
#     except:
#         info_list.append(None)

#     try:
#         l_sev = l[1].replace('\n','').split(':') # remove \n from severity
#         sev = l_sev[1].replace('\r','') # filter out everything from severity
#         info_list.append(sev)
#     except:
#         info_list.append(None)
    
#     writer.writerow(info_list)
#     page_count = page_count + 1



    