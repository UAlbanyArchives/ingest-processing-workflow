# located in /etc/profile.d

ingest () {
    # function to call ingest.py in the background
    
    # set pyenv
    #pyenv activate ingest
    sudo -b python3 /opt/lib/ingest-processing-workflow/ingest.py "$@" >> /media/SPE/ingest/log/$(date +"%Y%m%d%H%M")-ingest-"$1".log 2>&1

    # deactivate pyenv
    #pyenv deactivate
}

transfer () {
    # function to call transferAccession.py in the background

    # set pyenv
    #pyenv activate ingest
    sudo -b python3 /opt/lib/ingest-processing-workflow/transferAccession.py "$@" >> /media/SPE/ingest/log/$(date +"%Y%m%d%H%M")-transfer-"$1".log 2>&1

    # deactivate pyenv
    #pyenv deactivate
}

packageAIP () {
    # function to call packageAIP.py in the background

    args="$*"
    colID="$(cut -d'_' -f1 <<<"$args")"
    
    # make log dir if it doesn't exist
    [[ -d /media/SPE/processing/log/"$colID" ]] || mkdir /media/SPE/processing/log/"$colID"

    # set pyenv
    #pyenv activate ingest
    sudo -b python3 /opt/lib/ingest-processing-workflow/packageAIP.py $args >> /media/SPE/processing/log/"$colID"/$(date +"%Y%m%d%H%M")-packageAIP-"$1".log 2>&1

    # deactivate pyenv
    #pyenv deactivate
}

check () {
    # function to call ingest.py in the background

    args="$*"
    ps aux | grep [${args:0:1}]${args:1}
    
}