from .test_api_setup import TestSetUp


class TestApi(TestSetUp):
    def test_api_list_get(self):
        response = self.client.get(self.book_list_url)
        response_data = response.json()[-1]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.raw_data[0]["title"], response_data["title"])

    def test_api_list_get_with_filter(self):
        response = self.client.get(self.book_list_url, {"title": "First"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()[0]["title"], self.raw_data[0]["title"])
        self.assertEqual(response.json()[0]["lang"], self.raw_data[0]["lang"])

    def test_api_list_get_date_range(self):
        response = self.client.get(
            self.book_list_url,
            {
                "publication_date_from": "2001-01-01",
                "publication_date_to": "2002-01-01",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)

    def test_api_list_get_invalid_data(self):
        response = self.client.get(
            self.book_list_url, {"publication_date_from": "2012-"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()["publication_date_from"], ["Enter a valid date."]
        )
