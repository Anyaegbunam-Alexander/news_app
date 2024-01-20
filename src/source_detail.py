import flet as ft
from faker import Faker

from parsers import BaseParser
from queries import Query

fake = Faker()

class SourceDetail:
    def __init__(self, page: ft.Page, id, param) -> None:
        self.page = page
        self.source_id = id
        self.param = param

    def get_view(self):
        return ft.View(f"/sources/{self.source_id}", list(self.view_build()))
    
    def view_build(self):
        return self.source_row(), self.source_extensions(), self.source_results()


    def source_row(self):
        source_id, source_name, source_url, source_image, _ = Query().get_one_source(self.source_id)
        return ft.Row(
            [
                ft.Row(
                    [
                        ft.Image(
                            src=source_image,
                            border_radius=50,
                            width=40,
                            height=40,
                        ),
                        ft.TextButton(f"{source_name} website", url=source_url),
                    ]
                ),
                ft.Row(
                    [
                        ft.TextButton("Change source", on_click=lambda _: self.page.go("/")),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def source_extensions(self):
        extensions = []
        for ext in Query().get_source_extensions(self.source_id):
            _, ext_url, ext_name, _ = ext
            on_click = lambda _, s_id=self.source_id, s_ext_name=ext_name: self.page.go(f"/sources/{s_id}?{s_ext_name}")
            if ext_name == self.param:
                text_button = ft.TextButton(ext_name, on_click=on_click, autofocus=True)
            else:
                text_button = ft.TextButton(ext_name, on_click=on_click)

            extensions.append(text_button)
        
        column = ft.Column(
            [
                ft.Text("Latest"),
                ft.Row(extensions, scroll=ft.ScrollMode.ADAPTIVE, alignment=ft.alignment.top_left),
            ]
        )
        return ft.Container(column)

    def get_url(self):
        # if self.param:
        ext = Query().get_one_source_extension(self.source_id, self.param)
        _, ext_url, _, _ = ext
        return ext_url 

    def results(self):
        results = ft.ListView(expand=1, spacing=10, padding=20)
        content = BaseParser(url=self.get_url()).get_data()
        for data in content:
            results.controls.append(
                ft.Container(
                    ft.Column(
                        [
                            ft.ResponsiveRow(
                                [
                                    ft.Image(data.image_url, width=150, height=150),
                                    ft.Column(
                                        [
                                            ft.Text(data.title, width=self.page.width),
                                            ft.Row(
                                                [
                                                    ft.Icon(ft.icons.ACCESS_TIME_FILLED_ROUNDED),
                                                    ft.Text(data.published),
                                                ]
                                            ),
                                        ]
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Divider(height=9, thickness=3),
                        ]
                    ),
                    on_click=self.on_click,
                )
            )
        return results

    def source_results(self):
        return self.results()

    def on_click(self, e):
        pass
