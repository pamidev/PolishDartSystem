# Idea
The idea to create an application was born during a darts competition in one of the local pubs, 
during which the results were written down on pieces of paper.


# Goals

### The main tasks of the application are currently:
* collecting information about ongoing darts tournaments in one place, along with the possibility of signing up
for players' lists
* automation of the registration and approval process of tournament participants
* automation of the selection of pairs of players
* displaying individual game results and statistics

### in the future it is planned:
* adding a "scoreboard" module that will help collect and convert points entered during the game to ultimately 
generate statistics for a given game and the entire tournament
* rescaling the application to support more tournaments and users


# Assumptions (business requirements)

## User not logged in
An not logged in user can only see basic information about planned and completed tournaments, such as date, name, city,
place and the number of players approved by the organizer.

>Such a not logged in user can, of course, create an account to have more options.

## User logged in
__User__ - i.e. one who does not have the `organizer` status, but has the ability to:
* see your profile (data that is saved in the database)
* change or supplement the data provided during registration
* register for the tournament
* see own registration status in tournament details (registered, player, referee)
* see a list of approved players for a given tournament and their status
* after approval by the organizer and granting him the status of a player or referee, he may perform these functions 
in the tournament for which he registered
* become an organizer

__Organizer__ - i.e. one who has the `organizer` status assigned by the administrator:
* has possibilities like `user` (except the last one of course)
* additionally can:
    * add information about tournaments he organizes
    * edit information about tournaments you have added
    * grant and revoke player and/or referee status to registered participants in their tournaments
    * create a schedule of matches for approved players and assign referees to them
    * enter match results

>Since the application is still in the development process, it is impossible to update the `README.md` frequently. 
>Once some modules are refined, its more detailed description of how it works and screenshots will appear.