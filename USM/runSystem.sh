#!/bin/bash
for i in {4080..4514..4}
do
    let "j = $i + 4"
    PYTHONPATH=./USM:./USM/tools/:./USM/spiders/:$PYTHONPATH /usr/bin/python3.4 ~/PycharmProjects/unoporunoDQN/USM/sample.py $i  $j
done