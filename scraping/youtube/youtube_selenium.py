####################
# Skip Youtube Ads
####################

# libraries used
import time

# selenium
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
capabilities = DesiredCapabilities.CHROME.copy()
capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
# chrome_options.add_argument("--headless") # Run selenium in headless mode

#driver = webdriver.Chrome(ChromeDriverManager(path = "/kellogg/proj/<YOUR_NEDID>/drivers/").install(), desired_capabilities=capabilities,options=chrome_options)
driver = webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=capabilities,options=chrome_options)
driver.set_page_load_timeout(60) # times out page after attempting to load for 10 seconds

#########################################
## Functions ##
###############

# Skip Youtube Ads
def skip_ads():

    # wait for ad to laod
    time.sleep(10)

    # click on ad button
    try:
        button = driver.find_element_by_class_name('ytp-ad-skip-button-container')
        button.click()
        print("Ad skipped. I push the button.")

    except:
        print("no ads")


def scroll_down(scroll_pause=2):

    try:
        scroll_height_init = driver.execute_script("return document.documentElement.scrollHeight") # current scroll height
        while True:
            driver.execute_script("window.scrollTo(0, arguments[0]);", scroll_height_init)
            time.sleep(scroll_pause)

            # Calculate new scroll height and compare with last scroll height
            scroll_height_new = driver.execute_script("return document.documentElement.scrollHeight")
            if scroll_height_new == scroll_height_init:
                break
            scroll_height_init = scroll_height_new
        print("scrolled to bottom")

    except:
        print("failed")

#########################################
## Inputs ##
############

#url = 'https://www.youtube.com/watch?v=axBtzSNir1E'
url = 'https://www.youtube.com/results?search_query=i+push+the+button+plucky+duck'

#########################################
## To Run ##
############

def main():
  
    driver.get(url)
    #skip_ads()
    time.sleep(20)
    scroll_down()
    print("finished running")
    driver.quit()


if __name__ == "__main__":
    main()
#########################################
