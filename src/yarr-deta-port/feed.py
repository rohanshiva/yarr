import html 
from deta import Deta
deta = Deta(os.getenv("DETA_PROJECT_KEY"))
feeds_db = deta.Base('feeds')
items_db = deta.Base('items')


def get_all(db, query):
    blob_gen = db.fetch(query)
    blobs = []
    for stored_blob in blob_gen:
        for blob in stored_blob:
            blobs.append(blob)
    return blobs


def create_feed(title, description, link, feed_link, folder_id):
    title = html.unescape(title)

    if title == "":
        title = "<???>"
    try:
        feed = feeds_db.put({'title': title, 'description': description, 'link': link, 'feed_link': feed_link, 'folder_id': folder_id})
        return feed
    except:
        print("Failed to create feed.")
        return None
    
def rename_feed(id, title):
    try:
        feed = feeds_db.get(id)
        feed['title'] = title
        feeds_db.put(feed)
        return True
    except:
        return False
    
def update_feed_folder(id, folder):
    try:
        feed = feeds_db.get(id)
        feed['folder_id'] = folder
        feeds_db.put(feed)
        return True
    except:
        return False

def delete_feed(id):
    try:
        res = feeds_db.delete(id)
        res = delete_items(id)
        return True
    except:
        return False

def delete_items(feed_id):
    query = {"feed_id":feed_id}
    items = get_all(items_db, query)
    for item in items:
        items_db.delete(item['key'])

