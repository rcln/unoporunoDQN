#!/bin/bash

rm -rf ~/unoporunoDQN/USM/train_db/*
python make_folders.py

#for i in {0..9936..4}
for i in {0..2000..4}
do
    let "j = $i + 4"
#    PYTHONPATH=./USM:./USM/tools/:./USM/spiders/:$PYTHONPATH /usr/bin/python3 ~/PycharmProjects/unoporunoDQN/USM/sample.py $i  $j
    PYTHONPATH=~/unoporunoDQN/USM:~/unoporunoDQN/USM/USM:$PYTHONPATH python ~/unoporunoDQN/USM/sample.py $i $j
done