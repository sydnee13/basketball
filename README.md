# basketball
NBA Basketball Compatability

What makes basketball players compatible? Is it their ability to pass and cut and create space around each other? Is it their ability to mold their play style night to night around the ups and downs of their complementary teammate? This project aims to quantify the attributes of “dynamic duos” in the NBA that allow them to play well together. Using data science techniques like regression, random forest, and XGBoost, I expect to create a rankable compatibility score for each duo. I will use these scores to make predictions on what players around the league can possibly play well together as well as make predictions on the outcomes of winning based on the structure of NBA rosters. 

All but one data source comes from Basketball Reference. The exception comes from pbpstats (https://www.pbpstats.com/assist-combo-summary/nba) that includes data on assists for duos on each team. Some of the Basketball Reference sources are listed:
- https://www.basketball-reference.com/teams/BOS/2024/lineups (and the corresponding site for each team)
- https://www.basketball-reference.com/leagues/NBA_2024_per_game.html
- https://www.basketball-reference.com/teams/ATL/2024.html (and the corresponding site for each team)
