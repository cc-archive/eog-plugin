import eog
import os
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
            # Seed with information from us.
            
            #license_value, web_statement_value, more_permissions_value, creator_value
            # FIXME: Python bindings only expose LL_LICENSE metadata
            for widget_id in self.metadata:
                widget = self.wTree.get_widget(widget_id)
		value = self.metadata[widget_id]
		if value is not None:
		    widget.set_text(value)
            # FIXME: Make back and next do something?
            self.dialog.show()

        def license2iconsbutton(self, license_uri):
            but = gtk.Button("")
            image = gtk.Image()
            image.set_from_file("/home/paulproteus/cc-work/liblicense/icons/scales.svg")
            # FIXME: Look up license, get picture!
            but.set_image(image)
            image.show()
            but.connect("clicked", self.show_license_info_dialog)
            return but
            
        def __init__(self):
                eog.Plugin.__init__(self)
                self.gladefile = os.path.join(
                    os.path.dirname(__file__), "licensing-properties-dialog.glade")
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
            self.metadata = {'license_value': liblicense.read(filename),
			     'more_permissions_value':
				 liblicense.read(filename, liblicense.LL_MORE_PERMISSIONS),
			     'creator_value':
				 liblicense.read(filename, liblicense.LL_CREATOR),
			     'web_statement_value':
				 liblicense.read(filename, liblicense.LL_WEBSTATEMENT)}

            # Get statusbar object
            statusbar = window.get_statusbar()
            but = self.license2iconsbutton('wtf')
            but.show()
            box = gtk.VBox()
            box.pack_end(but)
            statusbar.pack_end(box)
            box.show()

        
