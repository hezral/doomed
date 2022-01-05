# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText: 2021 Adi Hezral <hezral@gmail.com>

import sys
import os

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Granite', '1.0')
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gio, Granite, Gdk, GLib, Gst

from .window import doomedWindow
from .cpu_usage import CPUsage

import threading
import time

class Application(Gtk.Application):

    app_id = "com.github.hezral.doomed"
    image_count = 6
    previous_image_idx = None
    previous_cpu_load = None
    stop_thread = False

    def __init__(self):
        super().__init__(application_id=self.app_id,
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

        self.gio_settings = Gio.Settings(schema_id=self.app_id)
        self.gtk_settings = Gtk.Settings().get_default()
        self.granite_settings = Granite.Settings.get_default()

    def do_activate(self):
        self.window = self.props.active_window
        if not self.window:
            self.window = doomedWindow(application=self)
        self.window.present()
        self._run()

    def do_startup(self):
        Gtk.Application.do_startup(self)
        
        # Support quiting app using Super+Q
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit_action)
        self.add_action(quit_action)
        self.set_accels_for_action("app.quit", ["<Ctrl>Q", "Escape"])

        prefers_color_scheme = self.granite_settings.get_prefers_color_scheme()
        self.gtk_settings.set_property("gtk-application-prefer-dark-theme", prefers_color_scheme)
        self.granite_settings.connect("notify::prefers-color-scheme", self.on_prefers_color_scheme)

        if "io.elementary.stylesheet" not in self.gtk_settings.props.gtk_theme_name:
            self.gtk_settings.set_property("gtk-theme-name", "io.elementary.stylesheet.blueberry")

        # set CSS provider
        provider = Gtk.CssProvider()
        provider.load_from_path(os.path.join(os.path.dirname(__file__), "data", "application.css"))
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        # prepend custom path for icon theme
        icon_theme = Gtk.IconTheme.get_default()
        icon_theme.prepend_search_path(os.path.join(os.path.dirname(__file__), "data", "icons"))        

    def on_quit_action(self, action, param):
        if self.window is not None:
            self.window.on_close_window()

    def on_prefers_color_scheme(self, *args):
        prefers_color_scheme = self.granite_settings.get_prefers_color_scheme()
        self.gtk_settings.set_property("gtk-application-prefer-dark-theme", prefers_color_scheme)

    def on_update_timer(self):
        cpu_load = int(CPUsage(interval=0.2).result)
        image_idx = int(cpu_load / (100/(self.image_count-1)))

        if image_idx != self.previous_image_idx:
        	GLib.idle_add(self.window.image_stack.set_visible_child_name, str(image_idx))


        if cpu_load >= 90 and self.previous_cpu_load != cpu_load:
            self.play_unf()
            
        self.previous_image_idx = image_idx
        self.previous_cpu_load = cpu_load
        return True

    def _run(self):

        def init_manager():
            while True:  
                self.on_update_timer()
                if self.stop_thread:
                    break
                time.sleep(2)

        self.thread = threading.Thread(target=init_manager)
        self.thread.daemon = True
        self.thread.start()

    def play_unf(self):
        Gst.init(None)

        player = Gst.ElementFactory.make("playbin", "player")
        fakesink = Gst.ElementFactory.make("fakesink", "fakesink")
        player.set_property("video-sink", fakesink)

        unf_file = Gio.File.new_for_path(os.path.join(os.path.dirname(__file__), "data", "unf.mp3"))
        player.props.uri = unf_file.get_uri()

        player.set_state(Gst.State.PLAYING)

        bus = player.get_bus()
        bus.poll(Gst.MessageType.EOS, Gst.CLOCK_TIME_NONE)

        player.set_state(Gst.State.NULL)

        print("playing")


def main(version):
    app = Application()
    print(version)
    return app.run(sys.argv)
