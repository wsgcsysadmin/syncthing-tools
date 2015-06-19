# syncthing-tools
Supplemental tools for Syncthing

## set-st-bw
This is a bash script to modify the traffic shaping on a Syncthing server using the
REST API.  It was written for altering Syncthing's trafic shaping on a schedule using CRON.

### Requires
* jq - https://stedolan.github.io/jq/
* curl


### Configuration
A minimal configuation file:
```
URL=https://USER:PASS@backup-svr:8384
APIKEY="SUPERSECRET"
# Use if you are using self-signed certificates
#INSECURE=1
```
The defaul configuration location is hard coded in the script to /etc/syncthing/set-st-bw.cfg. Override it with the -c command line option.

### Usage
```
USAGE: ./set-st-bw -nv -c CONFIGFILE -d DOWN-RATE -u UP-RATE 
  -c Path to configuration file.
  -n Make no changes, only print the current settings.
  -d Set maxRecvKbps. Not required if -n is used.
  -u Set maxSendKbps. Not required if -n is used.
  -v Verbose output. Useful only for troubleshooting.
```
