import config
import spicepy

print(spicepy.tkvrsn("TOOLKIT"))

config_list = config.main()
bodiesList = []

for i in config_list:
    bodiesList.append(config_list[i])

print(bodiesList)