import autogen
import streamlit as st
import cloudscraper
from bs4 import BeautifulSoup
from typing import List
import re
from streamlit_chat import message


# Configuration
llm_config = {
    "model": "gpt-4o-mini",  
    "api_key": st.secrets["OPENAI_API_KEY"]
}

SERP_API_KEY = st.secrets["SERP_API_KEY"]

# Class to scrape legal content
class Website:
    def __init__(self, url: str):
        self.url = url
        scraper = cloudscraper.create_scraper()  # Bypass Cloudflare
        response = scraper.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to fetch webpage. Status Code: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"

        if soup.body:
            for tag in soup.body(["script", "style", "img", "input"]):
                tag.decompose()
            self.text = soup.body.get_text(separator="\n", strip=True)
        else:
            self.text = "No content found"

        self.links = [link.get('href') for link in soup.find_all('a') if link.get('href')]

    def get_contents(self):
        return self.text  # Full cleaned content

# Function to search legal articles using SerpAPI
def get_legal_article(query):
    search_url = f"https://serpapi.com/search?engine=google&q={query}&api_key={SERP_API_KEY}"
    try:
        response = cloudscraper.create_scraper().get(search_url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "organic_results" in data and len(data["organic_results"]) > 0:
            for result in data["organic_results"]:
                link = result["link"]

                # Avoid links ending in .pdf or containing "/pdf/" or "-pdf"
                if not re.search(r"\bpdf\b", link, re.IGNORECASE):
                    return link

    except Exception as e:
        st.error(f"Error fetching article: {e}")
    
    return None

# Streamlit App
def main():
    st.title("Indian Legal Assistant")
    if 'responses' not in st.session_state:
      st.session_state['responses'] = ["Hi there! Welcome to Indian Legal Assistant. How can I assist you today?"]
    if 'requests' not in st.session_state:
      st.session_state['requests'] = []

    
    # Container for chat history
    response_container = st.container()
    # Container for text box
    text_container = st.container()
    msg = st.chat_input("Enter your legal query:")

    if msg:
        with st.spinner("typing..."):
            try:
                query = f"{msg} Indian law"
                article_url = get_legal_article(query)

                if article_url:
                    #st.write(f"Found article: [Click here]({article_url})")

                    # Extract legal content using the Website class
                    try:
                        website = Website(article_url)
                        extracted_content = website.get_contents()
                    except Exception as e:
                        st.error(f"Failed to extract content: {e}")
                        return


                    # Initialize agent
                    summarization_assistant = autogen.AssistantAgent(name="summarization_agent", llm_config=llm_config)

                    user_proxy_auto = autogen.UserProxyAgent(
                        name="User_Proxy_Auto",
                        human_input_mode="NEVER",
                        is_termination_msg=lambda x: True,
                        code_execution_config={
                            "last_n_messages": 1,
                            "work_dir": "coding",
                            "use_docker": False,
                        },
                    )

                    # Legal Task
                    legal_task = f"""Read the following legal text and provide a natural, easy-to-understand response to the query: "{msg}".  
                     Make sure the explanation is clear and conversational, like how a legal expert would explain it to a non-lawyer. Avoid robotic or overly formal language.  

                     Here is the legal text:  

                     {extracted_content} 
                    """

                    # Initiate Chats
                    chat_results = autogen.initiate_chats(
                        [
                            {
                                "sender": user_proxy_auto,
                                "recipient": summarization_assistant,
                                "message": legal_task,
                                "silent": False,
                                "clear_history": False,
                            }
                        ]
                    )

                    # Display Results
                    if chat_results and chat_results[-1].chat_history:
                        final_response = re.sub(r'\s*TERMINATE\s*$', '', chat_results[-1].chat_history[-1].get("content", "No content received."))
                        st.session_state.requests.append(msg)
                        st.session_state.responses.append(final_response)
                    else:
                        st.error("No results were generated. Please try again.")

                else:
                    st.error("No relevant articles found. Try a different query.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    # Display chat history
    with response_container:
      if st.session_state['responses']:
          for i in range(len(st.session_state['responses'])):
              with st.chat_message('Momos', avatar='legal_pic.png'):
                  st.write(st.session_state['responses'][i])
              if i < len(st.session_state['requests']):
                  message(st.session_state["requests"][i], is_user=True, key=str(i) + '_user')

if __name__ == "__main__":
    main()
