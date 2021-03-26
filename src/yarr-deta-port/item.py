from datetime import datetime
import base64
from deta import Deta
deta = Deta(os.getenv("DETA_PROJECT_KEY"))
items_db = deta.Base('items')
feeds_db = deta.Base('feeds')

def get_all(db, query):
    blob_gen = db.fetch(query)
    blobs = []
    for stored_blob in blob_gen:
        for blob in stored_blob:
            blobs.append(blob)
    return blobs

def create_items(items):
    now = datetime.now()
    try:
        for i, item in enumerate(items):
            if item['guid'] == '':
                item['guid'] = item['link']
            item['date_arrived'] = str(now)
            item['status'] = 'unread'
        put_items(items)
        return True
    except:
        return False

def put_items(items):
    n = len(items)

    if (n <= 24):
        res = items_db.put_many(items);
        return
    start = 0
    end = 0
    while(end!=n):
        end+=24
        if (end > n):
            end = n
        try:
            res = items_db.put_many(items[start:end])
        except:
            print('Failed to push items')
        start = end
    
def update_item_status(id, status):
    try:
        # item_status = {"unread":0, "read": 1, "starred": 2}
        item = items_db.get(id)
        item['status'] = status
        items_db.put(item)
        return True
    except:
        return False


def list_query_predicate(filter):
    # item_status = {"unread":0, "read": 1, "starred": 2}

    # if filter.get('status') != None:
    #     filter['status'] = item_status[filter['status']]
    if filter.get('search') != None:
        filter['title?contains'] = filter.pop('search')
    
    if filter.get('folder_id') == None:
        return get_all(items_db, filter)
    
    else:
        folder_query  = {'folder_id': filter['folder_id']}
        print(folder_query)
        feeds = get_all(feeds_db, folder_query)
        filter.pop('folder_id')
        query = []
        for feed in feeds:
            d = {'feed_id': feed['key']}
            d.update(filter)
            query.append(d)
        print(query)
        return get_all(items_db, query)

def list_items(filter, offset, limit, newest_first):
    result = list_query_predicate(filter)
    count = len(result)
    result = result[offset:]
    if len(result)> limit:
        result = result[:limit]
    print(len(result))
    for l in result:
        l['id'] = l.pop('key')
    return result, count

def count_items(filter):
    res = list_query_predicate(filter)
    return len(res)

def feed_stats():
    feeds = get_all(feeds_db, {})
    res = []
    for feed in feeds:
        stat = {'feed_id': feed['key']}
        stat['unread'] = len(get_all(items_db, {'feed_id': feed['key'], 'status':'unread'}))
        stat['read'] = len(get_all(items_db, {'feed_id': feed['key'], 'status':'read'}))
        stat['starred'] = len(get_all(items_db, {'feed_id': feed['key'], 'status':'starred'}))
        res.append(stat)
    return res
    