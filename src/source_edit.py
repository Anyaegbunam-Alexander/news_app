import flet as ft

from fields import TextField
from queries import Query


class SourceEdit:
    def __init__(self, page: ft.Page, id: int) -> None:
        self.page = page
        self.source_id = id
        self.query = Query()
        # make the query at init so the query is run just once
        self.source = self.query.get_one_source(self.source_id)
        self.name_field = TextField(label="Name", value=self.source.name)
        self.home_url_field = TextField(label="Home URL", value=self.source.url)
        self.image_url_field = TextField(label="Image URL", value=self.source.image_url)
        self.existing_topics_column = ft.Column()
        self.new_topics_column = ft.Column()

    def get_view(self):
        """Returns the view"""
        self.page.title = "Edit Source"
        return ft.View(f"/edit/{self.source_id}", self.view_build())

    def back_to_source(self, e):
        self.query.rollback()
        self.page.go(f"/sources/{self.source_id}?{self.source.topics[0].name}")

    def view_build(self):
        """Returns the stack to be used for the view"""
        return [
            ft.Container(
                ft.TextButton(
                    "Back to source",
                    icon=ft.icons.ARROW_BACK_IOS,
                    on_click=self.back_to_source,
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
                            on_click=self.add_topic_row,
                            icon=ft.icons.ADD_CIRCLE_SHARP,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                margin=ft.margin.only(top=20, bottom=10),
            ),
            ft.ListView(
                [
                    self._existing_topics_column,
                    self.new_topics_column,
                ],
                expand=1,
                height=200,
                auto_scroll=True,
                padding=ft.padding.only(top=10, bottom=20),
            ),
            ft.ElevatedButton(
                "Save", on_click=self.save, icon=ft.icons.SAVE, width=150, height=50
            ),
        ]

    @property
    def _existing_topics_column(self):
        """returns columns which look like rows.
        These are prefilled with the values of `self.source.topics`.
        The number of column returned is dependent on `len(self.source.topics)`
        """
        for topic in self.source.topics:
            column = ft.Column()
            row = ft.ResponsiveRow(
                [
                    TextField(label=f"Name", value=topic.name, col={"md": 4}, id=topic.id),
                    TextField(label=f"URL", value=topic.url, col={"md": 4}, id=topic.id),
                ],
            )
            button = ft.IconButton(
                icon=ft.icons.DELETE_FOREVER_ROUNDED,
                icon_color="pink600",
                col={"md": 1},
                on_click=lambda _, id=topic.id, col=column: self.remove_existing_topic_row(
                    id, col
                ),
            )
            row.controls.append(button)
            column.controls.append(row)
            column.controls.append(ft.Divider(height=9, thickness=3))
            self.existing_topics_column.controls.append(column)

        return self.existing_topics_column

    @property
    def new_topic_row(self):
        """returns an empty responsive row"""
        return ft.ResponsiveRow(
            [
                TextField(label=f"Name", col={"md": 4}),
                TextField(label=f"URL", col={"md": 4}),
            ]
        )

    def add_topic_row(self, _):
        """adds an empty column with a divider and a button to `self.topics_column`"""
        column = ft.Column()
        new_row = self.new_topic_row
        remove_button = ft.IconButton(
            icon=ft.icons.DELETE_FOREVER_ROUNDED, icon_color="pink600", col={"md": 1}
        )
        remove_button.on_click = lambda _: self.remove_new_topic_row(column)
        new_row.controls.append(remove_button)
        column.controls.append(new_row)
        column.controls.append(ft.Divider(height=9, thickness=3))
        self.new_topics_column.controls.append(column)
        self.new_topics_column.update()

    def remove_new_topic_row(self, row):
        """removes only a user-added column from `self.topics_column`.
        Removal of prefilled columns is handled by another method."""
        self.new_topics_column.controls.remove(row)
        self.new_topics_column.update()

    def remove_existing_topic_row(self, id, row):
        if len(self.existing_topics_column.controls) > 1:
            self.query.delete_topic(id)
            self.existing_topics_column.controls.remove(row)
            self.existing_topics_column.update()
        else:
            return

    def get_topic_fields(self, col: ft.Column, id=False):
        topics = []

        # get the columns in topics_column.controls
        for column in col.controls:
            # get the rows in column.controls
            for row in column.controls:
                # since there are widgets other than TextFields
                # in the column, check if it is a TextField and if not pass
                if isinstance(row, (ft.ResponsiveRow, ft.Row)):
                    # In the row, the first two are always TextFields. Get these
                    name_field, url_field = row.controls[:2]
                    # validate the values and if they pass append the dictionary to the topics list
                    if not (name_field.validate_has_text() and url_field.validate_is_url()):
                        return None

                    topic = {"name": name_field.value, "url": url_field.value}
                    if id:
                        topic["id"] = name_field.id
                    
                    topics.append(topic)

        return topics

    def save(self, e):
        """handles the saving of the entries"""
        data = {
            "name": self.name_field.validate_and_get_value(),
            "url": self.home_url_field.validate_and_get_value(type=self.home_url_field.URL),
            "image_url": self.image_url_field.validate_and_get_value(
                type=self.image_url_field.URL
            ),
            "id": self.source.id
        }

        if None in data.values():
            return

        new_topics = self.get_topic_fields(self.new_topics_column)
        existing_topics = self.get_topic_fields(self.existing_topics_column, id=True)

        data["new_topics"] = new_topics
        data["existing_topics"] = existing_topics
        self.query.update_source_and_topics(data, self.source.id)
        self.query.save()
        self.page.go(f"/sources/{self.source_id}?{self.source.topics[0].name}")
