import os
from typing import Optional
from fastapi import FastAPI, Request, status, HTTPException
from pydantic import BaseModel
from deta import Deta
from folder import CreateFolder, RenameFolder, ToggleFolderExpanded, DeleteFolder
from feed import CreateFeed, UpdateFeedFolder, RenameFeed, DeleteFeed
from item import CreateItems
from crawler import discoverFeed, convertItems


deta = Deta('project_key')
folders_db = deta.Base('folders')
feeds_db = deta.Base('feeds')

app = FastAPI()

class NewFolder(BaseModel):
    title: str

class Folder(BaseModel):
    title: Optional[str] = None
    isExpanded: Optional[int] = None

class FeedUpdate(BaseModel):
    title: Optional[str] = None
    FolderID: Optional[str] = None

class FeedCreateForm(BaseModel):
    Url: str
    FolderID: str

@app.get("/api/folders")
def FolderListHandler():
    try:
        list = next(folders_db.fetch())
        return list
    except:
        return "Failed to fetch folders."

@app.post("/api/folders")
def FolderListHandler(folder : NewFolder):
    try:
        if len(folder.title) == 0:
            return {'Error':'Folder title is missing.'}
        res = CreateFolder(folder.title)
        return res
    except:
        return {'Error': 'Failed to create folder'}


@app.put('/api/folders/{id}', status_code=200)
def FolderHandler(id:str, folder: Folder):
    try:
        if folder.title != None and len(folder.title) != 0:
            res = RenameFolder(id, folder.title)
        if folder.isExpanded != None:
            res = ToggleFolderExpanded(id, folder.isExpanded)
        return 
    except:
        return {'Error': 'Bad request'}

@app.delete('/api/folders/{id}')
def FolderHandler(id:str):
    try:
        DeleteFolder(id)
    except:
        return {'Error':'Failed to delete'}


@app.get('/api/feeds/')
def FeedListHandler():
    try:
        list = next(feeds_db.fetch())
        return list
    except:
        return "Failed to fetch feeds."

@app.post('/api/feeds/')
def FeedListHandler(feedReq: FeedCreateForm):
    feed, err = discoverFeed(feedReq.Url)
    if err != None:
        return {"status": "notfound"}

    if feed != None:
        entries = feed.entries
        feed = feed.feed
        
        description = ""
        if feed.get('subtitle')!=None:
            description = feed.subtitle

        title = ""
        if feed.get('title')!=None:
            title = feed.title
        
        link = ""
        if feed.get('link')!=None:
            link = feed.link

        feed_link = feedReq.Url

        folder_id = feedReq.FolderID

        storedFeed = CreateFeed(title, description, link, feed_link, folder_id)

        if storedFeed != None:
            items = convertItems(entries, storedFeed['key'])

            CreateItems(items)
            image = None
            # if 'image' in feed.keys():
            #     image = feed.image
            storedFeed['icon'] = image

            feeds_db.put(storedFeed)
            # Todo
        return {"status": "success"}
    else:
        return {"status": "notfound"}


@app.put('/api/feeds/{id}')
def FeedHandler(id:str, feedUpdate: FeedUpdate):
    try:
        feed = feeds_db.get(id)
        if feed == None:
            raise HTTPException(status_code=400)
        if feedUpdate.title != None and len(feedUpdate.title) != 0:
            res = RenameFeed(id, feedUpdate.title)
        if feedUpdate.FolderID != None and len(feedUpdate.FolderID) != 0:
            res = UpdateFeedFolder(id, feedUpdate.FolderID)
    except:
        raise HTTPException(status_code=405)

@app.delete('/api/feeds/{id}')
def FeedHandler(id: str):
    DeleteFeed(id)

@app.

@app.get('/api/settings')
def SettingsHandler():
    try:
        settings_db = deta.Base('settings')
        res =  next(settings_db.fetch())
        return res
    except:
        return {'Error': 'Failed to fetch settings'}
    



    