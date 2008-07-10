import eog
import pprint
import gtk
import gtk.glade

def hide_true(widget):
    widget.hide()
    return True

class LicenseInfoDialog(gtk.Window):
    pass

class HelloWorldPlugin(eog.Plugin):
        _ui_str = '''
        <ui>
            <menubar name="MainMenu">
                <menu name="ToolsMenu" action="Tools">
                    <separator/>
                    <menuitem name="LicenseViewer" action="LicenseViewer"/>
                    <separator/>
                </menu>
            </menubar>
        </ui>'''

        def show_license_info_dialog(self, event):
            self.dialog.show()

        def license2iconsbutton(self, license_uri):
            but = gtk.Button("")
            image = gtk.Image()
            image.set_from_file("/home/paulproteus/gitted/liblicense/scales.svg")
            but.set_image(image)
            image.show()
            but.connect("clicked", self.show_license_info_dialog)
            return but
            
        def __init__(self):
                eog.Plugin.__init__(self)
                self.gladefile = "licensing-properties-dialog.glade"
                self.wTree = gtk.glade.XML(self.gladefile)
                self.dialog = self.wTree.get_widget("eog_image_properties_dialog")
                self.dialog.connect("destroy", lambda event, dummy: hide_true(self.dialog))
                self.dialog.connect("delete_event", lambda event, dummy: hide_true(self.dialog))

        def activate(self, window):
                ui_manager = window.get_ui_manager()
                group = gtk.ActionGroup('LicenseViewer')
                group.add_actions([('LicenseViewer', None, '_License Viewer',
                    None, None, self.console_cb)], window)
                ui_manager.insert_action_group(group, 0)
                ui_id = ui_manager.add_ui_from_string(self._ui_str)

                print 'The answer landed on my rooftop, whoa'

        def deactivate(self, window):
                print 'The answer fell off my rooftop, woot'

        def console_cb(self, action, window):
            image = window.get_image()
            if image is None:
                return # nothing to do
            filename = image.get_uri_for_display()
            try:
                import liblicense
            except ImportError:
                print 'You do not have liblicense.'
                return # get outta here
            license = liblicense.read(filename)
            if license is None:
                print 'The thing has no license.'
            else:
                print 'The thing has license', license
            # Get statusbar object
            statusbar = window.get_statusbar()
            but = self.license2iconsbutton('wtf')
            but.show()
            box = gtk.VBox()
            box.pack_end(but)
            statusbar.pack_end(box)
            box.show()

        
