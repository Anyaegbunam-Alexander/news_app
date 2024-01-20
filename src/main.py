import flet as ft

from search_sources import SearchSource
from source_detail import SourceDetail


def main(page: ft.Page):
    page.title = "Search Sources"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def route_change(route):
        page.views.clear()
        page.views.append(SearchSource(page).get_view())

        if "/sources/" in page.route:
            split_url = page.route.split("?")
            
            if len(split_url) > 1:
                param = split_url[-1]
            else:
                param = None

            path = split_url[0]
            page_id = int(path.split("/")[-1])
            page.views.append(SourceDetail(page=page, id=page_id, param=param).get_view())
        
        page.window_height = 915
        page.window_width = 412
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main, assets_dir="assets")
