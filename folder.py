from deta import Deta
deta = Deta('project_key')
folders_db = deta.Base('folders')
feeds_db = deta.Base('feeds')





def CreateFolder(title):
    expanded = 1
    folders = next(folders_db.fetch())
    
    # Do nothing if folder with name already exists
    for folder in folders:
        if folder['title']==title:
            return folder
    try:
        res = folders_db.put({'title':title, 'is_expanded':expanded})
        return res
    except:
        print("Something bad happened.")
        return None

def RenameFolder(id, title):
    try:
        folder = folders_db.get(id)
        folder['title'] = title
        folders_db.put(folder)
        return True
    except:
        return False

def ToggleFolderExpanded(id, isExpanded):
    try:
        folder = folders_db.get(id)
        folder['is_expanded'] = isExpanded
        folders_db.put(folder)
        return True
    except:
        return False

def putItems(items):
    print(len(items))
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

def DeleteFolder(id):
    try:
        folders_db.delete(id)
        feeds = next(feeds_db.fetch({"folder_id":id}))
        for feed in feeds:
            feed['folder_id'] = None
        putItems(feeds)
        return True
    except:
        return False




