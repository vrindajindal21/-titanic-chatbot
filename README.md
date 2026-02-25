# Titanic Dataset Chatbot

A friendly chatbot that analyzes the Titanic dataset using natural language queries.

## Features
- Answer questions about Titanic passengers
- Generate visualizations (histograms, bar charts)
- Conversation history with save/delete functionality
- Built with FastAPI backend and Streamlit frontend

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Download dataset: `curl -o titanic.csv https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv`
3. Run backend: `cd app && uvicorn main:app --reload`
4. Run frontend: `cd frontend && streamlit run app.py`

## Usage
Open the Streamlit app and ask natural language questions like:

### 📊 Demographics
- "Show me the age distribution"
- "What are the age statistics?"
- "What percentage of passengers were male?"
- "How many passengers were female?"

### 🚢 Survival Analysis
- "What was the survival rate?"
- "Show me survival rates by class"
- "How many passengers survived?"
- "What was the survival rate for women?"

### 💰 Economics
- "What was the average ticket fare?"
- "Show me the fare distribution"
- "What are the fare statistics?"

### 👨‍👩‍👧‍👦 Travel & Ports
- "How many passengers embarked from each port?"
- "How many people came from Southampton?"
- "What's the family size distribution?"

### 📈 Overview
- "Give me an overview of the dataset"
- "Tell me about the Titanic passengers"
- "What's in this dataset?"

## New Features
- **Beautiful Chat Interface**: Gradient message bubbles with smooth animations
- **Attractive Design**: Custom CSS styling with gradients, shadows, and modern UI
- **Statistics Dashboard**: Quick stats cards showing dataset info
- **Enhanced UX**: Welcome screen, loading animations, and visual feedback
- **Message Management**: Delete individual messages or clear entire conversation
- **Responsive Layout**: Optimized for different screen sizes

## Tech Stack
- Backend: Python, FastAPI
- Frontend: Streamlit
- Data: Pandas, Matplotlib, Seaborn

## Notes
- Handles specific queries directly for accuracy
- Provides visualizations for supported questions
- No external API keys required