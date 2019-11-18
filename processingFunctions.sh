# located in /etc/profile.d

ingest () {
    # function to call ingest.py in the background

    args="$*"
    colID="$(cut -d'_' -f1 <<<"$args")"
    
    # make log dir if it doesn't exist
    [[ -d /media/SPE/ingest/log/"$colID" ]] || mkdir /media/SPE/ingest/log/"$colID"

    # set pyenv
    #pyenv activate ingest
    sudo -b python3 /opt/lib/ingest-processing-workflow/ingest.py $args >> /media/SPE/ingest/ingest-"$1".log 2>&1

    # deactivate pyenv
    #pyenv deactivate
}

transfer () {
    # function to call transferAccession.py in the background

    args="$*"
    colID="$(cut -d'_' -f1 <<<"$args")"
    
    # make log dir if it doesn't exist
    [[ -d /media/SPE/ingest/log/"$colID" ]] || mkdir /media/SPE/ingest/log/"$colID"

    # set pyenv
    #pyenv activate ingest
    sudo -b python3 /opt/lib/ingest-processing-workflow/transferAccession.py $args >> /media/SPE/ingest/transfer-"$1".log 2>&1

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
    sudo -b python3 /opt/lib/ingest-processing-workflow/packageAIP.py $args >> /media/SPE/processing/log/packageAIP-"$1".log 2>&1

    # deactivate pyenv
    #pyenv deactivate
}