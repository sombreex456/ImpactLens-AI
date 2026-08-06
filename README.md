# 🔎 ImpactLens AI

### AI-Powered Decision Impact & Risk Analyser

ImpactLens AI is a Streamlit application that uses a local large language model (LLM) to analyse and compare two decisions across multiple impact and risk dimensions.

The application combines AI-generated analysis with Python-based calculations and visualisations to provide structured decision support.

## Features

- AI-powered decision analysis using Ollama and Llama 3.2
- Compares two decision options
- Scores six impact dimensions from 1–10:
  - Financial
  - Operational
  - Customer
  - Reputation
  - Privacy
  - Ethical
- Calculates overall mean risk scores using Python
- Identifies key trade-offs between options
- Generates advantages, disadvantages and hidden consequences
- Provides an AI-generated comparison and recommendation
- Visualises risk scores using Plotly
- Includes loading states and error handling

## How It Works

1. The user enters two decisions into the Streamlit interface.
2. Python sends the information to a locally running Ollama LLM.
3. The LLM analyses each option and returns structured JSON containing impact scores and written analysis.
4. Python processes the JSON response and calculates the overall mean risk score.
5. The application compares the individual scores to identify significant trade-offs.
6. Streamlit displays the scores, analysis, visualisations and recommendation.

A key design principle is that the LLM performs the qualitative analysis, while Python handles the numerical calculations and comparisons.

## Technologies

- Python
- Streamlit
- Ollama
- Llama 3.2
- Requests
- JSON
- Plotly
- Git & GitHub

## Project Structure

```text
ImpactLens-AI/
├── app.py
├── README.md
├── requirements.txt
└── .gitignore