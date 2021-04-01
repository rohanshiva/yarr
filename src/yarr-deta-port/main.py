import os
import math
from typing import Optional
from fastapi import FastAPI, Request, status, HTTPException

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from deta import Deta
from folder import create_folder, rename_folder, toggle_folder_expanded, delete_folder
from feed import create_feed, update_feed_folder, rename_feed, delete_feed, get_all
from item import create_items, update_item_status, list_items, count_items, feed_stats
from refresh import fetch_all_feeds
from crawler import discover_feed, convert_items

deta = Deta()
folders_db = deta.Base("folders")
feeds_db = deta.Base("feeds")
items_db = deta.Base("items")
errors_db = deta.Base("feed_errors")
settings_db = deta.Base("settings")

app = FastAPI()
app.mount("/static/", StaticFiles(directory="assets"), name="static")


class New_Folder(BaseModel):
    title: str


class Folder(BaseModel):
    title: Optional[str] = None
    is_expanded: Optional[bool] = None


class Feed_Update(BaseModel):
    title: Optional[str] = None
    folder_id: Optional[str] = None


class Feed_Create_Form(BaseModel):
    url: str
    folder_id: Optional[str] = None


class Item_Update_Form(BaseModel):
    status: Optional[str] = None


class Settings(BaseModel):
    filter: Optional[str] = ""
    feed: Optional[str] = ""
    feed_list_width: Optional[int] = 300
    item_list_handler: Optional[int] = 300
    sort_newest_first: Optional[bool] = True
    theme_name: Optional[str] = "light"
    theme_font: Optional[str] = ""
    theme_size: Optional[int] = 1
    refresh_rate: Optional[int] = 0


default_settings = {
    "key": "settings",
    "filter": "",
    "feed": "",
    "feed_list_width": 300,
    "item_list_width": 300,
    "sort_newest_first": True,
    "theme_name": "light",
    "theme_font": "",
    "theme_size": 1,
    "refresh_rate": 0,
}


@app.get("/")
def render_page(request: Request):
    return FileResponse("assets/index.html")


@app.get("/api/folders")
def folder_list_handler():
    try:
        list = get_all(folders_db, {})
        for l in list:
            l["id"] = l.pop("key")
        return list
    except:
        raise HTTPException(status_code=400, detail="Failed to fetch folders.")


@app.post("/api/folders")
def folder_list_handler(folder: New_Folder):
    try:
        if len(folder.title) == 0:
            return {"Error": "Folder title is missing."}
        res = create_folder(folder.title)
        return res
    except:
        return {"Error": "Failed to create folder"}


@app.put("/api/folders/{id}", status_code=200)
def folder_handler(id: str, folder: Folder):
    try:
        if folder.title != None and len(folder.title) != 0:
            res = rename_folder(id, folder.title)
        if folder.is_expanded != None:
            res = toggle_folder_expanded(id, folder.is_expanded)
        return
    except:
        return {"Error": "Bad request"}


@app.delete("/api/folders/{id}", status_code=204)
def folder_handler(id: str):
    try:
        delete_folder(id)
        return
    except:
        raise HTTPException(status_code=400, detail="Failed to delete")


@app.post("/api/feeds/refresh", status_code=200)
def feed_refresh_handler():
    try:
        res = fetch_all_feeds()
        return True
    except:
        raise HTTPException(status_code=400, detail="Failed to refresh")


@app.get("/api/feeds/errors")
def feed_errors_handler():
    try:
        errors = get_all(errors_db, {})
        return errors
    except:
        raise HTTPException(status_code=400, detail="Failed to fetch errors")


@app.get("/api/feeds")
def feed_list_handler():
    try:
        list = get_all(feeds_db, {})
        for l in list:
            l["id"] = l.pop("key")
        return list
    except:
        return "Failed to fetch feeds."


@app.post("/api/feeds")
def feed_list_handler(feed_req: Feed_Create_Form):
    try:
        feed, err = discover_feed(feed_req.url)
        if err != None:
            return {"status": "notfound"}

        if feed != None:
            entries = feed.entries

            feed = feed.feed

            description = ""
            if feed.get("subtitle") != None:
                description = feed.subtitle

            title = ""
            if feed.get("title") != None:
                title = feed.title

            link = ""
            if feed.get("link") != None:
                link = feed.link

            feed_link = feed_req.url

            folder_id = feed_req.folder_id

            stored_feed = create_feed(title, description, link, feed_link, folder_id)

            if stored_feed != None:
                items = convert_items(entries, stored_feed["key"])

                create_items(items)

                image = False
                if feed.get("image") != None:

                    image = feed.image.href
                stored_feed["icon"] = image

                feeds_db.put(stored_feed)
                # Todo
            return {"status": "success"}
        else:
            return {"status": "notfound"}
    except:
        raise HTTPException(status_code=400, detail="Failed to make feed")


@app.put("/api/feeds/{id}")
def feed_handler(id: str, feed_update: Feed_Update):
    try:
        feed = feeds_db.get(id)
        if feed == None:
            raise HTTPException(status_code=400)
        if feed_update.title != None and len(feed_update.title) != 0:
            res = rename_feed(id, feed_update.title)
        if feed_update.folder_id != None and len(feed_update.folder_id) != 0:
            res = update_feed_folder(id, feed_update.folder_id)
    except:
        raise HTTPException(status_code=405)


@app.delete("/api/feeds/{id}", status_code=204)
def feed_handler(id: str):
    delete_feed(id)
    return


@app.put("/api/items/{id}")
def item_handler(id: str, item_update: Item_Update_Form):
    try:
        if item_update.status != None:
            update_item_status(id, str(item_update.status))
    except:
        raise HTTPException(status_code=400)


@app.get("/api/items")
def item_list_handler(
    page: int = None,
    folder_id: str = None,
    feed_id: str = None,
    status: str = None,
    search: str = None,
    oldest_first: bool = None,
):
    per_page = 20
    cur_page = 1

    if page != None:
        cur_page = int(page)
    filter = {}
    if folder_id != None:
        filter["folder_id"] = folder_id

    if feed_id != None:
        filter["feed_id"] = feed_id

    if status != None:
        filter["status"] = status

    if search != None:
        filter["search"] = search

    newest_first = True

    items, count = list_items(filter, (cur_page - 1) * per_page, per_page, newest_first)


    return {
        "page": {
            "cur": cur_page,
            "num": int(math.ceil(float(count) / float(per_page))),
        },
        "list": items,
    }


@app.get("/api/settings")
def settings_handler():
    try:
        settings = settings_db.get("settings")
        if settings == None:
            settings_db.put(default_settings)
            settings = default_settings
            del settings["key"]
            return settings
        else:
            del settings["key"]
            return settings
    except:
        raise HTTPException(status_code=400, detail="Failed to fetch settings")


@app.put("/api/settings")
def settings_handler(settings: Settings):
    updates = {}
    updates["filter"] = settings.filter
    updates["feed"] = settings.feed
    updates["feed_list_width"] = settings.feed_list_width
    updates["item_list_handler"] = settings.item_list_handler
    updates["sort_newest_first"] = settings.sort_newest_first
    updates["theme_name"] = settings.theme_name
    updates["theme_font"] = settings.theme_font
    updates["theme_size"] = settings.theme_size
    updates["refresh_rate"] = 0
    settings_db.put(updates, "settings")
    return settings


@app.get("/api/status")
def status_handler():
    try:
        res = {"running": 0}
        res["stats"] = feed_stats()
        return res
    except:
        raise HTTPException(status_code=400)
