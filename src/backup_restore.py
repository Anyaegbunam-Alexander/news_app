import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import flet as ft

from fields import TextField

WARNING_TEXT = """This emails the sources.db file to your email address.
    Essentially you email it to yourself.
    It might be safe; it might not.
    Just use with caution until I can find a better way to backup data.   
"""


class BackupRestore:
    def __init__(self, page: ft.Page) -> None:
        self.page = page
        self.email_field = TextField(label="Email address", col={"xs": 6})
        self.password_field = TextField(
            label="Password", col={"xs": 6}, password=True, can_reveal_password=True
        )

    def get_view(self):
        return ft.View(f"/backup", self.view_build())

    def view_build(self):
        self.page.title = "Backup Restore"
        return [
            ft.Text(""),
            ft.Container(
                ft.TextButton(
                    "Back to sources",
                    on_click=lambda _: self.page.go("/"),
                    icon=ft.icons.ARROW_BACK_IOS,
                )
            ),
            ft.Container(ft.TextButton("Restore Data", on_click=self.select_file)),
            ft.Divider(height=3, thickness=10),
            ft.Column(
                [
                    ft.Container(
                        ft.Column(
                            [
                                ft.ResponsiveRow([self.email_field, self.password_field]),
                                ft.TextButton("Backup", on_click=self.confirm_backup),
                            ]
                        )
                    )
                ]
            ),
        ]

    def send_email(self):
        gmail_user = self.email_field.validate_and_get_value()
        gmail_password = self.password_field.validate_and_get_value()
        if not gmail_password or not gmail_user:
            return

        body = "the backup"
        subject = "Backup"
        file_path = "sources.db"

        msg = MIMEMultipart()
        msg["From"] = gmail_user
        msg["To"] = gmail_user
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        # Open file in bynary mode
        binary_file = open(file_path, "rb")

        payload = MIMEBase("application", "octate-stream", Name=file_path)
        # To change the payload into encoded form
        payload.set_payload((binary_file).read())
        encoders.encode_base64(payload)

        # add payload header with pdf name
        payload.add_header("Content-Decomposition", "attachment", filename=file_path)
        msg.attach(payload)

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(gmail_user, gmail_password)
            text = msg.as_string()
            server.sendmail(gmail_user, gmail_user, text)
            server.quit()
        except Exception as e:
            server.quit()
            self.page.add(ft.Text(e, bgcolor=ft.colors.RED))
            self.page.update()

    def select_file(self, e: ft.FilePickerResultEvent):
        pass

    def confirm_restore(self, e):
        pass

    def confirm_backup(self, e):
        self.send_email()
        dlg = ft.AlertDialog(
            title=ft.Text("Sent!"),
            open=True
        )
        self.page.dialog = dlg
        self.page.update()
