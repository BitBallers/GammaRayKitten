Team Name: Bit Ballers
Jay Miller, Trevor Aron, Glen Smith, Bertha Hu

We have added level 3, which contains a new enemy type, the insect.
The insect is significantly faster than the slimes, hence a more challenging enemy.
There is also a new landscape to the level, which gives it a more sinister feel
than the previous two levels. Right now there is only 1 enemy type per each level.
This is simply to emphasize the differences in levels, but in the final game
it is likely that there will be a mixture of enemies on each level, and that mixture
will be determined by the difficulty of the level. This week, we added support for
that functionality (multiple enemy types per level, spawned at a certain percentage).

We also added a new item type, which like all items, will randomly appear in the item
room (each item has a equal probability of appearing). This new item is a shield. 
When the player picks up this item, they are given full health, and the maximum amount
of health they can obtain increases from 5 to 6.

We also revised the enemy AI system so that if there is not a valid path towards the player,
they will "wander" around, as opposed to staying still. Although this "wandering" includes
staying stationary, for strategic reasons.

Finally, we finally added interlevel cutscenes, which are pretty dope.

To skip levels, press 0. 

To run the game, type "python game.py". 
