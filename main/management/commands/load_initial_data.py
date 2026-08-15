from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

from main.models import Department, Event, GalleryImage, Review, Reward, SiteSettings, Teacher


class Command(BaseCommand):
    help = "Загружает данные из fixtures/initial_data.json, если база ещё пуста (идемпотентно)."

    CONTENT_MODELS = [SiteSettings, Department, Event, Reward, Teacher, Review, GalleryImage]

    def handle(self, *args, **options):
        existing_tables = connection.introspection.table_names()
        if 'main_sitesettings' not in existing_tables:
            self.stdout.write('Таблицы ещё не созданы. Сначала выполните migrate.')
            return

        if any(model.objects.exists() for model in self.CONTENT_MODELS):
            self.stdout.write('База уже содержит данные — импорт пропущен.')
            return

        self.stdout.write('База пуста. Загружаю данные из fixtures/initial_data.json...')
        call_command('loaddata', 'initial_data.json', verbosity=1)
        self.stdout.write(self.style.SUCCESS('Данные успешно загружены.'))
