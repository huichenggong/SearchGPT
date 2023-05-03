import requests
import openai


def get_search_result(API_KEY, SEARCH_ENGINE_ID, query, page=[1], print_result=True):
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
            res_str += line + "\n"

            line = "Title: " + title
            res_str += line + "\n"

            if long_description != "N/A":
                line = "Long description: " + long_description
            else:
                line = "Description: " + snippet
            res_str += line + "\n"

            line = "URL: " + link + "\n"
            res_str += line + "\n"
    if print_result:
        print(res_str)
    return res_str


def search_res_decoration(search_res, question, query):
    message_res = search_res + f"""
    Here is the web search result using the following keywords "{query}".
    1. Please write a comprehensive reply discussing "{question}". Make sure to cite search results using [number](URL) notation after the reference.
    2. List all the useful reference you discussed using [number](URL) notation.
    3. Provide more search keywords to better understand the first question.
    """
    return message_res


def search_ask_gpt35t(query, question, page, GOOGLE_API_KEY, SEARCH_ENGINE_ID,
                      decorat_fun=search_res_decoration, print_debug=True):
    search_res = get_search_result(GOOGLE_API_KEY, SEARCH_ENGINE_ID, query, page=page, print_result=False)
    message_res = decorat_fun(search_res, question, query)
    message = [
        {"role": "system", "content": "You are a helpful assistant that reads and summarizes academic literatures"},
        {"role": "user", "content": message_res},
    ]
    res35T = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        temperature=0.4,
        max_tokens=800,
    )
    print("Keywords :", query)
    print("Question :", question)
    print()
    print(res35T["choices"][0]["message"]["content"])

    if print_debug:
        print(res35T["usage"])
        print("This conversation costs ", res35T["usage"]["total_tokens"] / 1000 * 0.002, "USD")
        print(res35T["choices"][0]["finish_reason"])
    return search_res, res35T
