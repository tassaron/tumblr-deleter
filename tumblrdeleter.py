#!/usr/bin/env python3
"""
Brianna Rainey (tassaron)
Super messy code I threw together on March 31, 2018 to wipe all the posts from
a Tumblr account without using the Tumblr API. Not something you should do,
technically, but it does work quickly. This was my first time using Selenium.

It doesn't log in to Tumblr: it opens a Firefox window for you to log in
manually. After logging in, the program will begin deleting posts automatically
after some time. If an errors occurs, it will return to the login screen
from which you can cleanly restart it by logging in once more. :)
"""
import selenium.webdriver
import selenium.common.exceptions as exceptions
from time import sleep

EDIT_PAGE = 'http://www.tumblr.com/mega-editor'


def acceptAlert(browser):
    try:
        alert = browser.switch_to_alert()
        print(alert.text)
        alert.accept()
        return True
    except (
            exceptions.UnexpectedAlertPresentException,
            exceptions.NoAlertPresentException
            ):
        return False


def deletePosts(browser):
    element = browser.find_element_by_id("delete_posts")
    while True:
        element.click()
        if acceptAlert(browser):
            break


def selectPosts(browser):
    for element in browser.find_elements_by_xpath(
            "/html/body/div[4]/a[contains(@id, 'post')]")[:100]:
        element.click()


def notLoggedIn(browser):
    if '/login' in browser.current_url:
        return True
    else:
        return False


def main():
    while True:
        # open firefox and wait until user is logged in
        browser = selenium.webdriver.Firefox()
        browser.set_page_load_timeout(60)
        browser.get('https://www.tumblr.com/login')
        while notLoggedIn(browser):
            sleep(60)
        print('starting!')
        browser.get(EDIT_PAGE)
        sleep(5)

        # delete posts forever
        while True:
            try:
                selectPosts(browser)
                sleep(1)
                deletePosts(browser)
                sleep(5)

            except (
                    exceptions.TimeoutException,
                    exceptions.ElementNotInteractableException
                   ) as e:
                # if something super bad happens then return to login
                print('bad thing happened! %s' % str(e))
                browser.close()
                break

            except Exception as e:
                # most other errors should be unimportant, so whatever
                print('%s: %s' % (
                        str(e.__class__.__name__),
                        str(e)
                    )
                )


if __name__ == '__main__':
    main()
