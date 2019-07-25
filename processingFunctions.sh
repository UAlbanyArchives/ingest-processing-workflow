# located in /etc/profile.d

ingest () {
    # function to call ingest.py under nohup

    args="$*"

    # set pyenv
    #pyenv activate ingest
    sudo nohup python3 /opt/lib/ingest-processing-workflow/ingest.py $args >> /media/SPE/ingest/"$1"-ingest.log 2>&1 &
    
    # deactivate pyenv
    #pyenv deactivate
}

transfer () {
    # function to call transferAccession.py under nohup

    args="$*"

    # set pyenv
    #pyenv activate ingest
    sudo nohup python3 /opt/lib/ingest-processing-workflow/transferAccession.py $args >> /media/SPE/ingest/"$1"-transfer.log 2>&1 &
    
    # deactivate pyenv
    #pyenv deactivate
}

ingestTest () {
    # function to call ingest.py under nohup

    args="$*"

    # set pyenv
    #pyenv activate ingest
    sudo python3 /opt/lib/ingest-processing-workflow/ingest.py $args &
    
    # deactivate pyenv
    #pyenv deactivate
}