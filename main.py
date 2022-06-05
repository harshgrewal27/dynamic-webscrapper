from urllib.request import urlopen as ureq
from bs4 import BeautifulSoup as soup
import pandas as pd
import app



def search(search,save):
    search = search.replace(" ", "%20")

    # -------------------------parse and search given url-------------------------------------------------
    url = f"https://www.flipkart.com/search?q={search}&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
    uClient = ureq(url)
    html_text = uClient.read()
    uClient.close()
    page_soup = soup(html_text, "html.parser")
    items(page_soup,search,save)

def items(page_soup,search,save):
    items = page_soup.find_all("div", class_="_4rR01T")
    ratings = page_soup.find_all("div", class_="_3LWZlK")
    prices = page_soup.find_all("div", class_="_30jeq3 _1_WHN1")
    if len(items)!=0:
        ConvDF(*(items, ratings, prices),search,save)
    elif len(items) == 0:
        items = page_soup.find_all("div", class_="_2WkVRV")
        if len(items)==0:
            items = page_soup.find_all("a", class_="s1Q9rs")
        prices = page_soup.find_all("div", class_="_30jeq3")
        if len(items) != 0:
            ConvDF(*(items, ratings, prices),search,save)
    if len(items) == 0:
        print("Items not found")
        exit()


def ConvDF(i,r,p,s,save):
    itemdf=[]
    for (item, rating, price) in zip(i, r, p):
        itemdf.append((item.get_text(),float(rating.get_text()),price.get_text()))
    df=pd.DataFrame(itemdf,columns=["Item","Rating","Price"])
    s=s.replace("%20"," ")
    if save==True:
        df.to_excel(f"output/{s}.xlsx",index=False)
        file=f"{s}.xlsx"
        app.save(file)
    else:
        pass
    print(save)
    app.items(df)


if __name__ == '__main__':
    search()
