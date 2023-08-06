# Entries

Entries is a Django app that has basic CRUD functionality with some defaults.

Detailed documentation is in the "docs" directory.

## Quick start

1. Add "entries" to your INSTALLED_APPS setting like this::

   INSTALLED_APPS = [
   ...
   'entries',
   ]

2. Include the entries URLconf in your project urls.py like this::

   path('entries/', include('entries.urls')),

3. Run `python manage.py migrate` to create the entries models.
