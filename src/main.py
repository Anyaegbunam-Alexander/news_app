import flet as ft
from backup_restore import BackupRestore

from search_sources import SearchSource
from source_add import SourceAdd
from source_detail import SourceDetail
from source_edit import SourceEdit


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def route_change(route):
        page.views.clear()
        page.views.append(SearchSource(page).get_view())

        if "/sources/" in page.route:
            # get the path and query
            split_url = page.route.split("?")

            # check is a query exists;
            # though a query will always exist but it doesn't hurt to still check
            if len(split_url) > 1:
                # get the param (Topic.name) which will be the last item in the list
                param = split_url[-1]
            else:
                param = None

            # now we get the path and the page id
            path = split_url[0]

            # this may raise an error but only if the actual db is tampered with
            # and the pks are no longer integers.
            # In that case, it's the user's fault
            page_id = int(path.split("/")[-1])
            page.views.append(SourceDetail(page=page, id=page_id, param=param).get_view())

        elif "/add" in page.route:
            page.views.append(SourceAdd(page=page).get_view())

        elif "/edit" in page.route:
            # this may also raise an error but only if the actual db is tampered with
            # and the pks are no longer integers.
            # In that case, it's the user's fault
            page_id = int(page.route.split("/")[-1])
            page.views.append(SourceEdit(page=page, id=page_id).get_view())

        elif "/backup" in page.route:
            page.views.append(BackupRestore(page=page).get_view())

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # set to mobile dimensions since it is intended as a mobile app
    page.window_height = 915
    page.window_width = 412
    page.go(page.route)


ft.app(target=main, assets_dir="assets")
