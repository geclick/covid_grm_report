#!/usr/bin/env bash
# This script setups dockerized Redash on Ubuntu 18.04.
set -eu

REDASH_BASE_PATH=/opt/redash

setup(){
    # Installing system dependencies
    sudo apt install pwgen

}

create_directories() {
    if [[ ! -e $REDASH_BASE_PATH ]]; then
        mkdir -p $REDASH_BASE_PATH
        chown $USER:$USER $REDASH_BASE_PATH
    fi

    if [[ -e $REDASH_BASE_PATH/maps ]]; then
        rm -r $REDASH_BASE_PATH/maps
    fi
    
    mkdir -p $REDASH_BASE_PATH/maps
 
    
}

create_config() {
    if [[ -e $REDASH_BASE_PATH/env ]]; then
        rm $REDASH_BASE_PATH/env
    fi
    
    touch $REDASH_BASE_PATH/env

    COOKIE_SECRET=$(pwgen -1s 32)
    SECRET_KEY=$(pwgen -1s 32)
    POSTGRES_PASSWORD="covid19grm"
    REDASH_DATABASE_URL="postgresql://covid19grm:${POSTGRES_PASSWORD}@db/postgres?client_encoding=utf-8"

    echo "PYTHONUNBUFFERED=0" >> $REDASH_BASE_PATH/env
    echo "REDASH_LOG_LEVEL=INFO" >> $REDASH_BASE_PATH/env
    echo "REDASH_REDIS_URL=redis://redis:6379/0" >> $REDASH_BASE_PATH/env
    echo "POSTGRES_PASSWORD=$POSTGRES_PASSWORD" >> $REDASH_BASE_PATH/env
    echo "REDASH_COOKIE_SECRET=$COOKIE_SECRET" >> $REDASH_BASE_PATH/env
    echo "REDASH_SECRET_KEY=$SECRET_KEY" >> $REDASH_BASE_PATH/env
    echo "REDASH_DATABASE_URL=$REDASH_DATABASE_URL" >> $REDASH_BASE_PATH/env 
}

setup_compose() {  
    cp redash/json_ds.py $REDASH_BASE_PATH
    cp redash/granma.json $REDASH_BASE_PATH/maps   
    docker-compose down
    docker-compose run --rm server create_db
    docker-compose up -d --build
}

setup
create_directories
create_config
setup_compose
