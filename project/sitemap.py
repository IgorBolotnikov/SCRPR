from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return [
            "scrpr:index",
            "scrpr:news",
            "scrpr:about",
            "scrpr:rate",
            "scrpr:games",
            "scrpr:jobs",
            "authentication:login",
            "authentication:register",
        ]

    def location(self, item):
        return reverse(item)
