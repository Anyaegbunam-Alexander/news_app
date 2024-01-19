import flet as ft

from items import S_KEYS, SOURCES

from source_detail import SourceDetail


class SearchSource:
    def __init__(self, page: ft.Page):
        self.page = page

    def build(self):
        self.page.add(self.search_box_row(), self.search_count_row(), self.search_results())
        # self.page.update()

    def rebuild(self, e):
        self.page.clean()
        self.build()
        self.page.update()

    def results(self):
        results = []

        for i in range(3):
            source = S_KEYS[i]
            
            def show_source_detail(e):
                self.page.clean()
                source_detail = SourceDetail(self.page, id=i)
                source_detail.change_source_btn.on_click = self.rebuild
                source_detail.build()
                self.page.update()

            column = ft.Column(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.Image(
                                            src=SOURCES[source],
                                            border_radius=50,
                                            width=60,
                                            height=60,
                                        ),
                                        ft.Text(source),
                                    ]
                                ),
                                ft.Row(
                                    [
                                        ft.IconButton(icon=ft.icons.NAVIGATE_NEXT, on_click=show_source_detail),
                                    ]
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        on_click=show_source_detail
                    ),
                    ft.Divider(height=9, thickness=3),
                ],
                
            )
        
            results.append(column)

        return results

    def search_results(self):
        return ft.Column(spacing=3, controls=self.results())

    def search_box_row(self):
        return ft.Row(
            [
                ft.TextField(label="Search for sources..."),
                ft.IconButton(icon=ft.icons.SEARCH),
            ]
        )

    def search_count_row(self):
        return ft.Row(
            [
                ft.Text("Sources matching search"),
                ft.Text("24"),
            ]
        )
    