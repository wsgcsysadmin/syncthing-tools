#!/usr/bin/python

# Copyright 2015 Williamson Street Grocery Cooperative
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License version 3 as published by the Free
# Software Foundation.
#

from __future__ import print_function


from pprint import pprint
import os
import os.path
import sys
from optparse import OptionParser
import ConfigParser
import requests
if requests.__version__ >= '2.4':
  import requests.packages.urllib3
import json

def get_st_config(url,credentials,verify_cert,apikey):
  r = requests.get(url+'/rest/system/config',verify=verify_cert,
    auth=credentials,
    headers={'X-API-Key': apikey})
  if r.status_code != 200:
    bail("Unable to retrieve config. "+r.text+"\nHTTP response code: " + str(r.status_code))
  return json.loads(r.text)

def set_max_recv(config,max_recv):
  config['options']['maxRecvKbps'] = int(max_recv)
  return config

def set_max_send(config,max_send):
  config['options']['maxSendKbps'] = int(max_send)
  return config

def put_st_config(url,credentials,verify_cert,config,apikey):
  r = requests.post(url+'/rest/system/config',verify=verify_cert,
    auth=credentials,
    headers={'X-API-Key': apikey} , data=json.dumps(config))
  if r.status_code != 200:
    bail("Unable to update config. "+r.text+"\nHTTP response code: " + str(r.status_code))

def restart_st(url,credentials,verify_cert,apikey):
  r = requests.post(url+'/rest/system/restart',verify=verify_cert,
    auth=credentials,
    headers={'X-API-Key': apikey} , data='')
  if r.status_code != 200:
    bail("Unable to restart Syncthing. "+r.text+"\nHTTP response code: " + str(r.status_code))




def bail(msg):
  print(msg, file=sys.stderr)
  exit( 1 )


def main():

  parser = OptionParser(usage="%prog [-e] [-c CONFIGFILE] [-x SECTION]  [-n] [-r MAX_RECV] [-s MAX_SEND]")
  parser.add_option("-x", "--conf-section", action="store", dest="section",help="Name of the configuration section to use for connection parameters.",default="localhost")
  parser.add_option("-c", "--config-file", action="store", dest="config_path",help="Path to configuration file.",default="/etc/syncthing/set-st-bw.conf")
  parser.add_option("-n", "--no-change", action="store_true", dest="no_change",help="Make no changes, only print the current settings.")
  parser.add_option("-e", "--restart", action="store_true", dest="restart",help="Restart Syncthing after changes have been made. For Syncthing < v0.14.19.")
  parser.add_option("-r", "--max-recv", action="store", dest="max_recv",help="Set maxRecvKbps. Not required if -n is used.")
  parser.add_option("-s", "--max-send", action="store", dest="max_send",help="Set maxSendKbps. Not required if -n is used.")
  #parser.add_option("-v", "--verbose", action="count", dest="verbose",help="Verbose output. Use more than once for more noise.")
  (options, args) = parser.parse_args()

  if not options.no_change and ( options.max_recv is None and  options.max_send is None):
    parser.error("The -s and/or -r options are required unless -n is used.")

  if not os.path.exists( options.config_path ):
    bail("Config file does not exist")
  if not os.access( options.config_path, os.R_OK):
    bail("Unable to read config file. Permissions? ")

  config = ConfigParser.RawConfigParser({'insecure':0,'username':'','password':''})
  config.read(options.config_path)

  if not config.has_section(options.section):
    bail("There is no section in the configuration named '"+options.section+"'")

  url = config.get( options.section, 'url')
  username = config.get( options.section, 'username')
  password = config.get( options.section, 'password')
  creds = (username,password)
  apikey = config.get(options.section, 'apikey')

  if config.get(options.section, 'insecure' )=='True':
    verify_cert = False
    if requests.__version__ >= '2.4':
      requests.packages.urllib3.disable_warnings()
  else:
    verify_cert = True

  config = get_st_config( url,creds,verify_cert,apikey)

  if options.no_change:
    print( 'maxSendKbps: '+ str(config['options']['maxSendKbps']) )
    print( 'maxRecvKbps: '+ str(config['options']['maxRecvKbps']) )
  else:
    if options.max_recv is not None:
      config = set_max_recv(config,options.max_recv)
    if options.max_send is not None:
      config = set_max_send(config,options.max_send)
    put_st_config(url,creds,verify_cert,config,apikey)
    if options.restart:
      restart_st(url, creds, verify_cert, apikey)

if __name__ == "__main__":
    main()
