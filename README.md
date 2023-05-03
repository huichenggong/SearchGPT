# SearchGPT
I want to combine search engine with GPT.  
We first do a keyword search on Google.  
Then we feed all the search result to GPT and ask question.

# How to use
```
cp env.example .env
```
Configure your [openAI API key](https://platform.openai.com/account/api-keys)  
Configure your [Programmable Search Engine](https://programmablesearchengine.google.com/controlpanel/all)  
For Biochemistry academic search, please look at the `academic_website.txt`.  
Go ahead to `search_and_sumarize.ipynb`
```
conda create -n search -c conda-forge openai requests python-dotenv ipykernel
# ipython kernel install --name search --user
```