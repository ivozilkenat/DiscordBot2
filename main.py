from clients.client_IPOS import ClientIPOS
from clients.data.token import tk #todo: change import of token? -> saver solution?

if __name__ == "__main__":
	client = ClientIPOS()
	client.run(tk)

#todo:
#-dont display bot dialogues to everyone
#-buttons?
#-work on documentation
#-work on type hints

#todo: bot ideen
#-Zitatgenerator -> Zitatformatierung, Upvotes, Zitat der Woche

#links:
#https://unicode.org/emoji/charts/full-emoji-list.html
#https://discordpy.readthedocs.io/en/stable/interactions/api.html?highlight=commandtree#decorators
#https://discordjs.guide/interactions/autocomplete.html#handling-multiple-autocomplete-options