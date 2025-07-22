# **AstroCryptoLab 🤖**

A local tool for analyzing crypto news trends using RSS feeds, SQLite, and a Large Language Model (LLM) run locally via LM Studio. The results are displayed in an interactive web interface built with Streamlit.

## **➤ Key Features**

* **RSS Feed Aggregation**: Automatically collects news from multiple, configurable crypto news sources.  
* **Local Data Persistence**: Stores all articles in a local SQLite database to avoid repeated downloads and allow for historical analysis.  
* **Private, Local AI Analysis**: Utilizes any language model loaded in [LM Studio](https://lmstudio.ai/) to analyze articles. Your data and analysis remain 100% private and offline.  
* **Structured Analysis**: Extracts key insights from each article:  
  * **Sentiment**: The overall tone (e.g., Positive, Neutral, Negative).  
  * **Mentioned Assets**: A list of cryptocurrencies or projects mentioned.  
  * **Investment Signal**: An assessment of market interest or hype.  
* **Interactive UI**: A web interface built with Streamlit to display, filter, and trigger the analysis of news articles.

## **➤ Technology Stack**

* **Backend & Logic**: Python  
* **Web Framework**: Streamlit  
* **Database**: SQLite  
* **RSS Parsing**: feedparser  
* **LLM Integration**: openai (client library, connected to the local LM Studio server)  
* **LLM Hosting**: LM Studio

## **➤ Project Structure**

The project is designed to be modular, with a clear separation of concerns.

krypto\_gpt\_analyser/  
|  
|-- data/  
|   \`-- news.db             \# The auto-generated SQLite database  
|  
|-- scripts/  
|   |-- \_\_init\_\_.py         \# Makes the directory a Python package  
|   |-- gpt\_analyzer.py     \# Contains the logic for interfacing with the LLM  
|   |-- rss\_parser.py       \# Parses RSS feeds and stores them in the DB  
|  
|-- .gitignore              \# Ignores venv and cache files  
|-- feeds.txt               \# A list of RSS feed URLs to parse  
|-- main.py                 \# The main Streamlit application script  
|-- requirements.txt        \# A list of Python dependencies

## **➤ Setup & Installation**

Follow these steps to get the project running locally.

### **1\. Prerequisites**

* [Python 3.10+](https://www.python.org/)  
* [LM Studio](https://lmstudio.ai/)  
* Git

### **2\. Clone the Repository**

git clone \<YOUR-REPOSITORY-URL\>  
cd krypto\_gpt\_analyser

### **3\. Set Up the Python Environment**

Create a virtual environment and install the required packages.

\# Create a virtual environment  
python \-m venv .venv

\# Activate the environment (Windows)  
.venv\\Scripts\\activate.bat

\# Activate the environment (macOS/Linux)  
source .venv/bin/activate

\# Install the dependencies  
pip install \-r requirements.txt

### **4\. Configure LM Studio**

1. Open LM Studio.  
2. Search for and download a suitable model.  
   * **Recommendation**: Nous Hermes 2 Mistral 7B-DPO (look for a Q4\_K\_M GGUF version for a good balance of performance and size).  
3. Navigate to the "Local Server" tab (the ↔️ icon).  
4. Select your downloaded model from the dropdown menu and click **"Start Server"**. The server should now be running and accessible at http://localhost:1234/v1.

## **➤ Running the Application**

### **1\. Initial Data Fetch**

Run the parser script once to create the database and populate it with the latest articles.

python scripts/rss\_parser.py

### **2\. Launch the Streamlit App**

Start the web interface.

streamlit run main.py

Your default web browser should open with the application running.

### **3\. How to Use**

* **Fetch News**: Click the "Fetch Latest News" button in the sidebar to update the database with new articles.  
* **Analyze an Article**: On any unanalyzed article, click the "Analyze with GPT" button to start the analysis with your local LLM.  
* **Filter & Search**: Use the sidebar controls to show only analyzed/unanalyzed articles or to search for keywords in titles and summaries.

## **➤ Future Work & Potential Enhancements**

* **Dashboard View**: Create an overview page with charts showing sentiment over time or the most frequently mentioned assets.  
* **Automation**: Set up a cron job to run rss\_parser.py on a schedule.  
* **Batch Analysis**: Add a feature to analyze all unanalyzed articles in one go.  
* **Model Comparison**: Allow switching between different LLMs in the UI to compare analysis results.