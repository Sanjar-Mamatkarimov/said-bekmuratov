from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    priorities = {
        'home': 1.0,
        'departments': 0.9,
        'teachers': 0.8,
        'events': 0.7,
        'rewards': 0.6,
        'gallery': 0.5,
        'reviews': 0.4,
        'contacts': 0.3,
    }

    changefreqs = {
        'home': 'daily',
        'events': 'weekly',
        'teachers': 'weekly',
    }

    def items(self):
        return ['home', 'departments', 'teachers', 'events', 'rewards', 'gallery', 'reviews', 'contacts']

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.priorities.get(item, 0.5)

    def changefreq(self, item):
        return self.changefreqs.get(item, 'weekly')
