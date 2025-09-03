### Selenium Python Cheat Sheet 🐍

Here is a quick reference guide for common Selenium commands in Python. This cheat sheet covers essential actions like setup, finding elements, interacting with them, and handling browser states.

-----

### 1\. Basic Setup and Browser Management

| Command | Description | Example |
| :--- | :--- | :--- |
| **`driver = webdriver.Chrome()`** | Initializes a new Chrome session. | `driver = webdriver.Chrome()` |
| **`driver.maximize_window()`** | Maximizes the browser window to full screen. | `driver.maximize_window()` |
| **`driver.get(url)`** | Navigates to a specific URL. | `driver.get("https://example.com")` |
| **`driver.close()`** | Closes the currently active browser tab. | `driver.close()` |
| **`driver.quit()`** | Closes all browser windows and ends the WebDriver session. **(Recommended)** | `driver.quit()` |

-----

### 2\. Finding Elements (Locators)

These commands are used with `driver.find_element()` to locate a single element or `driver.find_elements()` to find all matching elements.

| Locator Strategy | Method | Example |
| :--- | :--- | :--- |
| **ID** | `By.ID` | `driver.find_element(By.ID, "user-name")` |
| **Name** | `By.NAME` | `driver.find_element(By.NAME, "q")` |
| **Class Name** | `By.CLASS_NAME` | `driver.find_element(By.CLASS_NAME, "btn-submit")` |
| **Tag Name** | `By.TAG_NAME` | `driver.find_elements(By.TAG_NAME, "a")` |
| **Link Text** | `By.LINK_TEXT` | `driver.find_element(By.LINK_TEXT, "Log In")` |
| **Partial Link Text**| `By.PARTIAL_LINK_TEXT`| `driver.find_element(By.PARTIAL_LINK_TEXT, "Log")` |
| **CSS Selector** | `By.CSS_SELECTOR` | `driver.find_element(By.CSS_SELECTOR, "a.btn-main")` |
| **XPath** | `By.XPATH` | `driver.find_element(By.XPATH, "//button[@id='submit']")` |

-----

### 3\. Common Element Interactions

Once you've located an element, you can perform an action on it.

| Action | Description | Example |
| :--- | :--- | :--- |
| **`.click()`** | Clicks on an element. | `element.click()` |
| **`.send_keys(text)`** | Types text into an input field. | `input_field.send_keys("Hello World")` |
| **`.clear()`** | Clears the text from an input field. | `input_field.clear()` |
| **`.text`** | Gets the visible text of an element. | `print(element.text)` |
| **`.get_attribute(name)`**| Gets the value of an element's attribute. | `link.get_attribute("href")` |

-----

### 4\. Waiting and Synchronization

Using `time.sleep()` is not recommended as it is an unconditional wait. **Explicit Waits** are a more robust solution that wait only until a condition is met.

| Method | Description | Example |
| :--- | :--- | :--- |
| **Explicit Wait** | Waits until a specific condition is met, for up to a defined time limit. | See code example below. |
| **`time.sleep(s)`** | Pauses the script for a fixed number of seconds. **(Not Recommended)** | `time.sleep(3)` |

**Example of an Explicit Wait:**

```python
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

wait = WebDriverWait(driver, 10) # wait up to 10 seconds
element = wait.until(EC.element_to_be_clickable((By.ID, "my-button")))
element.click()
```

-----

### 5\. Executing JavaScript and Scrolling

| Command | Description | Example |
| :--- | :--- | :--- |
| **`execute_script()`** | Executes a JavaScript command in the browser. | `driver.execute_script("alert('Hi!');")` |
| **Scroll By** | Scrolls the window by a specific amount (horizontal, vertical). | `driver.execute_script("window.scrollBy(0, 500);")` |
| **Scroll to Bottom**| Scrolls the window to the bottom of the page. | `driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")` |