# (c) 2009, 2011 Canonical Ltd.
# Author: Martin Owens <doctormo@ubuntu.com>
# License: GPL v2 or later
# Adopted for Fedora: Hedayat Vatankhah <hedayat.fwd@gmail.com>

from jockey.handlers import Handler, KernelModuleHandler

# dummy stub for xgettext
def _(x): return x

class BroadcomDriver(KernelModuleHandler):
    '''Handler for the Broadcom STA driver
    Just to provide a better name and description! 
    '''
    def __init__(self, ui):
        KernelModuleHandler.__init__(self, ui, 'wl',
            name=_('Broadcom 802.11 STA driver'),
            description=_('Broadcom 802.11 Linux STA Driver for WiFi cards.'),
            rationale=_('Broadcom 802.11 Linux STA Driver for WiFi, a linux'
               ' device driver for use with Broadcom\'s BCM4311-, BCM4312-,'
               ' BCM4321-, and BCM4322-based hardware.\n\n'))

