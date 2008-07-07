import eog

class HelloWorldPlugin(eog.Plugin):
        def __init__(self):
                eog.Plugin.__init__(self)

        def activate(self, window):
                print 'The answer landed on my rooftop, whoa'

        def deactivate(self, window):
                print 'The answer fell off my rooftop, woot'

