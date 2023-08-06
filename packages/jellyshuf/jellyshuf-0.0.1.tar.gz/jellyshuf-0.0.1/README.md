# jellyshuf 
Essentially implements ncmpcpp's add random feature (default hotkey: `) through a script which grabs info from jellyfin api itself. 
jellyfin-mpd (and by proxy jellyfin-mopidy) does not implement the required mpd commands for this ncmpcpp function to work. 

# Install
`pip install jellyshuf` 
or 
```
git clone https://github.com/deafmute1/jellyshuf.git
pip install . 
```

# Usage
jellyshuf will asked for required information on first run (server url, username, password).
This info is stored to `$XDG_CONFIG_DIR/jellyshuf/user.json`
At the moment, the password is stored in plaintext in this file. In future, it will support use of keyrings.
`jellyshuf --help` 
```
USAGE: randjellympd <FLAGS> TYPE NUMBER
    
TYPE is one of artists, albums, songs (will take forever)
    
FLAGS: 
    --no-add  Instead of adding retrieved paths to mpd queue, emits them (line separated)
    --config  Run config (overwriting existing info if necessary) then exit
    --help    Display this message and exit
```
