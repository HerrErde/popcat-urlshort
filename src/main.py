from datetime import datetime

import pytz
import uvicorn
from quart import Quart, jsonify, redirect, render_template, request, url_for

import config
from db import DBHandler

app = Quart(__name__)
app.url_map.strict_slashes = False
app.debug = config.DEBUG

db_handler = DBHandler()


@app.before_serving
async def before_serving():
    await db_handler.initialize()


@app.route("/")
async def home():
    page = int(request.args.get("page", 1))
    per_page = 48

    success, page_data, total = await db_handler.list(page, per_page)
    if not success:
        page_data = []
        total = 0

    total_pages = (total + per_page - 1) // per_page

    return await render_template(
        "index.html", data=page_data, page=page, total_pages=total_pages, total=total
    )


@app.route("/<short>", methods=["GET"])
async def redirect_url(short):
    url = await db_handler.redirect(short)
    if url:
        return await redirect(url)
    else:
        return await render_template("error.html"), 404


@app.route("/shorten", methods=["POST"])
async def shorten():
    data = await request.form
    full = data.get("full")
    short = data.get("short")

    if not full:
        return "Full URL is required", 400

    success, short = await db_handler.create(full, short)
    if success:
        return redirect(url_for("info", short=short))
    else:
        return "Short could not be created", 400


@app.route("/<short>/info", methods=["GET"], endpoint="info")
async def url_info(short):
    success, data = await db_handler.info(short)
    if not success:
        return jsonify({"error": "Short URL doesn't exist"}), 404

    tz = pytz.timezone(config.TZ)

    created_date = data["date"]
    date_format = config.DATE_FORMAT

    if created_date.tzinfo is None:
        created_date = tz.localize(created_date)

    days_active = (datetime.now(tz) - created_date).days

    data.update(
        {"days_active": days_active, "date_format": date_format, "date": created_date}
    )

    return await render_template("info.html", data=data)


@app.errorhandler(404)
async def not_found(e):
    return await render_template("error.html"), 404


startargs = {"host": config.HOST, "port": config.PORT, "reload": config.DEBUG}

if __name__ == "__main__":
    uvicorn.run("main:app", **startargs)
