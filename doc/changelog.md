# upcoming

- (new) keyboard shortcuts to scroll article content
- (fix) `-base` not serving static files (thanks to @vfaronov)

# v1.4 (2021-03-11)

- (new) keyboard shortcuts (thanks to @Duarte-Dias)
- (new) show podcast audio
- (fix) deleting feeds
- (etc) minor ui tweaks & changes

# v1.3 (2021-02-18)

- (fix) log out functionality if authentication is set
- (fix) import opml if authentication is set
- (fix) login page if authentication is set (thanks to @einschmidt)

# v1.2 (2021-02-11)

- (new) autorefresh rate
- (new) reduced bandwidth usage via stateful http headers `last-modified/etag`
- (new) show feed errors in feed management modal
- (new) `-open` flag for automatically opening the server url
- (new) `-base` flag for serving urls under non-root path (thanks to @hcl)
- (new) `-auth-file` flag for authentication
- (new) `-cert-file` & `-key-file` flags for TLS
- (fix) wrapping long words in the ui to prevent vertical scroll
- (fix) increased toolbar height in mobile/tablet layout (thanks to @einschmidt)

# v1.1 (2020-10-05)

- (new) responsive design
- (fix) server crash on favicon fetch timeout (reported by @minioin)
- (fix) handling byte order marks in feeds (reported by @ilaer)
- (fix) deleting a feed raises exception in the ui if the feed's items are shown.

# v1.0 (2020-09-24)

Initial Release
