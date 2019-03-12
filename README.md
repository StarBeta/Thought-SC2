# Mind-SC2

## Introduction

Here is the code corresponding to the paper "Efficient Reinforcement Learning with a Mind-Game for Full-Length StarCraft II". 

Our program has the following characteristics: 
* **Efficient**: It takes only a few hours to train an agent that defeats built-in elite difficulty (difficulty 7) bot; 
* **Scalable**: Our approach can be easily extended to other races and maps and achieved good performance in these settings; 
* **Simple**: There is no need to design manual rewards in our method, nor does it require complex architectures.

## How to train an agent (P vs. T) in mind-game?

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
<div style="overflow-x:scroll">
<img src="https://github.com/mindgameSC2/mind-SC2/blob/master/figures/ACRL.png"/>
<img src="https://github.com/mindgameSC2/mind-SC2/blob/master/figures/ACRLfromScratch.png"/>
</div>

## What is the Mind-game model

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
**1. If there already has an AlphaStar from Deepmind, is it still needed to do research on SC2?**

We think this is needed. Firstly, Deepmind's approach is too resource intensive, making it difficult to reproduce their work. Secondly, the strength of AlphaStar is now more reflected in the micro-operations. Finally, as a research direction, there are still too few open source projects on StarCraft II. 

**2. Can the performance of this project's code reach the level of Deepmind's AlphaStar?**

No. This code still has a gap in performance with Deepmind's 'AlphaStar', but we concentrate on the efficiency of the method. Meanwhile, we hope to promote the development of model-based reinforcement learning on SC2.





