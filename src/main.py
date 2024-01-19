import flet as ft

from search_sources import SearchSource
from source_detail import SourceDetail

def main(page: ft.Page):
    page.title = "Search Sources"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    SearchSource(page).build()
    page.window_height = 915
    page.window_width = 412
    page.update()

ft.app(target=main)
