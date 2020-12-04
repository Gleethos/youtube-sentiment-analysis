from pyppeteer import launch
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time


# for extended documentation visit --> https://miyakogi.github.io/pyppeteer/
# !!! function could only be called with await !!!
async def scrape(url_: str, selector_: str, page_function_="(element) => element.outerHTML", log_=True):
    if log_: print("-------------------------Scrape Log Begin--------------------------", "\n")
    # create random user agent so YouTube's algorithm gets pypassed
    ua = UserAgent()
    agent = ua.random

    # create browser, incognito context and page
    browser = await launch()
    context = await browser.createIncognitoBrowserContext()
    page = await context.newPage()
    if log_: print("Browser, Incognito Context and Page created")

    # set user agent
    await page.setUserAgent(agent)
    if log_: print("User Agent:", agent)

    # open url
    await page.goto(url_)
    if log_: print("Url opened:", url_)

    await page.waitForSelector("h1.title")
    await page.click("h1.title")

    time.sleep(5)

    await page.keyboard.press("End")

    # wait until page gets loaded
    await page.waitForSelector(selector_)
    if log_: print("Selector loaded:", selector_)

    time.sleep(3)

    await page.click(selector_)

    # get element from query selector and relating function
    request_result = await page.querySelectorEval(selector_, page_function_)
    if log_: print("Request finished")

    # close browser
    await browser.close()
    if log_: print("Browser closed", "\n")
    if log_: print("-------------------------Scrape Log End----------------------------", "\n")

    return request_result


# get YouTube Video Title

url = "https://www.youtube.com/watch?v=dyN_WtjdfpA&list=PLhTjy8cBISEoOtB5_nwykvB9wfEDscuEo"
query_selector = "h1.title"
function = "(element) => element.firstChild.innerHTML"

title = await scrape(url, query_selector, function)

print(title)

# get comments and their authors as html

url = "https://www.youtube.com/watch?v=dyN_WtjdfpA&list=PLhTjy8cBISEoOtB5_nwykvB9wfEDscuEo"
query_selector = "ytd-comments"
function = "(element) => element.outerHTML"

html = await scrape(url, query_selector, function)

# parse html and assign them

soup = BeautifulSoup(html, features="html.parser")

# get authors of comments and clear html data
authors = [item.text.strip() for item in soup.select("a[id=author-text] > span")]

# get comments and clear html data
comments = [item.text.strip().replace("\n", " ") for item in soup.select("yt-formatted-string[id=content-text]")]

comments_with_authors = list(zip(authors, comments))

for author, comment in comments_with_authors:
    print(author, "wrote:\n -" + comment)
