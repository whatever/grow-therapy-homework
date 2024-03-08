import random
import unittest
import unittest.mock as mock

from datetime import datetime
from wikipedia_counter.routes import flask_app, month_start_end
from wikipedia_counter.routes import fetch_monthly_count


class TestRoutes(unittest.TestCase):
    def test_monthly_counts(self):
        """Trest whether api routes exist"""

        with flask_app.test_client() as client:

            r = client.get("/")
            self.assertIsNone(r.json)

            r = client.get("/api/1/count")
            self.assertEqual(r.status_code, 400)
            self.assertEqual(r.json["error"], "missing month")

            r = client.get(
                "/api/1/count",
                query_string={"month": "2021-01"},
            )
            self.assertEqual(r.status_code, 400)
            self.assertEqual(r.json["error"], "missing article name")

            r = client.get(
                "/api/1/count",
                query_string={"month": "2021-A1"},
            )
            self.assertEqual(r.status_code, 400)
            self.assertEqual(r.json["error"], "invalid month")

            r = client.get(
                "/api/1/count",
                query_string={"month": "2015-10", "article": "Gödel's_incompleteness_theorems"},
            )

    def test_month_start_end(self):
        """Test whether we correctly determine that start/end of a given year/month"""

        cases = [
            (2020, 1, datetime(2020, 1, 31)),
            (2020, 2, datetime(2020, 2, 29)),
            (2021, 2, datetime(2021, 2, 28)),
            (2021, 6, datetime(2021, 6, 30)),
        ]

        for year, month, expected_end in cases:
            with self.subTest(year=year, month=month):
                start, end = month_start_end(year, month)
                self.assertEqual(start, datetime(year, month, 1))
                self.assertEqual(end, expected_end)

    def test_live_albert_einstein(self):

        resp = fetch_monthly_count(
            article="Albert Einstein",
            month=datetime(2015, 10, 1),
            project="en.wikipedia",
            agent="all-agents",
            access="all-access",
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()["items"][0]["views"], 633964)

    def test_live_fetch_monthly_count(self):
        """Test whether we correctly fetch the wikipedia example"""

        pr = "en.wikipedia"
        ag = "all-agents"
        ac = "all-access"

        cases = [
            ("Albert_Einstein", datetime(2015, 10, 1)),
            # Seems they do the MediaWiki formatting for us:
            ("Albert Einstein", datetime(2015, 10, 1)),
            ("Python (programming language)", datetime(2021, 2, 1)),
        ]

        for case in cases:
            article, month = case
            with self.subTest(article=article, month=month):
                resp = fetch_monthly_count(
                    article=article,
                    month=month,
                    project=pr,
                    agent=ag,
                    access=ac,
                )
                self.assertEqual(resp.status_code, 200)
                self.assertIn("items", resp.json())
                self.assertEqual(len(resp.json()["items"]), 1)
                self.assertIn("views", resp.json()["items"][0])

    def test_happy_endpoint(self):
        """Test whether the /api/1/count endpoint works with mocked out wikipedia responses."""
        with flask_app.test_client() as client:
            for _ in range(100):
                count = random.randint(0, 1000000)
                with mock.patch("wikipedia_counter.routes.requests.get") as m:

                    m.return_value = mock.MagicMock(
                        status_code=200,
                        json=lambda: {"items": [{"views": count}]},
                    )

                    r = client.get(
                        "/api/1/count",
                        # query_string={"month": "2021-01", "article": "Gödel's_incompleteness_theorems"},
                        query_string={"month": "2021-01", "article": "Python"},
                    )

                    self.assertEqual(r.status_code, 200)
                    self.assertEqual(r.json, {"status": "ok", "count": count})

    def test_failed_responses(self):
        """Test whether our endpoint handles wikipedia failures alright"""

        with flask_app.test_client() as client:

            params = {"month": "2021-01", "article": "Gödel's_incompleteness_theorems"}

            responses = [
                None,
                "adasd",
                {"detail": "some error"},
                {"items": 10},
                {"items": []},
                {"items": [{}]},
                {"items": [{"views": "asdf"}]},
            ]

            for resp in responses:
                with mock.patch("wikipedia_counter.routes.requests.get") as m:
                    m.return_value = mock.MagicMock(
                        status_code=200,
                        json=lambda: resp,
                    )
                    r = client.get("/api/1/count", query_string=params)
                    self.assertEqual(r.status_code, 400)
                    self.assertEqual(r.json["status"], "error")
