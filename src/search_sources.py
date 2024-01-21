import flet as ft

from queries import Query


class SearchSource:
    def __init__(self, page: ft.Page):
        self.page = page
        self.search_term = None
        self.search_field = ft.TextField(label="Search for sources...")

    def get_view(self):
        return ft.View("/", self.view_build())

    def view_build(self):
        self.page.title = "Search Sources"
        return self.search_box_row(), self.search_results()

    def results(self):
        if self.search_term is None:
            sources = Query().get_sources()
        else:
            sources = Query().search_source_by_name(self.search_term)

        results = []
        for source in sources:
            # create the on_click function that goes to the source detail for SourceDetail
            on_click = lambda _, s_id=source.id, s_default=source.topics[0].name: self.page.go(
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
        return ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            self.search_field,
                            ft.IconButton(icon=ft.icons.SEARCH, on_click=self.update_search),
                        ]
                    ),
                    ft.Row(
                        [
                            ft.TextButton("Clear search", on_click=self.clear_search),
                            ft.TextButton(
                                "Add new source",
                                icon=ft.icons.ADD_CIRCLE,
                                on_click=lambda _: self.page.go("/add"),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ]
            ),
            margin=ft.margin.only(top=20, bottom=40),
        )

    def clear_search(self, e):
        self.search_field.value = None
        self.update_search(e)

    def update_search(self, _):
        self.search_term = self.search_field.value
        self.page.views.clear()
        self.page.views.append(self.get_view())
        self.page.update()
