# Online Courses RAG System

This project implements a **web crawling + semantic search + RAG system**
for searching online educational courses from real websites.

## Features
- Web crawling from online course platforms
- Knowledge base construction
- Semantic search using TF-IDF
- Answer generation using LLM (RAG)

## Project Structure
- crawler_sabzlearn.py → crawl courses
- crawler_w3schools.py → crawl tutorial courses
- merge_data.py → merge crawled data
- rag_system.py → semantic search + RAG

## How to Run
1. Run crawlers to collect course data
2. Run merge_data.py
3. Run rag_system.py and enter a query

## Demo Video
The demo video demonstrates crawling and RAG-based search.

## Technologies
- Python
- BeautifulSoup
- Scikit-learn
- Ollama (Qwen2.5)
