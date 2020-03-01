''' test_chromedriver chromedriver_autoinstaller '''
from selenium import webdriver
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
from selenium.webdriver.chrome.options import Options


def test_chromedriver():
    ''' test_chromedriver '''
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get("http://www.python.org")

    assert 'Python' in driver.title