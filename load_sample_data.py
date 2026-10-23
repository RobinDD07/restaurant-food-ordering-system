"""
Convenience script to populate sample data into the MySQL database.
Usage:
    python load_sample_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_ordering_system.settings')
django.setup()

from django.core.management import call_command

if __name__ == '__main__':
    print("Populating database 'restaurant_food_ordering' with sample records...")
    call_command('load_sample_data')
    print("Done! You can now start the server and view the data.")
