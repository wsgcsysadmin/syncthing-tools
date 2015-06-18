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
```
The path to the config file is hardcoded in the script.

### Usage
```
/path/to/set-st-bw {download rate} {upload rate}
```
