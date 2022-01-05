# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import gi
gi.require_version('Handy', '1')
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Handy, GdkPixbuf, Gdk

import os
resource_path = os.path.join(os.path.dirname(__file__), "data", "images")

class doomedWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'doomedWindow'

    Handy.init()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.app = self.props.application

        header = Handy.HeaderBar()
        header.props.show_close_button = True
        header.props.hexpand = True
        header.props.title = "doomed World"

        label = Gtk.Label("doomed World")
        label.props.expand = True
        label.props.valign = label.props.halign = Gtk.Align.CENTER

        image_0 = ImageContainer(os.path.join(resource_path, "0.png"), self.app)
        image_1 = ImageContainer(os.path.join(resource_path, "1.png"), self.app)
        image_2 = ImageContainer(os.path.join(resource_path, "2.png"), self.app)
        image_3 = ImageContainer(os.path.join(resource_path, "3.png"), self.app)
        image_4 = ImageContainer(os.path.join(resource_path, "4.png"), self.app)
        image_5 = ImageContainer(os.path.join(resource_path, "5.png"), self.app)

        self.image_stack = Gtk.Stack()
        self.image_stack.props.transition_type = Gtk.StackTransitionType.CROSSFADE
        self.image_stack.props.transition_duration = 100

        self.image_stack.add_named(image_0, "0")
        self.image_stack.add_named(image_1, "1")
        self.image_stack.add_named(image_2, "2")
        self.image_stack.add_named(image_3, "3")
        self.image_stack.add_named(image_4, "4")
        self.image_stack.add_named(image_5, "5")

        eventbox = Gtk.EventBox()
        eventbox.set_above_child(True)
        eventbox.add(self.image_stack)
        # eventbox.connect("button-press-event", self.on_button_pressed)

        self.grid = Gtk.Grid()
        self.grid.props.expand = True
        self.grid.get_style_context().add_class("transparent")
        self.grid.attach(eventbox, 0, 1, 1, 1)

        window_handle = Handy.WindowHandle() 
        window_handle.add(self.grid)

        self.add(window_handle)
        geometry = Gdk.Geometry()
        setattr(geometry, 'min_aspect', 1)
        setattr(geometry, 'max_aspect', 1)
        setattr(geometry, 'min_height', 32)
        setattr(geometry, 'min_width', 32)
        setattr(geometry, 'base_height', 64)
        setattr(geometry, 'base_width', 64)
        self.set_geometry_hints(None, geometry, Gdk.WindowHints.ASPECT | Gdk.WindowHints.MIN_SIZE | Gdk.WindowHints.BASE_SIZE)
        self.set_keep_above(True)
        self.get_style_context().add_class("transparent")
        
        self.move(self.app.gio_settings.get_int("pos-x"), self.app.gio_settings.get_int("pos-y"))
        self.set_size_request(32, 32)
        # self.set_size_request(self.app.gio_settings.get_int("window-height"), self.app.gio_settings.get_int("window-height"))

        self.show_all()
        self.connect("delete-event", self.on_close_window)
        

    def on_hover_enter(self, widget, eventcrossing):
        self.get_style_context().add_class("custom-decoration")
        self.get_style_context().add_class("custom-decoration-overlay")
        self.grid.get_style_context().remove_class("transparent")
        self.get_style_context().remove_class("transparent")

    def on_hover_leave(self, widget, eventcrossing):
        self.get_style_context().remove_class("custom-decoration")
        self.get_style_context().remove_class("custom-decoration-overlay")
        self.grid.get_style_context().add_class("transparent")
        self.get_style_context().add_class("transparent")

    def on_button_pressed(self, eventbox, eventbutton):
        if eventbutton.button == 1 and eventbutton.type.value_name == "GDK_BUTTON_PRESS":
            if self.get_style_context().has_class("transparent"):
                self.get_style_context().add_class("custom-decoration")
                self.get_style_context().add_class("custom-decoration-overlay")
                self.grid.get_style_context().remove_class("transparent")
                self.get_style_context().remove_class("transparent")
            else:
                self.get_style_context().remove_class("custom-decoration")
                self.get_style_context().remove_class("custom-decoration-overlay")
                self.grid.get_style_context().add_class("transparent")
                self.get_style_context().add_class("transparent")

    def setup_ui(self, transparency_value=None):
        css = "window#main.background {background-color: rgba(0,0,0," + str(transparency_value) + ");}"
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(bytes(css.encode()))
        self.get_style_context().add_provider(css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def on_close_window(self, window=None, event=None):
        width, height = self.get_size()
        x, y = self.get_position()

        self.app.gio_settings.set_int("pos-x", x)
        self.app.gio_settings.set_int("pos-y", y)
        self.app.gio_settings.set_int("window-height", height)
        self.app.gio_settings.set_int("window-width", width)
        self.destroy()
        return False

class ImageContainer(Gtk.Grid):

    alpha = False

    def __init__(self, filepath, app, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.app = app
        self.type = type
        self.filepath = filepath
        self.props.halign = self.props.valign = Gtk.Align.FILL
        self.props.can_focus = False
        self.props.name = "image-container"
        self.set_size_request(64, 64)
        # self.set_size_request(self.app.gio_settings.get_int("window-height"), self.app.gio_settings.get_int("window-height"))
        
        self.pixbuf_original = GdkPixbuf.Pixbuf.new_from_file(filepath)
        self.pixbuf_original_height = self.pixbuf_original.props.height
        self.pixbuf_original_width = self.pixbuf_original.props.width
        if self.pixbuf_original.get_has_alpha():
            self.alpha = True

        self.ratio_h_w = self.pixbuf_original_height / self.pixbuf_original_width
        self.ratio_w_h = self.pixbuf_original_width / self.pixbuf_original_height
    
        drawing_area = Gtk.DrawingArea()
        drawing_area.props.expand = True
        drawing_area.connect("draw", self.draw)
        drawing_area.props.can_focus = False
        drawing_area.get_style_context().add_class("dropshadow")
 
        self.attach(drawing_area, 0, 0, 1, 1)

    def draw(self, drawing_area, cairo_context):
        '''
        Forked and ported from https://github.com/elementary/greeter/blob/master/src/Widgets/BackgroundImage.vala
        '''
        from math import pi

        scale = self.get_scale_factor()
        width = self.get_allocated_width() * scale
        height = self.get_allocated_height() * scale

        pixbuf = self.pixbuf_original

        scaled_width = int(self.pixbuf_original_width * (width / self.pixbuf_original_width))
        scaled_height = int(self.pixbuf_original_height * (height / self.pixbuf_original_height))

        scaled_pixbuf = pixbuf.scale_simple(scaled_width, scaled_height, GdkPixbuf.InterpType.BILINEAR)

        final_pixbuf = scaled_pixbuf

        y = abs((height - final_pixbuf.props.height) / 2)
        x = abs((width - final_pixbuf.props.width) / 2)

        cairo_context.save()
        cairo_context.scale(1.0 / scale, 1.0 / scale)

        Gdk.cairo_set_source_pixbuf(cairo_context, final_pixbuf, x, y)

        cairo_context.paint()
        cairo_context.restore()