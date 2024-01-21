import flet as ft

from queries import Query


class SourceEdit:
    def __init__(self, page: ft.Page, id: int) -> None:
        self.page = page
        self.source_id = id
        # make the query at init so the query is run just once
        self.source = Query().get_one_source(self.source_id)
        self.name_field = ft.TextField(label="Name", value=self.source.name)
        self.home_url_field = ft.TextField(label="Home URL", value=self.source.url)
        self.image_url_field = ft.TextField(label="Image URL", value=self.source.image_url)
        self.topics_column = ft.Column()

    def get_view(self):
        self.page.title = "Edit Source"
        return ft.View(f"/edit/{self.source_id}", self.view_build())

    def view_build(self):
        return [
            ft.Column(
                [
                    self.name_field,
                    self.home_url_field,
                    self.image_url_field,
                    ft.Divider(height=9, thickness=3),
                ]
            ),
            ft.ListView(
                [
                    self._topics_column,
                ],
                expand=1,
                height=200,
                auto_scroll=True,
            ),
            ft.Column(
                [
                    ft.ElevatedButton("Add", on_click=self.add_topic_row),
                    ft.ElevatedButton("Submit", on_click=self.submit),
                ]
            ),
        ]

    @property
    def _topics_column(self):
        for topic in self.source.topics:
            row = ft.Row(
                [
                    ft.TextField(label=f"Name", value=topic.name),
                    ft.TextField(label=f"URL", value=topic.url),
                ]
            )
            button = ft.TextButton("Remove", on_click=lambda _: ...)
            row.controls.append(button)
            self.topics_column.controls.append(row)

        return self.topics_column

    @property
    def new_topic_row(self):
        return ft.Row(
            [
                ft.TextField(label=f"Name"),
                ft.TextField(label=f"URL"),
            ]
        )

    def add_topic_row(self, _):
        new_row = self.new_topic_row
        remove_button = ft.TextButton("Remove")
        remove_button.on_click = lambda _: self.remove_new_topic_row(new_row)
        new_row.controls.append(remove_button)
        self.topics_column.controls.append(new_row)
        self.topics_column.update()

    def remove_new_topic_row(self, row):
        self.topics_column.controls.remove(row)
        self.topics_column.update()

    def submit(self, e):
        pass
