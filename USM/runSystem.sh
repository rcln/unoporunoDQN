#!/bin/bash
#for i in {0..4514..4}
for i in {0..720..4}
do
    let "j = $i + 4"
#    PYTHONPATH=./USM:./USM/tools/:./USM/spiders/:$PYTHONPATH /usr/bin/python3.5 ~/PycharmProjects/unoporunoDQN/USM/sample.py $i  $j
    PYTHONPATH=~/unoporunoDQN/USM:~/unoporunoDQN/USM/USM:$PYTHONPATH python ~/unoporunoDQN/USM/sample.py $i $j
done