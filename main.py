from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.core.image import Image as CoreImage
from kivy.properties import NumericProperty, ObjectProperty


class TileBG(Widget):
    texture = ObjectProperty(None)
    base_textures = []  # Holds multiple textures
    scale = NumericProperty(1.0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Load the tile texture and 4 different base textures
        self.texture = CoreImage("assets/tile.png").texture
        self.base_textures = [
            CoreImage("assets/academy.png").texture,
            CoreImage("assets/mindrack.png").texture,
            CoreImage("assets/library.png").texture,
            CoreImage("assets/base.png").texture,
        ]
        self.texture.wrap = "repeat"
        self.size_hint = (1, 1)

        # Bind size and position updates
        self.bind(size=self._redraw_tiles, pos=self._redraw_tiles)
        Window.bind(on_resize=self._handle_resize)

        # Initial scaling and rendering
        self._update_tile_scale()
        self._redraw_tiles()

    def _handle_resize(self, instance, width, height):
        self._update_tile_scale()

    def _update_tile_scale(self):
        if self.texture:
            window_scale = min(
                Window.width / self.texture.width,
                Window.height / self.texture.height,
            )
            self.scale = window_scale * 0.2

    def _redraw_tiles(self, *args):
        if not self.texture:
            return

        self.canvas.clear()
        with self.canvas:
            # Calculate tile dimensions
            tile_width = self.texture.width * self.scale
            tile_height = tile_width / 2
            repeat_x = self.width / tile_width
            repeat_y = self.height / tile_height

            # Draw tiled background
            Rectangle(
                pos=self.pos,
                size=self.size,
                texture=self.texture,
                tex_coords=(0, 0, repeat_x, 0, repeat_x, repeat_y, 0, repeat_y),
            )

            # Calculate base dimensions to fit within a tile
            base_width = tile_width
            base_height = (base_width / 2) * 1.15

            # Calculate center of the screen
            center_x = Window.width / 2
            center_y = Window.height / 2

            # Define diamond pattern positions for 4 bases
            positions = [
                (0, tile_height),  # Top
                (-tile_width, 0),  # Left
                (tile_width, 0),  # Right
                (0, -tile_height),  # Bottom
            ]

            # Draw the four different bases
            for i, (offset_x, offset_y) in enumerate(positions):
                base_x = center_x + offset_x - (base_width / 2)
                base_y = center_y + offset_y - (base_height / 2)

                Rectangle(
                    pos=(base_x, base_y),
                    size=(base_width, base_height),
                    texture=self.base_textures[i],  # Use corresponding texture
                )


class TileApp(App):
    def build(self):
        layout = FloatLayout()
        layout.add_widget(TileBG())
        return layout


if __name__ == "__main__":
    TileApp().run()
