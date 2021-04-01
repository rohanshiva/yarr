from deta import Deta
from feed import get_all
from item import create_items
from crawler import convert_items, discover_feed

deta = Deta()
folders_db = deta.Base("folders")
feeds_db = deta.Base("feeds")
items_db = deta.Base("items")
feed_errors_db = deta.Base("feed_errors")
settings_db = deta.Base("settings")


def reset_feed_errors():

    feed_errors = get_all(feed_errors_db, {})
    for err in feed_errors:
        feed_errors_db.delete(err["key"])
    return True


def update_new(items, links):

    new_items = []
    for item in items:
        if links.get(item["link"]) == None:
            new_items.append(item)
    create_items(new_items)


def reset_feeds():
    feeds = get_all(feeds_db, {})
    items = get_all(items_db, {})
    links = {}
    for item in items:
        links[item["link"]] = True
    for feed in feeds:
        feed_link = feed["feed_link"]
        fd, err = discover_feed(feed_link)
        if err == None:
            entries = fd.entries
            items = convert_items(entries, feed["key"])
            update_new(items, links)


def fetch_all_feeds():
    try:
        res = reset_feeds()
        return True
    except:
        return False
