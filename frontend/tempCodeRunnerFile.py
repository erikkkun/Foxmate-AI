 Route.SETTINGS: SettingsPage(
                on_menu=self.toggle_menu,
                on_settings=lambda: goto(Route.SETTINGS),
                on_close=self.close
            ),