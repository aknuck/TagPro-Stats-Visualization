TagPro Stats Visualization
============
Created March 2014

Requires PyGame

This is created for use with player stats from the web game TagPro (www.tagpro.gg), a 2D capture the flag game. When moving in the game, a player must accelerate and decelerate in any direction you want to move. There is a lot of skill in properly "juking", or maneuvering around other players, to get to the flag and get away with it, while using various environment elements to assist you. While carrying the flag a player can be tagged, which reults in them going back to their flag and waiting a few seconds to respawn.

Statistics for tagpro players are shown on www.tagpro-stats.com, with statistics in categories such as captures per grab, number of times returning the flag, number of flags grabbed, etc.

This program takes the player statistics, which are normally just shown as a series of numbers, and displays them in a visualization to make it easier to judge the skill of a player. Statistics are also organized by offensive and defensive stats, so it is easier to see if the player is more of an offensive or defensive player. It also allows for comparison of two players by overlaying their visualizations. The statistics are based on monthly stats, and a larger area on the visualization means that the player is more highly ranked.

Usage
======
Find the page on tagpro-stats.com for the player and look at the url for the user id:
![ScreenShot](https://i.imgur.com/NqVslKy.png)

In the example above the id would be 22123
Then use that number to generate the statistics:
![ScreenShot](https://i.imgur.com/i6oQSMw.png)

The image of the Visualization can then be saved with or without the sidebar
Players can also be compared when both fields are filled:
![ScreenShot](https://i.imgur.com/GA6H1GU.png)


NOTE: There have been changes to tagpro-stats.com, so not everything works as well as it used to and the "games played" and "win percentage" stats on the sidebar no longer function. I'll be fixing it soon.
