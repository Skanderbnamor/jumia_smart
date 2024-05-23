#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from  jumia.scraper import *


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jumia_smart.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    def runserver():
        """Run the Django development server."""


        # Exécute le scraping des smartphones
        get_all_smartphone()

        os.system("python manage.py runserver")



if __name__ == '__main__':
    main()
