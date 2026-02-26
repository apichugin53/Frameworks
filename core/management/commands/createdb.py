from django.conf import settings
from django.db import connection
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create empty database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            "-f",
            action="store_true",
            help="Force overwrite of existing database",
        )

    def handle(self, *args, **options):
        db_name = settings.DATABASES[connection.alias]['NAME']
        connection.settings_dict['NAME'] = None
        with connection.cursor() as cursor:
            sql = ""
            if options["force"]:
                sql = fr"""
USE master
IF EXISTS(select * from sys.databases where name='{db_name}')
DROP DATABASE {db_name}
"""
            sql += f"CREATE DATABASE {db_name}"
            cursor.execute(sql)
            print(f"Created database {db_name}")
