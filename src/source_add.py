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
        self.page.title = "Add Source"
        return ft.View("/add", self.view_build())

    def view_build(self):
        return [
            ft.Container(
                ft.Column(
                    [
                        ft.Column(
                            [
                                self.name_field,
                                self.home_url_field,
                                self.image_url_field,
                            ]
                        ),
                        ft.Divider(height=9, thickness=3),
                        self._topics_column,
                        ft.ElevatedButton("Add", on_click=self.add_topic_column),
                        ft.ElevatedButton("Submit", on_click=self.submit),
                    ]
                )
            )
        ]

    @property
    def topic_row(self):
        return ft.Row(
            [
                ft.TextField(label=f"Name"),
                ft.TextField(label=f"URL"),
            ]
        )

    @property
    def _topics_column(self):
        self.topics_column.controls.append(self.topic_row)
        return self.topics_column

    def add_topic_column(self, _):
        new_row = self.topic_row
        remove_button = ft.TextButton("Remove")
        remove_button.on_click = lambda _: self.remove_topic_column(new_row)
        new_row.controls.append(remove_button)
        self.topics_column.controls.append(new_row)
        self.topics_column.update()

    def remove_topic_column(self, row):
        self.topics_column.controls.remove(row)
        self.topics_column.update()

    def submit(self, _):
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
