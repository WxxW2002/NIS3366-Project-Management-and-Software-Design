# theme.py
class Theme:
    def __init__(self, color=None, background_image=None):
        self.color = color if color else "default"
        self.background_image = background_image if background_image else None

    def set_color(self, color):
        """Set the theme color."""
        self.color = color

    def set_background_image(self, background_image):
        """Set the theme background image."""
        self.background_image = background_image

    def get_style_sheet(self):
        return f"background-image: url({self.background_image});"
