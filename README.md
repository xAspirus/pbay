# pbay
cli tool to fetch torrents from thepiratebay.org written in Python.


## Usage
### Search
`pbay search [OPTIONS] SEARCH_QUERY`

Search for torrents by search query.

#### Options
`--fmt=str`: Which columns to show

Columns:

`s`: Size

`S`: Seeders

`l`: Leechers

`f`: Files

`u`: Username

`d`: Date Added

`--no-wrap`: false to disable wrapping of text

`--count`: Number of torrent entries to show

### Info
`pbay info [OPTIONS] TORRENT_ID`

Get description and file list of torrent by torrent id (Get this from search).

### Magnet Link
`pbay magnetlink [OPTIONS] TORRENT_ID`

Open the magnetlink of torrent by torrent id in a browser window.

## Installation

```
git clone https://github.com/xAspirus/pbay
```
If you use a unix shell, easiest way is to add a alias
```
# $RepoLocation is the location where you cloned the repo
alias pbay "python3 $RepoLocation/pbay"
```
