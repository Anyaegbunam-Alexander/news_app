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
        self.query = Query()
        # make the query at init so the query is run just once
        self.source = self.query.get_one_source(self.source_id)

    def get_view(self):
        return ft.View(f"/sources/{self.source_id}", list(self.view_build()))

    def view_build(self):
        self.page.title = "Source News"
        return self.source_row(), self.source_topics(), self.source_results()

    def source_row(self):
        return ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Row(
                                [
                                    ft.Image(
                                        src=self.source.image_url,
                                        border_radius=50,
                                        width=40,
                                        height=40,
                                    ),
                                    ft.TextButton(self.source.name, url=self.source.url),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.TextButton(
                                        "Back",
                                        on_click=lambda _: self.page.go("/"),
                                        icon=ft.icons.ARROW_BACK_IOS,
                                    ),
                                ]
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Row(
                        [
                            ft.TextButton(
                                "Edit",
                                icon=ft.icons.EDIT_SHARP,
                                on_click=lambda _,: self.page.go(f"/edit/{self.source_id}"),
                            ),
                        ]
                    ),
                ]
            ),
            margin=ft.margin.only(top=10, bottom=5),
        )

    def source_topics(self):
        topics = []
        for topic in self.source.topics:
            # create the on_click function that gets the links form a topic
            on_click = lambda _, s_id=self.source_id, s_topic_name=topic.name: self.page.go(
                f"/sources/{s_id}?{s_topic_name}"
            )

            # focus the button of the current topic
            if topic.name == self.param:
                text_button = ft.TextButton(topic.name, on_click=on_click, autofocus=True)
            else:
                text_button = ft.TextButton(topic.name, on_click=on_click)

            topics.append(text_button)

        column = ft.Column(
            [
                ft.Text("Topics"),
                ft.Row(topics, scroll=ft.ScrollMode.ADAPTIVE, alignment=ft.alignment.top_left),
            ]
        )
        return ft.Container(column)

    def get_url(self):
        # get the url of the current topic.
        # this will work because every source must have one topic
        for topic in self.source.topics:
            if topic.name == self.param:
                break
        return topic.url

    def results(self):
        results = ft.ListView(
            expand=1, spacing=10, divider_thickness=3, padding=ft.padding.only(top=10)
        )
        content = BaseParser(url=self.get_url()).get_data()
        for data in content:
            results.controls.append(
                ft.Container(
                    ft.ResponsiveRow(
                        [
                            ft.Image(data.image_url, fit=ft.ImageFit.CONTAIN, col={"xs": 4}),
                            ft.Column(
                                [
                                    ft.Container(
                                        ft.Text(value=data.title),
                                        on_click=lambda _, link=data.link: self.page.launch_url(link)
                                    ),
                                    ft.Row(
                                        [
                                            ft.Icon(ft.icons.ACCESS_TIME_FILLED_ROUNDED),
                                            ft.Text(data.readable_date),
                                        ]
                                    ),
                                ],
                                col={"xs": 8},
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                )
            )
        return results

    def source_results(self):
        return self.results()
