from libzim.reader import Archive
from libzim.search import Query, Searcher
from libzim.suggestion import SuggestionSearcher

zim = Archive("data/wikipedia_en_all_nopic_2024-06.zim")
print(f"Main entry is at {zim.main_entry.get_item().path}")


#entry = zim.get_entry_by_path("home/fr") # fr?
#entry = zim.get_entry_by_path("home") # fr?
#print(f"Entry {entry.title} at {entry.path} is {entry.get_item().size}b.")
#print(bytes(entry.get_item().content).decode("UTF-8"))

# searching using full-text index
#search_string = "Welcome"
search_string = "pronoun"
query = Query().set_query(search_string)
searcher = Searcher(zim)
search = searcher.search(query)
search_count = search.getEstimatedMatches()
print(f"there are {search_count} matches for {search_string}")
print(list(search.getResults(0, search_count)))

# accessing suggestions
search_string = "kiwix"
suggestion_searcher = SuggestionSearcher(zim)
suggestion = suggestion_searcher.suggest(search_string)
suggestion_count = suggestion.getEstimatedMatches()
print(f"there are {suggestion_count} matches for {search_string}")
print(list(suggestion.getResults(0, suggestion_count)))
