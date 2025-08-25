# conftest.py (repo root)

import os
import django

# Ensure Django knows which settings to use
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")

# Set up Django before pytest starts importing test modules
django.setup()
