

import csv
import io
from selenium import webdriver
from selenium.common import exceptions
import sys
import time

def scrape(url):
    """
    Extracts the comments from the Youtube video given by the URL.
    Args:
        url (str): The URL to the Youtube video
    Raises:
        selenium.common.exceptions.NoSuchElementException:
        When certain elements to look for cannot be found
    """

    # Note: Download and replace argument with path to the driver executable.
    # Simply download the executable and move it into the webdrivers folder.
    ####driver = webdriver.Chrome('./webdrivers/chromedriver')
    # For windows:
    #https://pythonpedia.com/en/knowledge-base/47148872/-webdrivers--executable-may-have-wrong-permissions--please-see-https---sites-google-com-a-chromium-org-chromedriver-home
    #driver = webdriver.Chrome(executable_path=r'C:\Users\Daglemino\Downloads\chromedriver_win32\chromedriver.exe')
    #driver = webdriver.Chrome(executable_path=r'./webdrivers/chromedriver/chromedriver.exe')
    driver = webdriver.Chrome(executable_path=r'C:\chromedriver.exe')
    
    # Navigates to the URL, maximizes the current window, and
    # then suspends execution for (at least) 5 seconds (this
    # gives time for the page to load).
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)

    try:
        # Extract the elements storing the video title and
        # comment section.
        title = driver.find_element_by_xpath('//*[@id="container"]/h1/yt-formatted-string').text
        comment_section = driver.find_element_by_xpath('//*[@id="comments"]')
    except exceptions.NoSuchElementException:
        # Note: Youtube may have changed their HTML layouts for
        # videos, so raise an error for sanity sake in case the
        # elements provided cannot be found anymore.
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    # Scroll into view the comment section, then allow some time
    # for everything to be loaded as necessary.
    driver.execute_script("arguments[0].scrollIntoView();", comment_section)
    time.sleep(7)

    # Scroll all the way down to the bottom in order to get all the
    # elements loaded (since Youtube dynamically loads them).
    last_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        # Scroll down 'til "next load".
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        # Wait to load everything thus far.
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # One last scroll just in case.
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

    try:
        # Extract the elements storing the usernames and comments.
        username_elems = driver.find_elements_by_xpath('//*[@id="author-text"]')
        comment_elems = driver.find_elements_by_xpath('//*[@id="content-text"]')
    except exceptions.NoSuchElementException:
        error = "Error: Double check selector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    print("> VIDEO TITLE: " + title + "\n")

    with io.open('results.csv', 'w', newline='', encoding="utf-16") as file:
        writer = csv.writer(file, delimiter =",", quoting=csv.QUOTE_ALL)
        writer.writerow(["Username", "Comment"])
        for username, comment in zip(username_elems, comment_elems):
            writer.writerow([username.text, comment.text])

    driver.close()

urls = [
    'https://www.youtube.com/watch?v=dyN_WtjdfpA&list=PLhTjy8cBISEoOtB5_nwykvB9wfEDscuEo'
]
for url in urls:
    scrape(url)