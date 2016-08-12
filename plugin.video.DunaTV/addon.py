import os
import time
import urllib
import xbmc
import xbmcaddon
from BeautifulSoup import BeautifulSoup 

print "Starting..."

# setup
cs_url = "http://player.mediaklikk.hu/player/player-inside-full3.php?userid=mtva&streamid=dunalive"
cs_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25"
cs_name = xbmcaddon.Addon().getAddonInfo("id")
cs_file = os.path.join(xbmc.translatePath("special://temp"), cs_name + ".session")
cs_delay = 5

class CsatornakURLopener(urllib.FancyURLopener):
    version = cs_agent

print "Session: " + cs_file

# tries to limit deadlocks due to multiple runs
# fcntl for file locking may not be available on some platforms
if os.path.exists(cs_file) and time.time() - os.path.getmtime(cs_file) < cs_delay:
	print "Recently ran, exiting."
	sys.exit(0)
else:
	with open(cs_file, "a+"):
		os.utime(cs_file, None)

cs_player = xbmc.Player()

# stop playing and wait
cs_player.stop()
while cs_player.isPlaying():
	xbmc.sleep(10)
	
# load and parse stream	
print "Loading: " + cs_url

urllib._urlopener = CsatornakURLopener()
cs_page = urllib.urlopen(cs_url)
cs_soup = BeautifulSoup(cs_page.read())

cs_page.close()

cs_stream = cs_soup.source['src']

# play stream
print "Playing: " + cs_stream
cs_player.play(cs_stream)
print "Done."
