#!/usr/bin/python
import sys
import os
from subprocess import *
import time
import socket

import sys
import os
from subprocess import *
import time
import socket

pathname = os.path.dirname(sys.argv[0])
path = os.path.abspath(pathname)
contentPath = "/var/www"

#Check if content path already exists and has the right version
if not os.path.exists(contentPath):
        print "Copying content"
        #os.mkdir(contentPath)
        #Copy content to /Library/WebServer/Documents/unCloudServer
        call(["cp -r %s/content %s"%(path, contentPath)], shell=True)
        time.sleep(2)
        call(["chmod -R 777 %s"%contentPath], shell=True)
else:
    print "Content exists, checking version"
    if os.path.exists("%s/version.txt"%contentPath):
        systemVersionFile = open("%s/version.txt"%contentPath, "r")
        installVersionFile = open("%s/content/version.txt"%path, "r")
        if systemVersionFile.read() != installVersionFile.read():
            print "Copying content, versions did not match."
            call("rm -r %s"%contentPath, shell=True)
            os.mkdir(contentPath)
            #Copy content to /Library/WebServer/Documents/unCloudServer
            call(["cp -r %s/content/ %s"%(path, contentPath)], shell=True)
            time.sleep(2)
            call(["chmod -R 777 %s"%contentPath], shell=True)
        else:
            print "versions match."
    else:
        print "Copying content, no version file found. Deleting %s"%contentPath
        call("rm -r %s"%contentPath, shell=True)
        os.mkdir(contentPath)
        #Copy content to /Library/WebServer/Documents/unCloudServer
        call(["cp -r %s/content/ %s"%(path, contentPath)], shell=True)
        time.sleep(2)
        call(["chmod -R 777 %s"%contentPath], shell=True)


#Generate the config file from the template
apacheConfigTemplate = open("%s/unCloudTemplate.conf"%path, "r")
configText = apacheConfigTemplate.read().replace("UNCLOUDPATH", contentPath)
apacheConfigTemplate.close()
apacheConfig = open("%s/unCloudServer.conf"%path, "w")
apacheConfig.write(configText)
apacheConfig.close()

#Stop Apache
call(["apachectl stop"], shell=True)
#Hard kill the apache process to make sure it's really gone
call(["pkill apache2"],shell=True)
#give some time for the apache to end
time.sleep(2)
#Start Apache with our config file
call(["apachectl -f %s/unCloudServer.conf"%path], shell=True)
