# Entries

Entries is a Django app that has basic CRUD functionality with some defaults.

## What is included?

The `templates/base.html` includes:

1. `starter.css` [stylesheet](entries/static/css/starter.css) for some defaults
2. `pylon` 0.1.1 for `<hstack>` and `<vstack>` layouts
3. `htmx` 1.6.1 for html-over-the-wire functionality
4. `hyperscript` 0.9 for client-side reactivity
5. `simplemde` a simple text editor that accepts markdown

## Quick start

### 1: Add to apps

Add "entries" to your INSTALLED_APPS setting like this:

```python
INSTALLED_APPS = [
...
'crispy_forms'
'entries',
]
```

### 2: Add to urls

Include the entries URLconf in your project urls.py like this:

```python
urlpatterns = [
...
path('', include('entries.urls')),
]
```

### 3: Add to db

Run `python manage.py migrate` to create the entries models.
