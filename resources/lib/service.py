# -*- coding: utf-8 -*-

import sys
import logging
from threading import Event

import xbmc
import xbmcaddon
from xbmcgui import NOTIFICATION_ERROR,NOTIFICATION_WARNING, NOTIFICATION_INFO


#from resources.lib.qhue import Bridge
from resources.lib import kodiutils
from resources.lib.KodiGroup import KodiGroup
from resources.lib import kodiHue                                                                                                                                                          
from resources.lib import qhue


__addon__ = xbmcaddon.Addon()
__addondir__ = xbmc.translatePath(__addon__.getAddonInfo('profile'))
__cwd__ = __addon__.getAddonInfo('path')

from resources.lib.tools import get_version


ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))


logger.debug("Kodi Hue: In .(argv={}) service started, version: {}, SYSPATH: {}".format(
    sys.argv, get_version(), sys.path))

ev = Event()
capture = xbmc.RenderCapture()
fmt = capture.getImageFormat()
# BGRA or RGBA
fmtRGBA = fmt == 'RGBA'



##################################################
## RUN
###################
def run():
    logger.debug("Kodi Hue:  service started, version: {}".format(ADDON.getAddonInfo('version')))

    args = None
    if len(sys.argv) == 2:
        args = sys.argv[1]

    logger.debug("Kodi Hue: Args: {}".format(args))
    
    bridgeIP = ""
    bridgeUser = ""

    
    ev = Event()
    capture = xbmc.RenderCapture()
    fmt = capture.getImageFormat()
    # BGRA or RGBA
    fmtRGBA = fmt == 'RGBA'
    global connected
    connected = False
    
    
    #monitor = MyMonitor(settings)
    monitor=xbmc.Monitor()

    
###########################################################
########################################################### 
########################################################### 
###########################################################     



    if args == "discover":
        logger.debug("Kodi Hue: Discovery selected, don't load existing bridge settings.")
        bridge = kodiHue.initialConnect(monitor, True)
    else:
        bridge = kodiHue.initialConnect(monitor, False)

    
    if bridge:
        #got a bridge, do main script
        connected=True
        
        groups=bridge.groups
        lights=bridge.lights
        testgroup=bridge.groups["4"]
        
        
        logger.debug("Kodi Hue: Initial test flash")
        
        #bridge.groups['9'].action(alert="select")
        
        testgroup.action(alert="select")

        
        
        player = xbmc.Player 
        kgroup0=KodiGroup()
        kgroup0.setup(bridge,0,4) #kodigroup 0, huetestgroup =9
    
        

        ##Ready to go! Start running until Kodi exit.
        while connected and not monitor.abortRequested():
            logger.debug('Kodi Hue: Script waiting...')
            #TODO: restart script on Monitor.onSettingsChanged 
            ####Wait for abort
            xbmc.sleep(10000)
            
        return
        logger.debug('Kodi Hue: Process exiting...')
        #### End of script
        
    else:
        logger.debug('Kodi Hue: No bridge, exiting...')
        return
        
    
    #===========================================================================
    # if bridgeIP and bridgeUser:
    #     if kodiHue.userTest(bridgeIP, bridgeUser):
    #         bridge = qhue.Bridge(bridgeIP,bridgeUser)
    #         connected = True
    #         kodiutils.notification("Kodi Hue", "Bridge connected", time=5000, icon=NOTIFICATION_INFO, sound=False)
    #         logger.debug("Kodi Hue: Connected!")
    #  
    #     else:
    #         bridge = kodiHue.initialSetup(monitor)
    #         if not bridge:
    #             logger.debug("Kodi Hue: Connection failed, exiting script")
    #             kodiutils.notification("Kodi Hue", "Bridge not found, check your network", time=5000, icon=NOTIFICATION_ERROR, sound=True)
    #             return #exit run()
    #     
    # else:
    #     bridge = kodiHue.initialSetup(monitor)    
    #     if not bridge:
    #         logger.debug("Kodi Hue: Connection failed, exiting script")
    #         kodiutils.notification("Kodi Hue", "Bridge not found, check your network", time=5000, icon=NOTIFICATION_ERROR, sound=True)
    #         return #exit run()
    # 
    #===========================================================================
    
    #### Bridge is ready, lets GO
 
    
##########################################################################################################################################    





