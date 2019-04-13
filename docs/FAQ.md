**1. Can the performance of this project reach the level of DeepMind's AlphaStar?**

This project has a gap in performance with DeepMind's 'AlphaStar'. But given the difference between the number of machines and resources, such a gap is acceptable. We are solving the problem of StarCraft II in different dimensions with DeepMind. We concentrate more on the efficiency of the method. Additionally, we hope to promote the development of model-based reinforcement learning on StarCraft II.

**2. If there already has an AlphaStar from DeepMind, is it still needed to do research on StarCraft II in future?**

We think it is needed. Firstly, DeepMind's approach is very resource intensive, making it very difficult for small research institutes to reproduce their work. Secondly, the strength of AlphaStar is now more reflected in its micro-operations instead of strategic thinking, contrary to our approach. Finally, the research community of StarCraft II is not strong enough and there are not many open source projects.

**3. Why use the custom my_sc2_env instead of the default sc2_env?**

Two reasons: 1. The features provided by pysc2 are not rich enough. We use the raw interface to enhance the features. Meanwhile, since we use macro actions, in order to simplify the macro actions, we use the raw interface to get the middle information; 2. The change of game version of StarCraft II is very fast, we have added the passed parameter of sc2_env so that it can specify a game version, so our training and testing can be fixed in one version. So we simply modified the two places of sc2_env.

**4. Why use the raw interface of StarCraft II in somewhere?**

As we said before, the information provided by the original pysc2 interface is a bit lacking, so we use the raw interface as a complement. In addition, the execution of some actions in the macro operation requires location information. This information can be obtained from the interface of pysc2, but it is a bit cumbersome. For the sake of simplicity, we get it from the raw interface in this version. Since our goal is to study the use of reinforcement learning to solve StarCraft II, this approach simplifies setup and simplifies research.

**5. Currently, the agent only uses a part of the units and buildings. Is that right?**

Yes. In the current version, we only use some of the early buildings and units (of course, the current code can be easily extended to all units and buildings). For this reason, we call this setup a 'full-length' StarCraft II instead of a 'complete' StarCraft II. Our current code can be easily extended to all units and buildings in a very straightforward way. In a future version, we will try to build an agent using all the units and buildings for complete StarCraft II.

**6. Have you tried to learn this mind-game model before?**

Previous model-based reinforcement learning generally used supervised learning to learn the dynamic model of the environment. But mind-game is not the original environment, so it can't be learned through the data that interacts with the original environment. There are generally three ways to obtain a model. The first is a learning-based approach, and the second is an implementation-based approach (based on domain knowledge). Through prototype experiments, we found that due to the complexity of the StarCraft II environment, the learning-based approach is not effective, which may be the reason for the cumulative error of the model. Models that use domain knowledge have less error, but the cost of implementing full StarCraft II is high. This work uses the third method, which is to implement a mind-game model to learn by states and actions mapping, so as to achieve a balance between performance and efficiency. At the same time, the main purpose of this paper is to explore an efficient reinforcement learning algorithm, rather than focusing on the way the model is obtained. Therefore, more automated model acquisition methods can be put into future work.

**7. Can you summarize this work in one or two sentences?**

We propose an interesting idea and achieve excellent results which outperform previous state-of-the-art results (published). And we hope this work may open up the new way towards model-based reinforcement learning on StarCraft II.
