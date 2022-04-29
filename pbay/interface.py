import os
import webbrowser
from datetime import datetime

import rich.box
import rich_click as click
from datasize import DataSize
from rich.console import Console
from rich.highlighter import RegexHighlighter
from rich.table import Table

from thepiratebay import Torrent

console = Console()


@click.group()
def main():
	...

@main.command()
@click.argument('search_query', required=True)
@click.option('--fmt', default='sSlud', type=str)
@click.option('--no-wrap', default=False)
@click.option('--count', default=None, type=int)
def search(search_query: str, fmt: str, no_wrap: bool, count: int):
	torrents = Torrent.query(search_query)
	if torrents is None:
		console.print(f'[bright_yellow]No results found for "[green]{search_query}"')
		return
	table = Table(
		pad_edge=False,
		box=rich.box.SIMPLE,
		expand=True
	)
	table.add_column('ID', justify='right', style='bright_yellow')
	table.add_column('Name', style='bright_green', no_wrap=no_wrap)
	columns = {
	's': lambda: table.add_column('Size', justify='right', style='bright_blue'),
	'S': lambda: table.add_column('SE', justify='right', style='bright_cyan'),
	'l': lambda: table.add_column('LE', justify='right', style='bright_red'),
	'f': lambda: table.add_column('F', justify='right', style='bright_green'),
	'u': lambda: table.add_column('User', style='bright_yellow', no_wrap=no_wrap),
	'd': lambda: table.add_column('Added', justify='right', style='bright_blue')
	}
	col_content = {
	's': lambda t: f'{DataSize(t.size):.2a}',
	'S': lambda t: str(t.seeders),
	'l': lambda t: str(t.leechers),
	'f': lambda t: str(t.file_count),
	'u': lambda t: t.username + (f' [blue]({t.status})[/blue]' if t.status != 'member' else ''),
	'd': lambda t: datetime.fromtimestamp(t.added).strftime('%-d/%-m/%Y')
	}
	for i in fmt:
		columns[i]()
	if count is None:
		count = len(torrents)
	for torrent in torrents[:count]:
		table.add_row(str(torrent.id), torrent.name, *[col_content[i](torrent) for i in fmt])
	console.print(table)


@main.command()
@click.argument('TORRENT_ID', type=int)
def info(torrent_id: int):
	torrent = Torrent.from_id(torrent_id)
	if torrent is None:
		console.print(f'[bright_yellow]The torrent with the id [green]{torrent_id}[/green] does not exist')
		return
	console.print(f'\n [bold yellow on bright_black]{torrent.name}\n', highlight=False)
	console.print(torrent.description)
	table = Table(box=rich.box.SIMPLE)
	table.add_column('File', style='bright_blue')
	table.add_column('Size', justify='right', style='bright_cyan')
	for item in torrent.filelist:
		table.add_row(item['name']['0'], f'{DataSize(int(item["size"]["0"])):.2a}')
	console.print(table)


@main.command()
@click.argument('TORRENT_ID', type=int)
def magnetlink(torrent_id: int):
	torrent = Torrent.from_id(torrent_id)
	webbrowser.open(torrent.magnetlink, new=0, autoraise=True)
