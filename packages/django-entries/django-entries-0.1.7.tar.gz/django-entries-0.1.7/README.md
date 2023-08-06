# Entries

## Overview

Entries is a Django app that has basic create-read-update-delete functionality for a model that `Entry` consisting of the following fields: `title`, `excerpt`,`content` and `author`.

The [templates/base.html](./entries/templates/base.html) provides a light set of tools:

1. `starter.css` [stylesheet](./entries/static/css/starter.css) for some defaults
2. `pylon` 0.1.1 for `<hstack>` and `<vstack>` layouts
3. `htmx` 1.6.1 for html-over-the-wire functionality
4. `hyperscript` 0.9 for client-side reactivity
5. `simplemde` a simple text editor that accepts markdown

## Quickstart

```python
# in project_folder/settings.py
INSTALLED_APPS = [
    ...,
    'crispy_forms',  # crispy_forms at least > v1.13
    'entries' # new
]

# in project_folder/urls.py
from django.urls import path, include # new
urlpatterns = [
    ...,
    path('entry/', include('entries.urls')) # new
]
```

Add to database:

```zsh
.venv> python manage.py migrate # enter virtual environment
```
