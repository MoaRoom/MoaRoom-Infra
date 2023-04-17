#!/bin/sh
DEV_BRANCH=feat/${WEBSSH_BRANCH}

# sync webssh
item=webssh
git clone https://github.com/NayeonKeum/$item.git
cd $item
git remote update
git fetch
git checkout ${DEV_BRANCH} 
git pull origin ${DEV_BRANCH}
cd ..

# cp res files
RES_DIR_PATH=../../res
cp $RES_DIR_PATH/.env ./.env
cp $RES_DIR_PATH/*.py ./server/res/