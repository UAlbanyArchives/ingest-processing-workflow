# located in /etc/profile.d

ingest () {
    # function to call ingest.py under nohup

    args="$*"

    # set pyenv
    pyenv activate ingest
    nohup python /opt/lib/ingest-processing-workflow/ingest.py $args >> /media/SPE/ingest/"$1"-ingest.log 2>&1 &
    
    # deactivate pyenv
    pyenv deactivate
}

transfer () {
    # function to call transferAccession.py under nohup

    args="$*"

    # set pyenv
    pyenv activate ingest
    nohup python /opt/lib/ingest-processing-workflow/transferAccession.py $args >> /media/SPE/ingest/"$1"-transfer.log 2>&1 &
    
    # deactivate pyenv
    pyenv deactivate
}
