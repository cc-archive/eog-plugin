import eog
import gtk

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
        def __init__(self):
                eog.Plugin.__init__(self)

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
            print "Calling me to work it out."
