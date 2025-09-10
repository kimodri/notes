Here is a Selenium cheat sheet tailored specifically for web scraping, focusing on efficient and robust methods to extract data from websites.

-----

### 1\. Finding and Extracting Data

| Action | Description | Example |
| :--- | :--- | :--- |
| **Find Single Element** | Finds the first element that matches the locator. | `title = driver.find_element(By.CSS_SELECTOR, 'h1.post-title')` |
| **Find Multiple Elements**| Finds all elements that match the locator, returns a list. | `all_links = driver.find_elements(By.TAG_NAME, 'a')` |
| **Extract Text** | Gets the visible text of an element. | `recipe_name = title.text` |
| **Extract Attribute** | Gets the value of a specific HTML attribute. | `link_url = element.get_attribute('href')` |

-----

### 2\. Common XPath Patterns for Scraping

XPath is one of the most powerful tools for web scraping. These patterns help you target data precisely.

| Pattern | Use Case | Example |
| :--- | :--- | :--- |
| **`//tag[@attr='value']`** | Find a specific element by an attribute. | `//div[@class='recipe-card']` |
| **`//tag[text()='text']`**| Find an element by its exact text content. | `//h2[text()='Ingredients']` |
| **`//tag[contains(text(), 'text')]`**| Find an element with partial text. | `//span[contains(text(), 'Price:')]` |
| **`//parent/child`** | Find a direct child of a parent element. | `//ul[@id='main-menu']/li` |
| **`//grandparent//descendant`**| Find a descendant anywhere within a parent. | `//div[@class='main']//p` |
| **`//tag[last()]`**| Find the last element of a specific type. | `//li[last()]` |

-----

### 3\. Handling Dynamic Content

These techniques are critical for websites that load content asynchronously (e.g., with AJAX or JavaScript).

| Action | Description | Example |
| :--- | :--- | :--- |
| **Explicit Wait** | The **most reliable** way to wait for elements to become available. It avoids static `time.sleep()`. | `WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'content-area')))` |
| **Scroll to Load** | Use JavaScript to scroll down and trigger the loading of new content. | `driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")` |
| **Handling `StaleElementReferenceException`** | Re-find the element inside a loop or immediately before using it, especially after page changes. | `element = driver.find_element(By.XPATH, '...')` then `element.click()` |

-----

### 4\. Code Structure for Scraping

A standard scraping script should follow this pattern for stability and resource management.

```python
# Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 1. Setup the driver
driver = webdriver.Chrome()
driver.maximize_window()

try:
    # 2. Navigate to the page
    driver.get("https://example.com/products")
    
    # 3. Wait for content to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-list")))
    
    # 4. Find elements and extract data
    product_elements = driver.find_elements(By.CLASS_NAME, 'product-item')
    for product in product_elements:
        title = product.find_element(By.CSS_SELECTOR, 'h3').text
        price = product.find_element(By.CLASS_NAME, 'price').text
        print(f"Product: {title}, Price: {price}")
        
    # 5. Handle pagination (optional)
    # This might involve finding and clicking a "next page" button in a loop
    
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # 6. Close the browser
    driver.quit()
```
