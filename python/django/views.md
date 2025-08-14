# Django Notes (Full Guide)

## Project Structure & Routing

* **Project and Apps**: An overview of Django's project and application structure.
* **Creating a Project and App**: The steps for using `django-admin startproject` and `python manage.py startapp`.
* **URL Dispatcher**: How `urls.py` files map URLs to specific view functions.

---

## Templating & Rendering

* **Rendering HTML Templates**: Using the `render()` function to serve HTML files.
* **Dynamic Routes**: Creating URL paths that can capture and use variable data (e.g., `hello/<str:name>`).
* **Jinja Templates**: Using variables and a **context** dictionary within HTML files.
* **Advanced Templating**: Implementing conditional logic (`if/else`) and loops (`for`) within templates.

---

## Styling & Layouts

* **Static Files**: How to manage and link CSS and JavaScript files in a Django project.
* **Layouts and Inheritance**: Using a base `layout.html` file to create a consistent structure across multiple pages with **template inheritance**.

---

## Navigation & Forms

* **URL Namespacing**: Using the `{% url %}` tag and **app names** to prevent conflicts between apps with similar URL names.
* **Forms (CSRF)**: A quick guide to creating forms and using the `{% csrf_token %}` to protect against cross-site request forgery.
* **Django Forms Library**: An introduction to Django's built-in forms library for simplifying form creation and client-side validation.
* **Server-Side Validation**: The process of validating form data on the server to handle security and logic.

---

## Sessions & Database

* **Session Management**: An overview of how to use Django's session dictionary to store user-specific data.
* **Database Migration**: How to resolve the `No such table: django_session` error using `python manage.py migrate`.
## Project Structure & Routing

- `urls.py` is like a table of contents — it maps URL paths to views.
- One **project** contains many **applications**.
- When you run `django-admin startproject <project_name>`, it will create a Django project.

### Next step: Create a Django app
```bash
python manage.py startapp <app_name>
```
- Register the app in settings.py under INSTALLED_APPS.
- Then go to views.py of the app and create a function:

```python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello")
```
- Tell Django when that function should be called when a specific URL is submitted. You need to register a URL associated with that function.
- Create a urls.py inside the application:
```python
from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index")
]
```
- Then go back to the project folder (e.g., lecture3) and include the app’s URLs in the project-level urls.py, because that urls.py holds all the urls.py files of each app
```python
# lecture3/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello/', include("hello.urls"))
]
```
---
## Templating in Functions
You can create different functions like hello/kim, hello/audrey, etc. But that's inefficient. Instead, use a dynamic route:
```python
def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}")
```
In ``hello/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path("<str:name>", views.greet, name="greet")
]
```
---
## Rendering HTML Templates
Use the `render()` function:
```python
def index(request):
    return render(request, "hello/index.html")
```
To use this:
- Create a folder called `templates` inside your application.
- Inside `templates`, create a folder named after your app (e.g., `hello/`).
- Place your HTML files there: `hello/templates/hello/index.html`.

### Jinja Templates (Using Variables)
`hello/tempates/hello/greet.html`
```html
<body>
    <h1>Hello, {{ name }}</h1>
</body>
```
In `views.py`
```python
def greet(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()  # This is called the context
    })
```
---
## Advanced Templating (Conditional, Loops)
### Example: Check if today is New Year
```python
from django.shortcuts import render
import datetime

def index(request):
    now = datetime.datetime.now()
    return render(request, "newyear/index.html", {
        "newyear": now.month == 1 and now.day == 1
    })
```
In the HTML:
```html
<body>
    {% if newyear %}
        <h1>YES</h1>
    {% else %}
        <h1>NO</h1>
    {% endif %}
</body>
```
---
## Styling with Static Files
- Django supports static files like CSS/JS
- Place them in `static/<app_name>/`

In your HTML:
```html
{% load static %}
<link href="{% static 'app_name/filename.css' %}" rel="stylesheet">
```
---
## Layouts and Inheritance
### `layout.html`
Create a `layout.html` file to define the common structure:
```html
<!DOCTYPE html>
<html>
    <head>
        <title>Task</title>
    </head>
    <body>
        {% block body %}
        {% endblock %}
    </body>
</html>
```
Other templates can extend this:
```html
{% extends "tasks/layout.html" %}

{% block body %}
    <ul>
        {% for task in tasks %}
            <li>{{ task }}</li>
        {% endfor %}
    </ul>
{% endblock %}
```
---
## Navigation
You can normally link like:
```html
<a href="/something/something">Something</a>
```
But in Django you often use:
```html
<a href="{% url 'index' %}">Index Page</a>
```
### Problem
What if multiple apps use the same URL name like `index`?

To fix this, set an `app_name` in your app's `urls.py`:

```python
app_name = "tasks"

urlpatterns = [
    path("", views.index, name="index"),
    path("add", views.add, name="add")
]
```
Then in your template:
```html
<a href="{% url 'tasks:index' %}">Index Page</a>
```
---
## Forms
### CSRF Verification Failed
Django requires CSRF protection in forms:
Use:
```html
<form action="{% url 'tasks:add' %}" method="post">
    {% csrf_token %}
    <input type="text" name="task">
    <input type="submit">
</form>
<a href="{% url 'index' %}">View Tasks</a>
```
---
## Django Forms
### Using Django's Form Library
In `views.py`:
```python
from django import forms

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=10)
```
Create a form view:
```python
def add(request):
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })
```
In the HTML:
```html
<form action="{% url 'tasks:add' %}" method="post">
    {% csrf_token %}
    {{ form }}
    <input type="submit">
</form>
<a href="{% url 'index' %}">View Tasks</a>
```
This allows client-side validation automatically.

### But in Django…
If you want Django to reject disallowed methods automatically (like Flask does), you use decorators:
```python
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def my_view(request):
    ...
```

---
## Server-Side Validation
In case client-side validation is bypassed (e.g., old page version), do this:
```python
def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)  # Fill form with submitted data
        if form.is_valid():
            task = form.cleaned_data["task"]
            tasks.append(task)
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })
```
---
## Session
Session is like a bid dictionary for storing user-specific data (e.g., a to-do list)

Initialize a list for tasks:
```python
def index(request):
    if "tasks" not in request.session:
        request.session["tasks"] = []
    return render(request, "tasks/index.html", {
        "tasks": request.session["tasks"]
    })
```
Add a session in `add()`:
```python
if form.is_valid():
    task = form.cleaned_data['task']
    request.session["tasks"].append(task)  # Won’t work alone!
```
| Code                                            | Works? | Why                                        |
| ----------------------------------------------- | ------ | ------------------------------------------ |
| `request.session["tasks"].append(task)`         | ❌      | No auto-detection of in-place changes      |
| `request.session["tasks"] += [task]`            | ✅      | Reassigns value, Django detects the change |
| `.append()` + `request.session.modified = True` | ✅      | Manual trigger to mark session as changed  |

Fix:
```python
request.session["tasks"].append(task)
request.session.modified = True
```
---
## Error: No such table: `django_session`
- You may get this if you're using sessions but haven’t initialized the session table.
Fix:
```bash
python manage.py migrate
```