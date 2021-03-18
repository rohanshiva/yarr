import html

from deta import Deta
deta = Deta('project_key')
feeds_db = deta.Base('feeds')
items_db = deta.Base('items')

def CreateFeed(title, description, link, feed_link, folder_id):
    title = html.unescape(title)

    if title == "":
        title = "<???>"
    print(title)
    try:
        feed = feeds_db.put({'title': title, 'description': description, 'link': link, 'feed_link': feed_link, 'folder_id': folder_id})
        return feed
    except:
        print("Failed to create feed.")
        return None


def RenameFeed(id, title):
    try:
        feed = feeds_db.get(id)
        feed['title'] = title
        feeds_db.put(feed)
        return True
    except:
        return False

def UpdateFeedFolder(id, folder):
    try:
        feed = feeds_db.get(id)
        feed['folder_id'] = folder
        feeds_db.put(feed)
        return True
    except:
        return False

def DeleteFeed(id):
    try:
        feeds_db.delete(id)
        DeleteItems(id)
        return True
    except:
        return False

def DeleteItems(feedId):
    items = next(items_db.fetch({"feed_id":feedId}))
    for item in items:
        items_db.delete(item['key'])
    


