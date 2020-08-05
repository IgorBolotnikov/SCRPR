from django.test import Client


class TestSitemap:
    def test_get_response(self):
        response = Client().get("/sitemap.xml")
        assert response.status_code == 200, "Should be accessible by anyone"
        assert response.content is not None, "Should return sitemap data"
