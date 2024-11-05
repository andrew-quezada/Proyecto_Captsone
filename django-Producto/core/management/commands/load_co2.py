import csv
from datetime import date
from itertools import islice
import pathlib
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import Productos

class Command(BaseCommand):
    help = 'Load data from Productos file'

    def handle(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'data' / 'Productos_mm_mlo.csv'

        with open(datafile, newline='') as csvfile:
            reader = csv.DictReader(islice(csvfile, 51, None))
            for row in reader:
                dt = date(
                    year=int(row['year']),
                    month=int(row['month']),
                    day=1
                )
                Productos.objects.get_or_create(date=dt, average=row['average'])
                

        