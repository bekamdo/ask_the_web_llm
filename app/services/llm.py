from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from typing import List, Dict
from app.utils.config import Config
import logging


class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=Config.OPENAI_API_KEY,
            model="gpt-3.5-turbo-1106",
            temperature=0.3
        )

        self.prompt = ChatPromptTemplate.from_template("""
        You are a helpful research assistant. Answer the question comprehensively using the provided sources.
        Your answer should be detailed and cite specific information from the sources.

        Question: {question}

        Available Sources:
        {sources}

        Instructions:
        1. Analyze all sources carefully before answering
        2. Include relevant details, facts, and figures from the sources
        3. For each fact, cite its source using [ID] notation
        4. If the question is broad, provide a comprehensive overview
        5. Format your answer with clear paragraphs
        6. End with complete references in this format:
           [ID] Title - URL

        Answer:
        """)

        self.chain = (
                {"question": RunnablePassthrough(), "sources": RunnablePassthrough()}
                | self.prompt
                | self.llm
                | StrOutputParser()
        )

    def generate_answer(self, question: str, sources: List[Dict]) -> str:
        """Generate a comprehensive answer with proper citations."""
        try:
            # Format sources with clear structure
            formatted_sources = []
            for src in sources:
                source_id = src.get("id", "?")
                title = src.get("title", "Untitled Source").replace("-", " ").strip()
                url = src.get("url", "")
                content = src.get("text", src.get("snippet", "")).strip()

                formatted_sources.append(
                    f"\n[Source {source_id}]: {title}\n"
                    f"URL: {url}\n"
                    f"Content: {content[:1500]}{'...' if len(content) > 1500 else ''}"
                )

            if not formatted_sources:
                return "I couldn't find any relevant sources to answer this question."

            # Join sources with clear separation
            sources_text = "\n\n".join(formatted_sources)

            return self.chain.invoke({
                "question": question,
                "sources": sources_text
            })

        except Exception as e:
            logging.error(f"LLM generation failed: {str(e)}")
            return "I encountered an error while generating an answer. Please try again later."