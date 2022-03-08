# Victoris-Stats
This app is designed for two main functions at the moment.
The first is a way to get basic information on players that intend to play in our league such as win rate, games played in the season, current rank and summoner level. 
We have certain parameters that we vet accounts for our league to ensure that they are playing on their main or highest ranked account.

Second and most important to Victoris esports is the collection of stats from a tournament game so that we may keep track of games and playesrs statistics throughout the course of the league. 
In order to do this the bot looks only at one server that I only allow a few people access to. The syntax to use the bot looks something like this !<league acronym> <match id>. For example, !vts 4237955843 will grab me the necessary stats from the game with the ID of 4237955843.
After that the bot will call the Riot API and collect all of the data into an array and assigns it to each player and following the collection of this data it writes to our google sheets with all of our data. From there all of the data gets formatted into our sheets for the actual user interface part of the sheets for our players.
The bot also does the same thing for team stats and keeps track of champion stats such as pick rate, bans, pressence and win rate. 
An example of our output in it's formatted shape can be found here : https://docs.google.com/spreadsheets/d/1Ap58iizRYxzogINBYYcEH1fCCnhF4q90kzZmKBxzwxk/edit#gid=129161365 for our Victoris Triumph Series (Grandmaster Capped League) and the sample raw output can be found at this screenshot here : https://gyazo.com/125eff6c19dd42a596bb210b96b07787
  
One of our current biggest issues with our API key is that I have to re-generate my API key every morning in order for this to work which can be quite a hassle especially if I am out of town or away froom my computer. One of the advantages that I would love to utilize is not having to regenerate my api key every morning as I know other people who have thier production keys.
Another big issue currently is that we currently have to use third party websites in order to keep our tournaments running with tournament codes. After match-v4 was discontinued and it was moved onto match-v5 we lost custom game compatibility which meant we had to use tournament codes in order to collect any sort of stats from our games. 

Down the line some things we would like to add is the opportunity to track Valorant stats as our Valorant leagues are growing quite quickly. Tournament code generation so that we can cut reliance on third party websites such as toornament and battlefy. And our production team has mentioned multiple times that they would be able to integrate a lot of useful features into their broadcast with a production key as well. 

  
You can find any info about us at the following links  
Victoris Esports discord link : https://discord.gg/victoris
Victoris Esports youtube channel : https://www.youtube.com/c/VictorisEsports
Victoris Esports twitch channel : https://www.twitch.tv/victorisgg and https://www.twitch.tv/victorisgg2
Victoris Esports twitter : https://twitter.com/VictorisGG
Victoris Esports website : https://victoris.gg
