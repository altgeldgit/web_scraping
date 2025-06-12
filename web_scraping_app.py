#Recommned OS: Windows
#hint1: https://stackoverflow.com/questions/70523233/problems-scraping-a-dynamic-website-with-beautiful-soup
#hint2: https://stackoverflow.com/questions/47417581/selenium-chromedriver-how-to-disable-the-messagedevtools-on-ws
#hint3: https://stackoverflow.com/questions/38412495/difference-between-os-path-dirnameos-path-abspath-file-and-os-path-dirnam
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests

try:
    py_dir = os.path.dirname(os.path.abspath(__file__))
    txt_path = os.path.join(py_dir, "web_scraping_app_output.txt")
    #output will be collected here at each page
    all_output = []

    is_all_pages = False
    #https://xkcd.com/1193/ is different for hover_text: it uses dynamic content with javascript
    url_input = "https://xkcd.com/1/"
    url_main = "https://xkcd.com"
    ##output vars
    comic_number = 1
    comic_title = ""
    hover_text = ""
    image_link = ""

    while not is_all_pages:
        #show page number because waiting is boring
        print(f"current page: \"{comic_number}\"")

        #show comic_number
        all_output.append(f"Comic Number: \"{comic_number}\"\n")
        # print(f"Comic Number: \"{comic_number}\"")

        #init requests and BeautifulSoup
        response = requests.get(url_input)
        html_data = response.text
        soup = BeautifulSoup(html_data, "html.parser")
        
        #get comic_title
        comic_title = soup.find(id="ctitle").text
        all_output.append(f"Comic Title: \"{comic_title}\"\n")
        # print(f"Comic Title: \"{comic_title}\"")

        #get hover_text
        hover_text = soup.find(id="comic").find("img")["title"]
        #it is empty at https://xkcd.com/1193/ because it uses javascript for dynamic content loading -> use selenium if it cannot find img title
        #potential error is from different OS than Windows. Use try/catch to continue scraping even after an error.
        try:
            if hover_text=="":
                options = Options()
                options.add_argument("--headless")
                driver = webdriver.Chrome(options=options)
                driver.get(url_input)
                soup = BeautifulSoup(driver.page_source, "html.parser")
                driver.quit()
                hover_text = soup.find(id="comic").find("div", title = True)["title"]
        except Exception as err:
            # all_output.append(f"ERROR1: {err}")
            print(f"ERROR1: {err}")
        all_output.append(f"Hover Text:  \"{hover_text}\"\n")
        # print(f"Hover Text:  \"{hover_text}\"")

        #get image_link
        image_link = soup.find(id="comic").find("img")["src"]
        image_link = image_link.replace("https://imgs.xkcd.com", "imgs.xkcd.com").replace("//imgs.xkcd.com", "imgs.xkcd.com")
        all_output.append(f"Image Link: \"{image_link}\"\n\n")
        # print(f"Image Link: \"{image_link}\"\n")

        #get next comic_number from the link to the next page
        comic_number = soup.find("a", rel="next")["href"]
        url_input = url_main + comic_number
        comic_number = comic_number.replace("/", "")

        #check if there is next page
        if not comic_number.isdigit():
            is_all_pages = True

    with open(txt_path, "w", encoding="utf-8") as f:
        f.write("".join(all_output))

except Exception as err:
    print(f"ERROR2: {err}")
    