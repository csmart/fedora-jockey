# (c) 2009, 2011 Canonical Ltd.
# Author: Martin Owens <doctormo@ubuntu.com>
# License: GPL v2 or later
# Adopted for Fedora: Hedayat Vatankhah <hedayat.fwd@gmail.com>

from jockey.handlers import Handler, KernelModuleHandler

# dummy stub for xgettext
def _(x): return x

class VmwareClientHandler(KernelModuleHandler):
    '''Handler for the VMWARE client tools.
    '''
    def __init__(self, ui):
        KernelModuleHandler.__init__(self, ui, 'vmxnet',
                name=_('VMWare Client Tools'),
                description=_('Install VMWare client drivers and tools'),
                rationale=_('Install the VMWare client drivers'
                    'for your VMWare based Fedora/Parsidora installation.\n\n'
                    'This should help you use Fedora/Parsidora in your VM.'))

    def id(self):
        '''Return an unique identifier of the handler.'''
        return 'vm:' + self.module

