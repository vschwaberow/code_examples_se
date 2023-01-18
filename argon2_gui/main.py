from nicegui import ui
from nicegui.events import ValueChangeEventArguments
import argon2


class Argon:
    def __init__(self):
        self.password = "volker"
        self.hash = ""
        self.time_cost = 3
        self.memory_cost = 65536
        self.parallelism = 4
        self.hash_length = 32
        self.salt_length = 16
        self.type = argon2.Type.D

    def generate_hash(self):
        try:
            self.password = str(self.password)
            self.time_cost = int(self.time_cost)
            self.memory_cost = int(self.memory_cost)
            self.parallelism = int(self.parallelism)
            self.hash_length = int(self.hash_length)

            self.hash = argon2.PasswordHasher(
                time_cost=self.time_cost,
                memory_cost=self.memory_cost,
                parallelism=self.parallelism,
                hash_len=self.hash_length,
                type=self.type,
            ).hash(self.password)
        except Exception as e:
            ui.notify("Error occured: " + str(e))

    def validate_hash(self):
        try:
            self.password = str(self.password)
            self.hash = str(self.hash)
            argon2.PasswordHasher().verify(self.hash, self.password)
            ui.notify("Hash is valid")
        except Exception as e:
            ui.notify("Error occured: " + str(e))

    def event_change_password(self, event: ValueChangeEventArguments):
        self.password = event.value


def main():

    style = "margin-top: 8px; margin-bottom: 8px; align-self: center;"
    row_style = "width: 800px; margin-top: 8px; margin-bottom: 8px; align-self: center;"

    argon = Argon()
    ui.label("Argon2 GUI").style(
        "font-weight: bold; font-size: 20px;align-self: center;")

    with ui.row().style(row_style):
        time_cost = ui.number("Time Cost", format='%d').bind_value(
            argon, 'time_cost').style(style + "width: 50%;")
        memory_cost = ui.number("Memory Cost", format='%d').bind_value(
            argon, 'memory_cost').style(style + "width: 40%;")
    with ui.row().style(row_style):
        parallelism = ui.number("Parallelism", format='%d').bind_value(
            argon, 'parallelism').style(style + "width: 50%;")
        hash_length = ui.number("Hash Length", format='%d').bind_value(
            argon, 'hash_length').style(style + "width: 40%;")
    with ui.row().style(row_style):
        salt_length = ui.number("Salt Length", format='%d').bind_value(
            argon, 'salt_length').style(style + "width: 50%;")
        ui.label("Type").style(style + "width: 10%;")
        type = ui.select({argon2.Type.D: 'argon2d', argon2.Type.I: 'argon2i', argon2.Type.ID: 'argon2id'}).bind_value(
            argon, 'type').style(style + "width: 30%;")

    with ui.row().style(row_style):
        ui.input("Password", on_change=argon.event_change_password).bind_value(
            argon, "password").style(style + "width: 98%;")
    with ui.row().style(row_style):
        ui.input("Generated Hash").bind_value(
            argon, "hash").style(style + "width: 98%;")

    with ui.row().style(row_style):
        ui.button("Generate Hash",
                  on_click=argon.generate_hash).style(style)
        ui.button("Validate Hash", on_click=argon.validate_hash).style(style)

    ui.run(title="Argon2 GUI", binding_refresh_interval=0.5)


if __name__ in {"__main__", "__mp_main__"}:
    main()
