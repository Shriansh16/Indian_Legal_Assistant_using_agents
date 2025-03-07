# Indian Legal Assistant using Agents
## Overview
The Indian Legal Assistant using Agents is a sophisticated AI-powered tool designed to assist users in understanding complex legal concepts related to Indian law. Leveraging advanced natural language processing (NLP) and web scraping technologies, this application provides clear, concise, and conversational explanations of legal queries. The project integrates multiple components, including:

1. Web Scraping: Extracts relevant legal content from trusted sources.

2. AI Agents: Utilizes AI agents to summarize and explain legal texts in a user-friendly manner.

3. Streamlit Interface: Provides an intuitive and interactive user interface for seamless interaction.

This project is ideal for individuals seeking quick, reliable, and easy-to-understand legal information without needing a background in law.

## Features
1. Legal Query Resolution:

Users can input legal questions, and the assistant will provide detailed, easy-to-understand explanations.

The system searches for relevant legal articles and summarizes them using AI agents.

2. Web Scraping:

Extracts clean and relevant legal content from websites, bypassing Cloudflare protections.

Filters out non-relevant content (e.g., scripts, styles, images) to focus on textual information.

3. AI-Powered Summarization:

Uses OpenAI's GPT-4 model to generate conversational and natural summaries of legal texts.

Ensures explanations are tailored for non-lawyers, avoiding overly formal or robotic language.

4. Interactive Chat Interface:

Built with Streamlit, the interface allows users to interact with the assistant in real-time.

Displays chat history for easy reference.

5. SerpAPI Integration:

Searches for legal articles using Google's search engine via SerpAPI.

Filters out PDF links to ensure only readable content is processed.

## How It Works

1. User Input:

The user inputs a legal query through the Streamlit chat interface.

2. Article Search:

The system uses SerpAPI to search for relevant legal articles related to the query.

3. Content Extraction:

The selected article's content is scraped and cleaned using the Website class.

4. AI Summarization:

The extracted content is passed to an AI agent (powered by OpenAI's GPT-4) for summarization and explanation.

5. Response Generation:

The AI agent generates a clear, conversational response to the user's query, which is displayed in the chat interface.

## Tools and Libraries Used:

1. Streamlit: For building the interactive web interface.

2. Autogen: For managing AI agents and task automation.

3. BeautifulSoup: For web scraping and content extraction.

4. Cloudscraper: To bypass Cloudflare protections during web scraping.

5. SerpAPI: For searching legal articles on Google.

6. OpenAI GPT-4: For natural language understanding and summarization.