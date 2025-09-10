### Beautiful Soup Python Cheat Sheet

Here is a quick reference guide for common Beautiful Soup commands in Python. This cheat sheet covers essential actions like setup, parsing HTML, finding elements, extracting data, and handling real-world scraping tasks.

---

### 1. Setup and Initialization

| Command                                        | Description                  | Example                                       |
| :--------------------------------------------- | :--------------------------- | :-------------------------------------------- |
| **`pip install requests beautifulsoup4 lxml`** | Install required libraries.  | Run in terminal                               |
| **`import requests`**                          | Import requests for HTTP.    | `import requests`                             |
| **`from bs4 import BeautifulSoup`**            | Import Beautiful Soup.       | `from bs4 import BeautifulSoup`               |
| **`soup = BeautifulSoup(html, "lxml")`**       | Parse HTML with lxml parser. | `soup = BeautifulSoup(response.text, "lxml")` |

**Sample Code:**

```python
import requests
from bs4 import BeautifulSoup

url = "https://example.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, "lxml")
```

---

### 2. Fetching the Page

| Command                 | Description                        | Example                                          |
| :---------------------- | :--------------------------------- | :----------------------------------------------- |
| **`requests.get(url)`** | Fetches the HTML page from a URL.  | `response = requests.get("https://example.com")` |
| **`.text`**             | Returns the response body as text. | `html = response.text`                           |
| **`.status_code`**      | Checks the HTTP status code.       | `print(response.status_code)`                    |

**Sample Code:**

```python
url = "https://example.com/articles"
response = requests.get(url)

print(response.status_code)  # 200 means OK
print(response.text[:500])   # show first 500 chars of HTML
```

---

### 3. Finding Elements

| Method                 | Description                            | Example                              |
| :--------------------- | :------------------------------------- | :----------------------------------- |
| **`.find(tag)`**       | Finds the first matching element.      | `soup.find("h1")`                    |
| **`.find_all(tag)`**   | Finds all matching elements.           | `soup.find_all("p")`                 |
| **`attrs`**            | Match by attributes (class, id, etc.). | `soup.find("div", class_="content")` |
| **`.select(css)`**     | Finds all with CSS selectors.          | `soup.select("div.content p")`       |
| **`.select_one(css)`** | Finds the first with CSS selector.     | `soup.select_one("h1.title")`        |

**Sample Code:**

```python
title = soup.find("h1")
paragraphs = soup.find_all("p")
content_div = soup.find("div", class_="content")

print(title.text)
print([p.text for p in paragraphs])
```

---

### 4. Extracting Data

| Command                     | Description                      | Example                        |
| :-------------------------- | :------------------------------- | :----------------------------- |
| **`.text`**                 | Gets the inner text of a tag.    | `element.text`                 |
| **`.get("attr")`**          | Gets an attribute value.         | `link.get("href")`             |
| **`tag["attr"]`**           | Alternate way to get attribute.  | `img["src"]`                   |
| **`.get_text(strip=True)`** | Cleans text, removes whitespace. | `element.get_text(strip=True)` |

**Sample Code:**

```python
link = soup.find("a")
print(link.text)
print(link.get("href"))

image = soup.find("img")
print(image["src"])
```

---

### 5. Traversing the DOM

| Command                        | Description                     | Example                         |
| :----------------------------- | :------------------------------ | :------------------------------ |
| **`.parent`**                  | Gets the parent element.        | `title.parent`                  |
| **`.find_next_sibling()`**     | Next element at same level.     | `h2.find_next_sibling("p")`     |
| **`.find_previous_sibling()`** | Previous element at same level. | `p.find_previous_sibling("h2")` |
| **`.find_next(tag)`**          | Next occurrence of tag.         | `div.find_next("span")`         |

**Sample Code:**

```python
h2 = soup.find("h2")
print(h2.find_next_sibling("p").text)
```

---

### 6. Common Scraping Patterns

| Pattern         | Description                         | Example                                              |                  |
| :-------------- | :---------------------------------- | :--------------------------------------------------- | ---------------- |
| **All links**   | Extract all `<a href>` values.      | `[a["href"] for a in soup.find_all("a", href=True)]` |                  |
| **All images**  | Extract all `<img src>`.            | `[img["src"] for img in soup.find_all("img")]`       |                  |
| **All text**    | Extract visible text of whole page. | `soup.get_text("\n")`                                |                  |
| **Nested text** | Get clean text inside a div.        | \`div.get\_text("                                    | ", strip=True)\` |

**Sample Code:**

```python
links = [a["href"] for a in soup.find_all("a", href=True)]
print(links)

images = [img["src"] for img in soup.find_all("img")]
print(images)
```

---

### 7. Handling Tables

| Command               | Description         | Example                                                  |
| :-------------------- | :------------------ | :------------------------------------------------------- |
| **`.find("table")`**  | Finds a table.      | `table = soup.find("table")`                             |
| **`.find_all("tr")`** | Gets all rows.      | `rows = table.find_all("tr")`                            |
| **Loop rows/cols**    | Extract table data. | `[td.get_text(strip=True) for td in row.find_all("td")]` |

**Sample Code:**

```python
table = soup.find("table")
rows = table.find_all("tr")

for row in rows:
    cols = [td.get_text(strip=True) for td in row.find_all("td")]
    print(cols)
```

---

### 8. Pagination Example

**Sample Code:**

```python
url = "https://example.com/page/1"

while True:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")

    items = [h2.text for h2 in soup.find_all("h2")]
    print(items)

    next_page = soup.select_one("a.next")
    if not next_page:
        break
    url = next_page["href"]
```

---

### 9. Best Practices

| Practice                    | Description                             |
| :-------------------------- | :-------------------------------------- |
| **Use headers**             | Mimic a real browser with `User-Agent`. |
| **Respect robots.txt**      | Check site’s scraping rules.            |
| **Add delays**              | Prevent blocking with `time.sleep()`.   |
| **Handle errors**           | Use `try/except` for robustness.        |
| **Use Selenium/Playwright** | For JavaScript-heavy sites.             |

**Sample Code:**

```python
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get("https://example.com", headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "lxml")
```

---

### 10. Exporting Data

| Library    | Method                     | Example                              |
| :--------- | :------------------------- | :----------------------------------- |
| **pandas** | Save data as CSV.          | `df.to_csv("data.csv", index=False)` |
| **json**   | Save scraped data to JSON. | `json.dump(data, f)`                 |

**Sample Code:**

```python
import pandas as pd

data = [{"title": "Item 1", "price": "$10"},
        {"title": "Item 2", "price": "$15"}]

df = pd.DataFrame(data)
df.to_csv("output.csv", index=False)
```