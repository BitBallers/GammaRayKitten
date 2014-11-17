Bit Ballers
Jay Miller, Trevor Aron, Glen Smith, Bertha Hu

Things fixed
1) Added sound for player shooting and made the scientists death
	sound less annoying
3) Fix the HUD so elements on the HUD are more evenly spaced
	and nothing every overlaps
4) Made scenery more interesting/varied by adding tables, and machines
	and used blending effects for lighting, as opposed to just having
	the lights as part of the wall sprite images
5) More rooms were added to the 'pool' of rooms to randomly select from
	for the random map generation. This makes the random map generation
	much more varied than before.
8) Made it so the highscores list displays scores in order
9) Made it so you don't get damaged by dead enemies. Before, 
	if you ran into an enemy during its death animation you would still
	get damaged.
11) Made it more apparent that cat is damaged, by making the cat flash when 
	it gets hit. This also lets the player know when the invincibility period
	after getting hit has ended.
	
12) Fixed the enemy AI walking over walls.
13) Made it so duplicate items can't be picked up and if a player already has an
	item, it won't spawn again on the next level.
13) Polish code
	Made all our files pass pep8
	Superclassed our enemies, so know the different types of enemies inherit from the
	same class. This means that alot of methods that we had to write for each individual enemy
	can be inherited from one super class.
