# LamelosBalls
This is a performance predictor for NBA players. Using a random forrest AI model trained on the previous 10 games of all current NBA players, we will try to predict a basic statline for them in their upcoming game.
## How To Use
Run `fantasyProScraper.py` from the directory `/LamelosBalls/dataScraping/`. Once that script has finished running, run `finalFormatting.tcl`, followed by `mappingTeams.py`, then `mergeToOne.tcl`, both from that same directory. Note that after running finalFormatting, and before continuing, you may have to manually remove some data columns from `dariq-whitehead.csv` to match its syntax to the other files. You gotta remove percentages at some point too glhf
