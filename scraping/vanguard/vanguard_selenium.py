from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome(ChromeDriverManager(path="/kellogg/proj/<YOUR_NETID>/drivers").install())
driver = webdriver.Chrome(ChromeDriverManager().install())

#########################################
## Functions ##
###############

# Skip Youtube Ads
def find_headings(soup):

    try:
        table = soup.find('div',{'class':"vga-overview-serch-results"})
        headings = table.findAll('div',{'class':"vga-headings-content"})
        print(len(headings))
        for i in headings:
           print(i.text)

    except:
        print("Table could not be found.")


#########################################
## Inputs ##
############
url = 'https://www.vanguard.com.au/personal/products/en/overview'

#########################################
## To Run ##
############

def main():
    
    driver.get(url)
    time.sleep(30)
    #with open("vanguard.html") as fp:
     #   soup = BeautifulSoup(fp, 'html.parser')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    find_headings(soup)
    driver.quit()


if __name__ == "__main__":
    main()
#########################################
