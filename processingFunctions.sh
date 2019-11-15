# located in /etc/profile.d

ingest () {
    # function to call ingest.py in the background

    args="$*"

    # set pyenv
    #pyenv activate ingest
    sudo -b python3 /opt/lib/ingest-processing-workflow/ingest.py $args >> /media/SPE/ingest/"$1"-ingest.log 2>&1
    
    # deactivate pyenv
    #pyenv deactivate
}

transfer () {
    # function to call transferAccession.py in the background

    args="$*"

    # set pyenv
    #pyenv activate ingest
    sudo -b python3 /opt/lib/ingest-processing-workflow/transferAccession.py $args >> /media/SPE/ingest/"$1"-transfer.log 2>&1
    
    # deactivate pyenv
    #pyenv deactivate
}

packageAIP () {
    # function to call packageAIP.py in the background

    args="$*"

    # set pyenv
    #pyenv activate ingest
    sudo -b python3 /opt/lib/ingest-processing-workflow/packageAIP.py $args >> /media/SPE/processing/"$1"-packageAIP.log 2>&1
    
    # deactivate pyenv
    #pyenv deactivate
}