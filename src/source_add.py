import flet as ft

from queries import Query


class SourceAdd:
    def __init__(self, page: ft.Page, id: int) -> None:
        self.page = page
        self.id = id
        self.name_field = ft.TextField(label="Name")
        self.home_url_field = ft.TextField(label="Home URL")
        self.image_url_field = ft.TextField(label="Image URL")
        self.topics_column = ft.Column()

    def get_view(self):
        """Returns the view"""
        self.page.title = "Add Source"
        return ft.View("/add", self.view_build())

    def view_build(self):
        """Returns the stack to be used for the view"""
        return [
            ft.Container(
                ft.TextButton(
                    "Back to sources",
                    icon=ft.icons.ARROW_BACK_IOS,
                    on_click=lambda _: self.page.go("/"),
                ),
                alignment=ft.alignment.top_right,
            ),
            ft.Container(
                ft.Text("Source details", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                margin=ft.margin.only(top=20, bottom=10),
            ),
            ft.Column(
                [
                    self.name_field,
                    self.home_url_field,
                    self.image_url_field,
                    ft.Divider(height=9, thickness=3),
                ]
            ),
            ft.Container(
                ft.Row(
                    [
                        ft.Text("Topics", theme_style=ft.TextThemeStyle.TITLE_MEDIUM),
                        ft.ElevatedButton(
                            "Add topic",
                            icon=ft.icons.ADD_CIRCLE_SHARP,
                            on_click=self.add_topic_row,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                margin=ft.margin.only(top=20, bottom=10),
            ),
            ft.ListView(
                [
                    self._topics_column,
                ],
                expand=1,
                height=200,
                auto_scroll=True,
                padding=ft.padding.only(top=10),
            ),
            ft.ElevatedButton(
                "Save", on_click=self.save, icon=ft.icons.SAVE, width=150, height=50
            ),
        ]

    @property
    def topic_row(self):
        """Returns an empty topic column which looks like a row"""
        return ft.Column(
            [
                ft.ResponsiveRow(
                    [
                        ft.TextField(label=f"Name", col={"md": 4}),
                        ft.TextField(label=f"URL", col={"md": 4}),
                    ],
                )
            ]
        )

    @property
    def _topics_column(self):
        """returns the topics_column with one topic_row and a divider appended to the row"""
        row = self.topic_row
        row.controls.append(ft.Divider(height=9, thickness=3))
        self.topics_column.controls.append(row)
        return self.topics_column

    def add_topic_row(self, _):
        """adds a new topic row to the `_topics_column`"""
        new_row = self.topic_row
        remove_button = ft.IconButton(
            icon=ft.icons.DELETE_FOREVER_ROUNDED, icon_color="pink600", col={"md": 1}
        )
        remove_button.on_click = lambda _: self.remove_topic_row(new_row)
        new_row.controls[0].controls.append(remove_button)
        new_row.controls[0].controls.append(ft.Divider(height=9, thickness=3))
        self.topics_column.controls.append(new_row)
        self.topics_column.update()

    def remove_topic_row(self, row):
        """removes a topic row from the `_topics_column`"""
        self.topics_column.controls.remove(row)
        self.topics_column.update()

    def save(self, _):
        """handles the saving of the entries"""
        topics = []
        data = {}
        data["name"] = self.name_field.value
        data["url"] = self.home_url_field.value
        data["image_url"] = self.image_url_field.value

        for row in self.topics_column.controls:
            name_field, url_field = row.controls
            topics.append({"name": name_field.value, "url": url_field.value})

        data["topics"] = topics

        source = Query().add_source(data)
        self.page.go(f"/sources/{source.id}?{topics[0]['name']}")
