import requests


def get_search_result(API_KEY, SEARCH_ENGINE_ID, query, page=[1]):
    """
    API_KEY and SEARCH_ENGINE_ID are for the url
    query : keyword for searching
    page=[1]   means  1-10 results
    page=[1,2] means  1-20 results
    with 30 ir 40 results, you might run out of 4096 token in gpt3
    """
    res_str = ""
    for p in page:
        start = (p - 1) * 10 + 1
        url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"
        # print(url)
        data = requests.get(url).json()
        # get the result items
        search_items = data.get("items")
        # iterate over 10 results found
        for i, search_item in enumerate(search_items, start=1):
            try:
                long_description = search_item["pagemap"]["metatags"][0]["og:description"]
            except KeyError:
                long_description = "N/A"
            # get the page title
            title = search_item.get("title")
            # page snippet
            snippet = search_item.get("snippet")
            # alternatively, you can get the HTML snippet (bolded keywords)
            # html_snippet = search_item.get("htmlSnippet")
            # extract the page url
            link = search_item.get("link")

            # print the results
            line = f"[{i + start - 1}]"
            print(line)
            res_str += line + "\n"

            line = "Title: " + title
            print(line)
            res_str += line + "\n"

            if long_description != "N/A":
                line = "Long description: " + long_description
            else:
                line = "Description: " + snippet
            print(line)
            res_str += line + "\n"

            line = "URL: " + link + "\n"
            print(line)
            res_str += line + "\n"
    return res_str
