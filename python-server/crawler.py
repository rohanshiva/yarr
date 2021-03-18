import feedparser

def discoverFeed(feed_url):
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

def convertItems(entries, feed_id):
    result = [{}]*len(entries)

    for i, item in enumerate(entries):

        imageURL = ''
        if item.get('image')!=None:
            imageURL = item['image']
        
        author = ''
        if item.get('author')!=None:
            author = item['author']
        
        podcastUrl = ''
        if item.get('enclosures')!=None:
            for enclosure in item['enclosures']:
                podcastUrl = entries['href']
        
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
            "image": imageURL,
            "podcast_url": podcastUrl
        }
    return result