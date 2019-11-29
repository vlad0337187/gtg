from gi.repository import Clutter
import champlain


class MarkerLayer(champlain.Layer):

    def __init__(self):
        super().__init__()
        # a marker can also be set in RGB with ints
        self.gray = Clutter.Color(51, 51, 51)

        # RGBA
        self.white = Clutter.Color(0xff, 0xff, 0xff, 0xff)
        self.black = Clutter.Color(0x00, 0x00, 0x00, 0xff)

        self.hide()

    def add_marker(self, text, latitude, longitude, bg_color=None,
                   text_color=None, font="Airmole 8"):
        if not text_color:
            text_color = self.white

        if not bg_color:
            bg_color = self.gray

        marker = champlain.marker_new_with_text(text, font, text_color,
                                                bg_color)

        # marker.set_position(38.575935, -7.921326)
        if latitude and longitude:
            marker.set_position(latitude, longitude)
        self.add(marker)
        return marker
