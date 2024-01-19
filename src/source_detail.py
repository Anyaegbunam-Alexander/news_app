import flet as ft
from faker import Faker

from items import CNN

fake = Faker()
from items import IMAGES

EXTENSIONS = [
    "Top Stories",
    "Entertainment",
    "Finance",
    "Media",
    "Gaming",
    "Sports",
    "Arts",
    "Food",
    "Travel",
    "World",
    "Africa",
]


class SourceDetail:
    def __init__(self, page: ft.Page, id: int = 1) -> None:
        self.page = page
        self.source_id = id
        self.change_source_btn = ft.TextButton("Change source")

    def build(self):
        self.page.add(self.source_row(), self.source_extensions(), self.source_results())

    def source_row(self):
        return ft.Row(
            [
                ft.Row(
                    [
                        ft.Image(
                            src=CNN,
                            border_radius=50,
                            width=40,
                            height=40,
                        ),
                        ft.TextButton("www.cnn.com", url="https://edition.cnn.com/"),
                    ]
                ),
                ft.Row(
                    [
                        self.change_source_btn,
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def source_extensions(self):
        extensions = []
        for item in EXTENSIONS:
            extensions.append(ft.TextButton(item))
        column = ft.Column(
            [
                ft.Text("Latest"),
                ft.Row(extensions, scroll=ft.ScrollMode.ADAPTIVE, alignment=ft.alignment.top_left),
            ]
        )
        return ft.Container(column)

    def results(self):
        results = ft.ListView(expand=1, spacing=10, padding=20)
        for i in range(10):
            results.controls.append(
                ft.Container(
                    ft.Column(
                        [
                            ft.ResponsiveRow(
                                [
                                    ft.Image(IMAGES[i], width=150, height=150),
                                    ft.Column(
                                        [
                                            ft.Text(fake.text(), width=self.page.width),
                                            ft.Row(
                                                [
                                                    ft.Icon(ft.icons.ACCESS_TIME_FILLED_ROUNDED),
                                                    ft.Text(f"{i * 2 + 1}m ago"),
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
