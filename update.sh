#!/usr/bin/env bash
if git checkout master &&
    git fetch origin master &&
    [ `git rev-list HEAD...origin/master --count` != 0 ] &&
    git merge origin/master
then
    sudo service reddit-pgn-to-gif restart
    echo 'Updated and restarted'
else
    echo 'Not updated.'
fi
