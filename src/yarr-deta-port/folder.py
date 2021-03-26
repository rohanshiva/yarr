from deta import Deta
deta = Deta(os.getenv("DETA_PROJECT_KEY"))
folders_db = deta.Base('folders')
feeds_db = deta.Base('feeds')



def get_all(db, query):
    blob_gen = db.fetch(query)
    blobs = []
    for stored_blob in blob_gen:
        for blob in stored_blob:
            blobs.append(blob)
    return blobs


def create_folder(title):
    expanded = True
    folders = get_all(folders_db, {})

    for folder in folders:
        if folder['title']==title:
            return folder
    try:
        res = folders_db.put({'title':title, 'is_expanded':expanded})
        return res
    except:
        print("Something bad happened.")
        return None


def rename_folder(id, title):
    try:
        folder = folders_db.get(id)
        folder['title'] = title
        folders_db.put(folder)
        return True
    except:
        return False


def toggle_folder_expanded(id, is_expanded):
    try:
        folder = folders_db.get(id)
        folder['is_expanded'] = is_expanded
        folders_db.put(folder)
        return True
    except:
        return False

def put_items(items):
    n = len(items)

    if (n <= 24):
        res = feeds_db.put_many(items);
        return

    start = 0
    end = 0
    while(end!=n):
        end+=24
        if (end > n):
            end = n
        try:
            res = feeds_db.put_many(items[start:end])
        except:
            print('Failed to push items')
        start = end

def delete_folder(id):
    try:
        folders_db.delete(id)
        query = {"folder_id":id}
        feeds = get_all(feeds_db, query)
        for feed in feeds:
            feed['folder_id'] = None
        put_items(feeds)
        return True
    except:
        return False