#!/bin/bash

readonly root_dir='$HOME/mongoDB'

function clean() {
    sudo rm -rf '$root_dir'
}

sudo docker stop wb_spider
sudo docker rm wb_spider

sudo docker stop tw_spider
sudo docker rm tw_spider

clean