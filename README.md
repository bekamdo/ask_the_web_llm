```bash
git clone https://github.com/bekamdo/ask_the_web_llm.git
cd ask-the-web
cp .env.example .env  # Add your API keys
docker run -d -p 8501:8501 --env-file app/.env --memory=512m --cpus=1.0 --name ask-web ask-the-web

Here is the full architecture of the app the user inputs a query 
the websearch searches through the serpapi the contents is scrapped using 
beatufil soup and placed on a llm in which iam using langchain and the data
is outputed through streamlit interface
┌─────────────┐  ┌───────────┐  ┌─────────────┐  ┌───────────┐
│  User Query │→│ Web Search │→│ Content Scrape│→│ LLM Process│
└─────────────┘  └───────────┘  └─────────────┘  └──────┬─────┘
                                                   ┌─────▼─────┐
                                                   │ Formatted │
                                                   │ Answer w/ │
                                                   │ Citations │
                                                   └───────────┘