
from datetime import datetime

from deta import Deta
deta = Deta('project_key')
items_db = deta.Base('items')

def CreateItems(items):
    now = datetime.now()

    for i, item in enumerate(items):
        if item['guid'] == "":
            item['guid'] = item['link']
        item['date_arrived'] = str(now)

    items_db.put_many(items)


def putItems(items):
    print(len(items))
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
