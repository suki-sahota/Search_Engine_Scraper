import json
from search_engine import SearchEngine

#Dictionary to hold results for each query
query_to_results = {}

with open('queries_to_run.txt', 'r') as f:
    for line in f:
        query = line.strip()
        #Save the following list and put in JSON form
        results = SearchEngine.search(query)
        query_to_results[query] = results

#Write dictionary to json file
with open('scraped_search_results.json', 'w') as out_file:
    json.dump(query_to_results, out_file, indent = 4)
