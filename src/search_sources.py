import flet as ft

from queries import Query


class SearchSource:
    def __init__(self, page: ft.Page):
        self.page = page

    def get_view(self):
        return ft.View("/", list(self.view_build()))

    def view_build(self):
        return self.search_box_row(), self.search_count_row(), self.search_results()

    def results(self):
        results = []
        for source in Query().get_sources():
            # create the on_click function that goes to the source detail for SourceDetail
            on_click = lambda _, s_id=source.id, s_default=source.extensions[0].name: self.page.go(
                f"/sources/{s_id}?{s_default}"
            )
            column = ft.Column(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Row(
                                    [
                                        ft.Image(
                                            src=source.image_url,
                                            border_radius=50,
                                            width=60,
                                            height=60,
                                        ),
                                        ft.Text(source.name),
                                    ]
                                ),
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.icons.NAVIGATE_NEXT, on_click=on_click
                                        ),
                                    ]
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        on_click=on_click,
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
