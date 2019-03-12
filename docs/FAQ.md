**1. If there already has an AlphaStar from Deepmind, is it still needed to do research on SC2?**

We think this is needed. Firstly, Deepmind's approach is too resource intensive, making it difficult to reproduce their work. Secondly, the strength of AlphaStar is now more reflected in the micro-operations. Finally, as a research direction, there are still too few open source projects on StarCraft II. 

**2. Can the performance of this project's code reach the level of Deepmind's AlphaStar?**

No. This code still has a gap in performance with Deepmind's 'AlphaStar', but we concentrate on the efficiency of the method. Meanwhile, we hope to promote the development of model-based reinforcement learning on SC2.

**3. Why use the custom my_sc2_env instead of the default sc2_env?**

Two reasons: 1. The features provided by pysc2 are not rich enough. We use raw_interface to enhance the features. Meanwhile, since we use macro actions, in order to simplify the macro actions, we use raw_interface to get the middle information; 2. The change of game version of SC2 is very fast, we have added the pass parameter of sc2_env so that it can specify a game version, so our training and testing can be fixed in one version. So we simply modified the two places of sc2_env.
