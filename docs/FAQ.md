**1. Can the performance of this project reach the level of DeepMind's AlphaStar?**

This project has a gap in performance with DeepMind's 'AlphaStar'. But given the difference between the number of machines and resources, such a gap is acceptable. We are solving the problem of StarCraft II in different dimensions with DeepMind. We concentrate more on the efficiency of the method. Additionally, we hope to promote the development of model-based reinforcement learning on StarCraft II.

**2. If there already has an AlphaStar from DeepMind, is it still needed to do research on StarCraft II in future?**

We think it is needed. Firstly, DeepMind's approach is very resource intensive, making it very difficult for small research institutes to reproduce their work. Secondly, the strength of AlphaStar is now more reflected in its micro-operations instead of strategic thinking, contrary to our approach. Finally, the research community of StarCraft II is not strong enough and there are not many open source projects.

**3. Why use the custom my_sc2_env instead of the default sc2_env?**

Two reasons: 1. The features provided by pysc2 are not rich enough. We use the raw interface to enhance the features. Meanwhile, since we use macro actions, in order to simplify the macro actions, we use the raw interface to get the middle information; 2. The change of game version of StarCraft II is very fast, we have added the passed parameter of sc2_env so that it can specify a game version, so our training and testing can be fixed in one version. So we simply modified the two places of sc2_env.

**4. Why you use raw interface?**

As we said before, the information provided by the original pysc2 interface is a bit lacking, so we use the raw interface as a complement. In addition, the execution of some actions in the macro operation requires location information. This information can be obtained from the interface of pysc2, but it is a bit cumbersome. For the sake of simplicity, we get it from the raw interface in this version. Since our goal is to study the use of reinforcement learning to solve StarCraft II, this approach simplifies setup and simplifies research.

**4. I see that currently the agent only uses a part of the units and buildings. Is that right??**

Yes. In the current version, we only used some of the early buildings and units (of course, the current code can be easily extended to all units and buildings). For this reason, we call this setup a 'full-length' StarCraft II instead of a 'complete' StarCraft II. Our current code can be easily extended to all units and buildings in a very straightforward way. In a future version, we will try to build an agent using all the units and buildings for complete StarCraft II.
