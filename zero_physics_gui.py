import sys
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib

class ZeroPhysics(Gtk.Window):
    def __init__(self):
        super().__init__(title="Zero Physics - Ultimate Studio")
        self.set_default_size(1200, 800)
        
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = ""
        self.header.get_style_context().add_class("hidden-header")
        self.set_titlebar(self.header)
        
        self.setup_css()
        
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(main_box)
        
        # ================= TOOLBAR (Properties) =================
        self.sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.sidebar.set_size_request(300, -1)
        self.sidebar.get_style_context().add_class("sidebar")
        main_box.pack_start(self.sidebar, False, False, 0)
        
        logo = Gtk.Label(label="Z E R O P H Y S I C S")
        logo.get_style_context().add_class("sidebar-logo")
        logo.set_margin_top(20)
        logo.set_margin_bottom(20)
        self.sidebar.pack_start(logo, False, False, 0)
        
        lbl_props = Gtk.Label(label="ENVIRONMENT")
        lbl_props.get_style_context().add_class("section-label")
        lbl_props.set_halign(Gtk.Align.START)
        lbl_props.set_margin_start(20)
        self.sidebar.pack_start(lbl_props, False, False, 0)
        
        props = [
            ("Gravity (m/s²)", "-9.81"),
            ("Air Resistance", "0.01"),
            ("Time Scale", "1.0x"),
            ("Collision Quality", "Ultra")
        ]
        
        for name, default in props:
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            box.set_margin_start(20)
            box.set_margin_end(20)
            
            lbl = Gtk.Label(label=name)
            lbl.set_halign(Gtk.Align.START)
            lbl.get_style_context().add_class("prop-lbl")
            
            entry = Gtk.Entry()
            entry.set_text(default)
            entry.get_style_context().add_class("prop-entry")
            
            box.pack_start(lbl, False, False, 5)
            box.pack_start(entry, False, False, 0)
            self.sidebar.pack_start(box, False, False, 0)
            
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_box.set_margin_start(20)
        btn_box.set_margin_end(20)
        btn_box.set_margin_top(20)
        
        btn_reset = Gtk.Button(label="Reset")
        btn_reset.get_style_context().add_class("nav-btn")
        btn_apply = Gtk.Button(label="Apply")
        btn_apply.get_style_context().add_class("action-btn")
        
        btn_box.pack_start(btn_reset, True, True, 0)
        btn_box.pack_start(btn_apply, True, True, 0)
        self.sidebar.pack_start(btn_box, False, False, 0)
        
        # ================= ENGINE VIEW =================
        self.engine_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.engine_box.get_style_context().add_class("engine-box")
        main_box.pack_start(self.engine_box, True, True, 0)
        
        canvas_box = Gtk.Box()
        canvas_box.get_style_context().add_class("canvas")
        
        lbl_engine = Gtk.Label(label="3D Physics Engine Initialized.\nAwaiting Simulation Start.")
        lbl_engine.set_justify(Gtk.Justification.CENTER)
        lbl_engine.get_style_context().add_class("engine-text")
        canvas_box.pack_start(lbl_engine, True, True, 0)
        
        self.engine_box.pack_start(canvas_box, True, True, 20)
        
        # Timeline Controls
        controls = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
        controls.set_halign(Gtk.Align.CENTER)
        controls.set_margin_bottom(20)
        
        for c in ["⏪", "▶", "⏸", "⏩"]:
            b = Gtk.Button(label=c)
            b.get_style_context().add_class("ctrl-btn")
            controls.pack_start(b, False, False, 0)
            
        self.engine_box.pack_start(controls, False, False, 0)
        
    def setup_css(self):
        css = b'''
            window { background-color: #030305; }
            .hidden-header { background: #030305; min-height: 0px; padding: 0px; border: none; box-shadow: none; }
            .sidebar { background-color: rgba(6, 8, 12, 0.98); border-right: 1px solid rgba(255, 255, 255, 0.05); }
            .sidebar-logo { color: #FFFFFF; font-size: 18px; font-weight: 900; letter-spacing: 4px; text-shadow: 0 0 15px rgba(255, 0, 102, 0.6); }
            .section-label { color: #4A5568; font-size: 11px; font-weight: 900; letter-spacing: 2px; }
            .prop-lbl { color: #8B94A5; font-size: 13px; font-weight: bold; }
            .prop-entry { background: #0A0D14; color: #FFFFFF; border: 1px solid #1C2333; border-radius: 8px; padding: 8px; caret-color: #FF0066; }
            .prop-entry:focus { border: 1px solid #FF0066; box-shadow: 0 0 10px rgba(255, 0, 102, 0.3); }
            .nav-btn { background: rgba(255,255,255,0.05); color: #FFFFFF; border-radius: 8px; border: none; padding: 10px; font-weight: bold; transition: all 0.2s; }
            .nav-btn:hover { background: rgba(255,255,255,0.1); }
            .action-btn { background: linear-gradient(45deg, #FF0066, #CC0052); color: #FFFFFF; border-radius: 8px; font-weight: bold; padding: 10px; border: none; box-shadow: 0 5px 15px rgba(255, 0, 102, 0.3); transition: all 0.3s; }
            .action-btn:hover { box-shadow: 0 8px 25px rgba(255, 0, 102, 0.5); }
            .engine-box { background: radial-gradient(circle at center, #10141E, #030305); }
            .canvas { background: #000000; border: 1px solid #1C2333; border-radius: 20px; box-shadow: inset 0 0 50px rgba(255, 0, 102, 0.1); margin: 20px; }
            .engine-text { color: #FF0066; font-size: 24px; font-weight: 200; font-family: monospace; opacity: 0.7; }
            .ctrl-btn { background: #0A0D14; color: #FFFFFF; font-size: 24px; border-radius: 50%; padding: 15px; border: 1px solid #1C2333; transition: all 0.2s; }
            .ctrl-btn:hover { background: #1C2333; color: #FF0066; border: 1px solid #FF0066; box-shadow: 0 0 20px rgba(255, 0, 102, 0.3); transform: scale(1.1); }
        '''
        provider = Gtk.CssProvider()
        provider.load_from_data(css)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

if __name__ == "__main__":
    win = ZeroPhysics()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
