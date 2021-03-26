import feedparser 

def discover_feed(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        if feed.bozo:
            error = 'No feeds found at given url'
            return None, error
        else:
            return feed, None
    except:
        error = 'Failed to fetch feed'
        return None, error

def convert_items(entries, feed_id):
    result = [{}]*len(entries)

    for i, item in enumerate(entries):

        image_url = ''
        if item.get('image')!=None:
            image_url = item['image']
        
        author = ''
        if item.get('author')!=None:
            author = item['author']
        
        podcast_url = ''
        if item.get('enclosures')!=None:
            for enclosure in item['enclosures']:
                podcast_url = entries['href']
        
        published = ''
        if item.get('published')!=None:
            published = item['published']

        updated = None
        if item.get('updated')!=None:
            updated = item['updated']
        
        description = item['summary']
        if item.get('description')!=None:
            description = item['description']

        title = ''
        if item.get('title')!=None:
            title = item['title']

        link = ''
        if item.get('link')!=None:
            link = item['link']

        content = ''
        if item.get('content')!=None:
            content = item['content'][0]['value']

        guidislink = ''
        if item.get('id')!=None:
            guidislink = item['id']

        result[i] = {
            "guid": guidislink,
            "feed_id":feed_id,
            "title": title,
            "link": link,
            "description": description,
            "content": content,
            "author": author, 
            "date": published,
            "date_updated": updated,
            "status": 0,
            "image": image_url,
            "podcast_url": podcast_url
        }
    return result

