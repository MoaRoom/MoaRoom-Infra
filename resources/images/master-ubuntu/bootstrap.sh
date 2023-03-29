#!/bin/sh
DEV_BRANCH=feat/nkeum-dev
# for item in { webssh }
# do
item=webssh
git clone https://github.com/NayeonKeum/$item.git
cd $item
git checkout $DEV_BRANCH 
git pull origin $DEV_BRANCH
cd ..
# done