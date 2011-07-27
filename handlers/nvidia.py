# (c) 2009, 2011 Canonical Ltd.
# Author: Martin Owens <doctormo@ubuntu.com>
# License: GPL v2 or later
# Adopted for Fedora: Hedayat Vatankhah <hedayat.fwd@gmail.com>

from jockey.handlers import Handler, KernelModuleHandler

# dummy stub for xgettext
def _(x): return x

class NvidiaDriver(KernelModuleHandler):
    '''Handler for the NVidia graphic cards
    Just to provide a better name and description! 
    '''
    def __init__(self, ui):
        self._recommended = "kmod-nvidia"
        KernelModuleHandler.__init__(self, ui, 'nvidia',
            name=_('NVIDIA accelerated graphics driver'),
            description=_('3D-accelerated proprietary graphics driver for '
                'NVIDIA cards.'),
            rationale=_('This driver is required to fully utilise '
                'the 3D potential of NVIDIA graphics cards, as well as provide '
                '2D acceleration of newer cards.\n\n'
                'If you wish to enable desktop effects, this driver is '
                'required.\n\n'
                'If this driver is not enabled, you will not be able to '
                'enable desktop effects and will not be able to run software '
                'that requires 3D acceleration, such as some games.'))

    def id(self):
        '''Return an unique identifier of the handler.'''
        return 'vm:' + self.module
