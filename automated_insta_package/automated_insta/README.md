# Automated-Insta

## Save your time to develop Instagram bots

This ***Python*** package facilitates Instagram bot development
by scraping data and automating actions using ***Selenium***.

To use the features, you need a small setup:

```python
from automated_insta.webdriver.webdriver import EdgeWebDriver

webdriver = EdgeWebDriver  # It makes an instance of EdgeWebdriver
webdriver.initialize()  # It opens the webdriver
```

This code opens an Edge webdriver which inherits Selenium Edge Webdriver and 
is extended to have more features (mostly Instagram-related).

---

**Example of usage:**

```python
from automated_insta.webdriver.webdriver import EdgeWebDriver
from automated_insta.auth.login import login_by_username

webdriver = EdgeWebDriver.initialize()
webdriver.maximize_window()

webdriver.get('https://www.instagram.com/')

cookies = login_by_username(webdriver, 'username', 'password')
```