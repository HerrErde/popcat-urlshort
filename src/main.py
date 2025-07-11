import uvicorn
from quart import Quart, jsonify, render_template, request

import config
from db import DBHandler

app = Quart(__name__)
app.url_map.strict_slashes = False

db_handler = DBHandler()


@app.before_serving
async def before_serving():
    await db_handler.initialize()


@app.route("/")
async def home():
    data = await db_handler.list()
    return await render_template("index.html", data=data)


@app.route("/<short>", methods=["GET"])
async def redirect_url(short):
    url = await db_handler.redirect(short)
    if url:
        return await render_template("redirect.html", url=url)
    else:
        return await render_template("error.html"), 404


@app.route("/api/create", methods=["POST"])
async def set_urls():
    data = await request.json
    full = data.get("full")
    short = data.get("short")

    if not full:
        return jsonify({"error": "Full URL is required"}), 400

    success, short = await db_handler.create(full, short)
    if success:
        return jsonify({"url": f"/{short}"}), 200
    else:
        return jsonify({"error": "Short URL already exists"}), 400


@app.route("/<short>/info", methods=["GET"])
async def url_info_page(short):
    success, data = await db_handler.info(short)
    if success:
        return await render_template("info.html", data=data)
    else:
        return jsonify({"error": "Short URL doesn't exist"}), 404


@app.route("/api/get/<short>", methods=["GET"])
async def url_info(short):
    success, url = await db_handler.info(short)
    if success:
        return jsonify(url), 200
    elif success and not data:
        return jsonify({"error": "Short URL not found"}), 404
    else:
        return jsonify({"error": "There was an Error"}), 500


@app.route("/api/all", methods=["GET"])
async def all_urls():
    success, data = await db_handler.list()
    if success and data:
        return jsonify(data), 200
    elif success and not data:
        return jsonify({"error": "No URLs found"}), 404
    else:
        return jsonify({"error": "There was an Error"}), 500


@app.errorhandler(404)
async def not_found(e):
    return await render_template("error.html"), 404


startargs = {"host": config.HOST, "port": config.PORT, "reload": config.DEBUG}

if __name__ == "__main__":
    uvicorn.run("main:app", **startargs)
