import requests


def get_magnetlink(name: str, info_hash: str) -> str:
	trackers = [
		"udp://tracker.coppersurfer.tk:6969/announce",
		"udp://9.rarbg.to:2920/announce",
		"udp://tracker.opentrackr.org:1337",
		"udp://tracker.internetwarriors.net:1337/announce",
		"udp://tracker.leechers-paradise.org:6969/announce",
		"udp://tracker.coppersurfer.tk:6969/announce",
		"udp://tracker.pirateparty.gr:6969/announce",
		"udp://tracker.cyberia.is:6969/announce",
	]
	# magnetlink to redirect open to web browser
	return f'magnet:?xt=urn:btih:{info_hash}&dn={name}&tr={"&tr=".join(trackers)}'


class Torrent:
	@classmethod
	def query(cls, search_query) -> list['Torrent']:
		ret = []
		for torrent in requests.get(f'https://apibay.org/q.php?q={search_query}').json():
			obj = cls()
			obj.load_json(torrent)
			ret.append(obj)
		if ret[0].id == 0:
			return None
		return ret
	
	@classmethod
	def from_id(cls, torrent_id) -> 'Torrent':
		obj = cls()
		json = requests.get(
			f'https://apibay.org/t.php?id={torrent_id}'
		).json()
		obj.load_json(json)
		obj.load_more_json(json)
		if obj.name == 'Torrent does not exsist.': return None
		return obj
	
	def load_json(self, json):
		self.id: int            = int(json['id'])
		self.name: str          = json['name']
		self.info_hash: str     = json['info_hash']
		self.leechers: int      = int(json['leechers'])
		self.seeders: int       = int(json['seeders'])
		self.file_count: int    = int(json['num_files'])
		self.size: int          = int(json['size'])
		self.username: str      = json['username']
		self.added: int         = int(json['added'])
		self.status: str        = json['status']
		self.category: int      = int(json['category'])
		self.imdb: str          = json['imdb']
	
	def load_more_json(self, json):
		self.magnetlink: str    = get_magnetlink(self.name, self.info_hash)
		self.filelist: dict     = requests.get(f'https://apibay.org/f.php?id={self.id}').json()
		self.description: str   = json['descr']
		self.language: str      = json['language']
		self.text_language: str = json['textlanguage']
	
	def fetch_more_info(self):
		json = requests.get(
			f'https://apibay.org/t.php?id={self.id}'
		).json()
		self.load_more_json(json)
