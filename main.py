from scripts.ui import Home_UI,UI


ui = UI()
ui.create_window()
Home_UI(ui.window)

ui.window.mainloop()