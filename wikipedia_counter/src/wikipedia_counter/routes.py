import logging
import re
import requests

from datetime import datetime, timedelta
from flask import Flask, request

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


MONTH_REGEX = re.compile(r"^\d{4}-\d{2}$")


flask_app = Flask(__name__)


HOST = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/"


HEADERS = {
    "User-Agent": "WikiedpiaCounterBot/1.0 (https://github.com/whatever/; holler@worldshadowgovernment.com)",
}


def month_start_end(year, month):
    """Return the first day and last day of the month"""

    start = datetime(year, month, 1)
    next_month = datetime(year, month, 28) + timedelta(days=4)
    next_month = next_month.replace(day=1)
    end = next_month - timedelta(days=1)
    return start, end


def fetch_monthly_count(article, month, project, agent, access):
    """Return response from wikipedia servers"""

    start, end = month_start_end(month.year, month.month)
    start = start.strftime("%Y%m%d00")
    end = end.strftime("%Y%m%d00")
    target = f"{HOST}{access}/{agent}/{article}/monthly/{start}/{end}"
    logger.info("Requesting from url: %s", target)
    return requests.get(target, headers=HEADERS)


@flask_app.route("/api/1/count")
def count():
    """Return the count for a given wikipedia article and month"""

    logger.info("Requsting count from url: %s", request.url)

    if "month" not in request.args:
        logger.warning("Missing month for url: %s", request.url)
        return {"status": "error", "error": "missing month"}, 400

    if not MONTH_REGEX.match(request.args["month"]):
        logger.warning("Improperly structured  month for url: %s", request.url)
        return {"status": "error", "error": "invalid month"}, 400

    if "article" not in request.args:
        logger.warning("Missing article for url: %s", request.url)
        return {"status": "error", "error": "missing article name"}, 400

    y, m = map(int, request.args["month"].split("-", 1))

    try:
        month = datetime(y, m, 1)
    except ValueError:
        logger.warning("Invalid month for url: %s", request.url)
        return {"status": "error", "error": "invalid month"}, 400

    article = request.args["article"]

    project = request.args.get("project", "en.wikipedia")

    agent = request.args.get("agent", "all-agents")

    access = request.args.get("access", "all-access")

    resp = fetch_monthly_count(
        article=article,
        month=month,
        project=project,
        agent=agent,
        access=access,
    )

    if resp.status_code != 200 and "detail" in resp.json():
        logger.warning(
            "Error fetching count (detail: %s) for url: %s",
            resp.json()["detail"],
            request.url,
        )
        return {
            "status": "error",
            "error": "failed to fetch count",
        }, 400

    elif resp.status_code != 200:
        logger.warning(
            "Error fetching count (status: %s) for url: %s",
            resp.status_code,
            request.url,
        )
        return {
            "status": "error",
            "error": "failed to fetch count",
        }, 400


    blob = resp.json()

    if not blob or "items" not in blob:
        return {"status": "error", "error": "no data"}, 400

    if not isinstance(blob["items"], list) or len(blob["items"]) != 1:
        return {"status": "error", "error": "unexpected data"}, 400

    if "views" not in blob["items"][0]:
        return {"status": "error", "error": "no view count"}, 400

    if not isinstance(blob["items"][0]["views"], int):
        return {"status": "error", "error": "invalid view count"}, 400

    return {
        "status": "ok",
        "count": blob["items"][0]["views"],
    }, 200
