# -*- coding: utf-8 -*-

import sys
import logging
from threading import Event

import xbmc
import xbmcaddon
from xbmcgui import NOTIFICATION_ERROR, NOTIFICATION_WARNING, NOTIFICATION_INFO

# from resources.lib.qhue import Bridge
import globals
import kodiutils
from KodiGroup import KodiGroup
import kodiHue                                                                                                                                                          
import qhue
from resources.lib.globals import NUM_GROUPS



ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))

connected = False
settingsChanged = False



#===============================================================================
# ev = Event()
# capture = xbmc.RenderCapture()
# fmt = capture.getImageFormat()
# # BGRA or RGBA
# fmtRGBA = fmt == 'RGBA'
#===============================================================================

##################################################
# # RUN
###################
def run():
    logger.debug("Kodi Hue:  service started, version: {}".format(ADDON.getAddonInfo('version')))
    
    #global settingsChanged
    #global connected
    
    monitor = kodiHue.HueMonitor()
    

    initialFlash = kodiutils.get_setting_as_bool("initialFlash")
    
    
    bridgeIP = ""
    bridgeUser = ""

    if len(sys.argv) == 2:
        args = sys.argv[1]
    else: 
        args = ""
    
    logger.debug("Kodi Hue: Args: {}".format(args))
    
###########################################################
########################################################### 
########################################################### 
###########################################################     
    
    if args == "discover":
        logger.debug("Kodi Hue: Started with Discovery")
        bridge = kodiHue.initialConnect(monitor, True)

    elif args.startswith("groupSelect"):
        
        kgroup = args.split("=", 1)[1]
        logger.debug("Kodi Hue: Started with groupSelect. args: {}, kgroup: {}".format(args, kgroup))
        
        bridge = kodiHue.initialConnect(monitor, False, True)  # don't rediscover, proceed silently
        if bridge:
            kodiHue.configureGroup(bridge, kgroup)
        else:
            logger.debug("Kodi Hue: No bridge found. Select group cancelled.")
            
    else:
        # no arguments, proceed as normal.
        logger.debug("Kodi Hue: Started with no arguments")
        bridge = kodiHue.initialConnect(monitor)
        
    
        if bridge:
            # got a bridge, do main script
            globals.connected = True
            globals.settingsChanged = False
            
            daylight = kodiHue.getDaylight(bridge)
            
            
            
            ## Initialize kodi groups
            kgroups= [] 
            g=0
            while g < NUM_GROUPS:
                kgroups.append(KodiGroup())
                kgroups[g].setup(bridge, g, kodiutils.get_setting_as_int("group{}_hGroupID".format(g))) 
                g = g + 1
                
                
            #for g in kgroups:
            #    kgroups[g].setup(bridge, g, kodiutils.get_setting_as_int("group{}_hGroupID".format(g)))                #kgroups.append(KodiGroup())
            #kgroup0 = KodiGroup()
            #kgroup1 = KodiGroup()
            #kgroup0.setup(bridge, 0, kodiutils.get_setting_as_int("group{}_hGroupID".format(0)))
            #kgroup1.setup(bridge, 1, kodiutils.get_setting_as_int("group{}_hGroupID".format(1)))
    
            # #Ready to go! Start running until Kodi exit.
            while globals.connected and not monitor.abortRequested():
                logger.debug('Kodi Hue: Service running...')
                if globals.settingsChanged:
                    kgroups = kodiHue.reloadGroups(bridge,kgroups)
                    globals.settingsChanged = False
                    

                
                monitor.waitForAbort(10)
                
                
            
            logger.debug('Kodi Hue: Process exiting...')
            
            return
            #### End of script
            
        else:
            logger.debug('Kodi Hue: No bridge, exiting...')
            return
    

