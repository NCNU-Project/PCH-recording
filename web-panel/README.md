# the web panel

## setup the dev environement
1. download the docker `curl -L get.docker.com | sudo sh`
2. run the setup script `./setup.sh`
3. generate the virtual environment, install pyenv and poetry
    ```
    # install the python build essential
    apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
    
    # install pyenv
    curl https://pyenv.run | bash
    # load some script for interactive shell                                                                                                                                                                         tee -a ~/.bashrc << EOF
    export PATH="$PATH:$HOME/.pyenv/bin/pyenv"
    export PYENV_ROOT="$HOME/.pyenv"
    command -v pyenv >/dev/null || export PATH="\$PYENV_ROOT/bin:\$PATH" 
    eval "\$(pyenv init -)"
    EOF
    source ~/.bashrc
    
    # install the poetry
    curl -sSL https://install.python-poetry.org | python3 -
    # check poetry is installed
    poetry --version
    ```

## run this application
1. set environment and run it
    ```
    # enter the virtual environment
    poetry shell
    export  FLASK_DEBUG=1
    export FLASK_APP=web_panel
    flask run --host=0.0.0.0
    ```
2. browse it on your web browser at `http://<this server's ip>:5000`

## build the docker image
