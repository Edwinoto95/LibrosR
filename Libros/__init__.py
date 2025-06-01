# Libros/__init__.py
import django
from django import VERSION

# Hack temporal para MariaDB 10.4
if VERSION >= (5, 0):
    from django.db.backends.mysql.base import DatabaseWrapper
    original_check = DatabaseWrapper.check_database_version_supported
    
    def bypass_version_check(self):
        pass
    
    DatabaseWrapper.check_database_version_supported = bypass_version_check