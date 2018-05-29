#!/bin/bash

echo "Provisioning virtual machine for local apps..."
# NVM
if ! grep -q 'export NVM_DIR="$HOME/.nvm"' $HOME/.bashrc ; then
    echo "Install NVM..."
    NVM_VERSION=v0.33.11
    NODE_VERSION=v8.11.2
    wget -qO- https://raw.githubusercontent.com/creationix/nvm/$NVM_VERSION/install.sh | bash &>/dev/null
    source ~/.nvm/nvm.sh; nvm install $NODE_VERSION --silent; nvm use --delete-prefix $NODE_VERSION
fi

# Virtualenvwrapper
if ! grep -q 'virtualenvwrapper.sh' $HOME/.bashrc ; then
    echo "Install Virtualenvwrapper..."
    pip install --user virtualenvwrapper --quiet
    printf '\n%s\n%s\n%s\n%s\n%s\n' \
    'export WORKON_HOME=$HOME/.virtualenvs' \
    'export PROJECT_HOME=$HOME' \
    'export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3' \
    'export VIRTUALENVWRAPPER_VIRTUALENV=$HOME/.local/bin/virtualenv' \
    'source $HOME/.local/bin/virtualenvwrapper.sh' >> $HOME/.bashrc
fi

# Add aliases
touch $HOME/.bash_aliases
PYTHON="alias python='python3'"
RUNSERVER='alias runserver="python manage.py runserver 0.0.0.0:8000"'
ACTIVATE="alias activate='cd $HOME/app; workon app'"
if ! grep -q "$RUNSERVER" $HOME/.bash_aliases ; then
    echo "set up alias for RUNSERVER"
    echo $RUNSERVER >> $HOME/.bash_aliases
fi
if ! grep -q "$ACTIVATE" $HOME/.bash_aliases ; then
    echo "set up alias for ACTIVATE"
    echo $ACTIVATE >> $HOME/.bash_aliases
fi
if ! grep -q "$PYTHON" $HOME/.bash_aliases ; then
    echo "set up alias for PYTHON"
    echo $PYTHON >> $HOME/.bash_aliases
fi

# Set up project
# mkvirtualenv app
# cd app
# pip install -r requirements/local.txt
# mv $VIRTUAL_ENV/bin/postactivate $VIRTUAL_ENV/bin/postactivate_org
# ln -s $HOME/app/_virtualenv/postactivate_local $VIRTUAL_ENV/bin/postactivate
# mv $VIRTUAL_ENV/bin/predeactivate $VIRTUAL_ENV/bin/predeactivate_org
# ln -s $HOME/app/_virtualenv/predeactivate $VIRTUAL_ENV/bin/predeactivate
