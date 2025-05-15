import streamlit as st
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from app.services.scraper import ScraperService
from app.services.search import SearchService
from app.services.llm import LLMService
from app.utils.config import Config
# Initialize services
Config.validate()
search_service = SearchService()
scraper_service = ScraperService()
llm_service = LLMService()


def main():
    st.set_page_config(page_title="Ask the Web", page_icon="🌐")
    st.title("🌐 Ask the Web (LangChain)")

    # Session state
    if "answer" not in st.session_state:
        st.session_state.answer = None
    if "sources" not in st.session_state:
        st.session_state.sources = []

    question = st.text_input("Ask a question:")

    if st.button("Ask") and question:
        with st.spinner("Searching & generating answer..."):
            try:
                # 1. Search the web
                search_results = search_service.search_web(question)

                # 2. Scrape content
                scraped_sources = []
                for result in search_results:
                    scraped = scraper_service.scrape_page(result["url"])
                    scraped_sources.append({
                        "id": result["id"],
                        "title": result["title"],
                        "url": result["url"],
                        "text": scraped["text"]
                    })

                # 3. Generate answer
                st.session_state.answer = llm_service.generate_answer(question, scraped_sources)
                st.session_state.sources = scraped_sources

            except Exception as e:
                st.error(f"Error: {str(e)}")

    if st.session_state.answer:
        st.markdown(st.session_state.answer)

        with st.expander("View Sources"):
            for source in st.session_state.sources:
                st.write(f"[{source['id']}] {source['title']} - {source['url']}")


if __name__ == "__main__":
    main()