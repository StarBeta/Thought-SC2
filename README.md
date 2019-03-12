# Mind-SC2

## Update

We have added the codes for training or testing an agent (P vs. T) in SC2. Now you can train an agent beating the most difficult (level-7) bot of SC2 in only one to two hours (on a common sever). Enjoy it! If you find any questions, please start an issue.

## Introduction

This is the code corresponding to the paper "Efficient Reinforcement Learning with a Mind-Game for Full-Length StarCraft II". 

Our method has the following characteristics: 
* **Efficient**: It takes only a few hours to train an agent that defeats built-in elite difficulty (difficulty 7) bot; 
* **Scalable**: Our approach can be easily extended to other races and maps and achieved good performance in these settings; 
* **Simple**: There is no need to design manual rewards in our method, nor does it require complex architectures.

![Terran Agent](figures/Terran_1.jpg)

## What is the Mind-game model?

This is a mixed model which combines the accurate part of information of SC2 units and buildings and inaccurate part which contains a turn-based simulated battle system partially inspired by the game of 'Heroes of Might and Magic III'. 

The directory structure is as follows:
```
mind-SC2/
          |->strategy/
                |-> agent.py              * base classs of transition part
          |->unit/
                |-> units.py              * base classs of unit and building part
                |-> protoss_unit.py       * units for protoss from SC2
                |-> terran_unit.py        * units for terran from SC2
                |-> zerg_unit.py          * units for zerg from SC2
          |->mini_agent.py                * transition part for protoss
          |->strategy_env.py              * battlefield part
```

## How to train an agent (P vs. T) in mind-game?

### Requirements
- python==3.5
- tensorflow==1.5

### Usage
Run train_by_dummy.py to train an agent of P vs. T in mind game in a distributed setting. See train_by_dummy.py for more parameters.

**Run testing**
```
python train_by_dummy.py --restore_model=True --show_details=True
```

**Important Parameters**
```
--restore_model:    Whether to restore old model.
--num_for_update:   How many episodes for one iteration.
--parallel:         How many process to run, debug set to 1, training set to 10.
--thread_num:       How many threads in one process, debug set to 1, training set to 5.
--port_num:         Port number for distribute training in tensorflow.
--train_iters:      How many iterations for training.
--show_details:     Weather to show details of one mind-game, debug set to True, training set to False.
```

**Run training**
```
python train_by_dummy.py 
```

### Results

**ACRL**

![ACRL](figures/ACRL.png)

**ACRLfromScratch**

![ACRLfromScratch](figures/ACRLfromScratch.png)

## How to train an agent (P vs. T) defeating difficulty 7 bot of SC2 in one hour ?

### Requirements
- python==3.5
- tensorflow==1.5
- future==0.16
- pysc2==1.2
- matplotlib==2.1
- scipy==1.0

**Notes**
If you install pysc2==1.2 and find this error "futures requires Python '>=2.6, <3' but the running Python is 3.5.6", then try first install futures as follow
```
pip install futures==3.1.1
```
then install pysc2==1.2, and this problem is solved.

**Notes**
If you find this warning "[features.py:361] Unknown ability 3757 seen as available." too many, you can go to the pysc2 folder and find the code of features.py and comment the line 361 code.

### Usage
Run eval_mini_srcgame.py to train an agent (P vs. T) in StarCraft II. See eval_mini_srcgame.py for more parameters. 

**Run testing**
```
python eval_mini_srcgame.py
```

**Important Parameters**
```
--training:         Whether to train an agent.
--restore_model:    Whether to restore old model.
--on_server:        If want to train on a server in distributed setting, set it to ture.
--map:              Name of a map to use. Default is Simple64.
--agent_race:       Agent's race. Default is P.
--bot_race:         Bot's race. Default is T.
--difficulty:       Bot's strength. Default is 7.
--port_num:         Port number for running SC2.
--max_iters:        How many iterations for training.
--step_mul:         Game speed. Set to 1 while testing. Set to 8 while training.
```

**Run training (transferring from mind-game)**
```
python eval_mini_srcgame.py --restore_model_path="./model/20190121-212908_mini/" --on_server=True --step_mul=8 --max_iters=100
```

### Benchmark
**Time**
TODO

## LICENSE
MIT LICENSE

## Citation
Please cite our paper if you find this repository useful.

## TODO
- [x] Mind-game model
- [x] P vs. T in mind-game by ARCL
- [x] P vs. T in SC2 (Simple64, difficulty 7) by transfer learning
- [ ] Z vs. Z in mind-game by ARCL
- [ ] T vs. T in mind-game by ARCL

## FAQ

Please refer to [here](docs/FAQ.md)





