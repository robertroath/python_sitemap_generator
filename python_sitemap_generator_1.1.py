#prereqs: install python-apt, pip bs4
#working on python 3.8. haven't tried it in any other version
from bs4 import BeautifulSoup
import xml.etree.cElementTree as ET 
import requests, time, os, datetime

def ask_for_url():
    time.sleep(1)
    global url 
    url = ('<ENTER URL HERE>') #specify the url you want to scan here
    try:
        global response
        checking = url[-1] #getting last char of the string url
        if checking == "/":
            response = requests.get(url)
            start_crawling()
        else:
            url = url+"/"
            response = requests.get(url)
            start_crawling()
    except:
        print('Please write a valid URL: ex: https://www.yourdomain.com')
        ask_for_url()
    
def start_crawling():
    print('Crawling in process. Please stand by')
    time.sleep(3)
    global checked_links
    checked_links = []
    checked_links.append(url)
    crawling_web_pages()

def crawling_web_pages():
    global responses
    control = 0
    while control < len(checked_links):
        try:
            responses = requests.get(checked_links[control])
            source_code = responses.text
            soup = BeautifulSoup(source_code,"html.parser")
            new_links = [w['href'] for w in soup.findAll('a',href=True)] #getting links from that page
            counter = 0
            while counter < len(new_links):
                #this code is for links which start with a /
                if "http" not in new_links[counter]: #checking for absolute or relative linking
                    verify = new_links[counter][0] #getting first character of every link. if it starts with / will remove it. we already added one at the end of the domain
                    if verify == "/":
                        new_links[counter] = new_links[counter][:1].replace('/','') + new_links[counter][1:] #this will remove only the first / not every /
                        new_links[counter] = url+new_links[counter] #joining the domain with the relative url's
                        counter = counter + 1
                    else: #this code is for links that do not start with a /
                        new_links[counter] = url+new_links[counter] #joining the domain with the relative url's
                        counter = counter + 1  
                else:
                    counter = counter +1 
            else:
                counter2 = 0
                while counter2 < len(new_links):
                    #here is where we can apply filters. so if the links contain any of these strings. don't include these in the final array for the links on the site
                    #this also will never append a link to the array that already exists in the array. caution on changing this as it will result in it never ending
                    #this statement also only add links in the array that have the domain. Will not include redirects to another domain
                    if "#" not in new_links[counter2] and "mailto" not in new_links[counter2] and "tel" not in new_links[counter2] and "@" not in new_links[counter2] and ".jpg" not in new_links[counter2] and new_links[counter2] not in checked_links and url in new_links[counter2]:
                        checked_links.append(new_links[counter2])
                        print(str(control)+"/"+str(len(checked_links)))
                        print('')
                        print(str(control)+" Web Pages Crawled & "+str(len(checked_links))+" Web Pages Found")
                        print('')
                        print(new_links[counter2]) #displays the current url
                        counter2 = counter2 + 1
                    else:
                        counter2 = counter2 + 1
                else:
                    print(str(control)+"/"+str(len(checked_links)))
                    print('')
                    print(str(control)+" Web Pages Crawled & "+str(len(checked_links))+" Web Pages Found")
                    print('')
                    print(checked_links[control]) #displays the current url
                    control = control + 1
        except:
            control = control + 1
    else:
        print(str(len(checked_links))+" Web pages crawled")
        time.sleep(2)
        creating_sitemap()

def creating_sitemap():
    time.sleep(2)
    print('Creating sitemap...')
    urlset = ET.Element("urlset",xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    count = 0
    while count < len(checked_links):
        urls = ET.SubElement(urlset,"url")
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        ET.SubElement(urls,"loc",).text = str(checked_links[count])
        ET.SubElement(urls,"lastmod",).text = str(today)
        ET.SubElement(urls,"changefreq",).text = "daily"
        ET.SubElement(urls,"priority",).text = "1.00"
        count = count + 1
    else:
        tree = ET.ElementTree(urlset)
        tree.write("sitemap.xml")
        print("Sitemap ready...enjoy!")
        time.sleep(2)

ask_for_url()
