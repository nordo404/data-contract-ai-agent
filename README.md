# data-contract-ai-agent

A Python-based data processing tool that infers schemas, generates YAML data contracts, and organizes column metadata using both deterministic logic and LLM-assisted analysis.

## Features
- Automatic schema inference from CSV files  
- AI-powered detection of timestamps, dates, booleans, and numeric types  
- YAML data contract generation following a strict reference structure  
- Column ordering based on data modeling best practices  
- Clean snake_case normalization for all fields  
- Supports both rule-based and LLM-based schema inference

## Project Structure
data-contract-ai-agent/
│
├── data/               # Input CSV files
├── generator/          # YAML contract generator logic
├── llm/                # LLM schema inference logic
├── notebooks/          # Jupyter notebooks for exploration
├── output/             # Generated YAML contracts
├── reference/          # Reference contract templates
├── schema/             # Schema inference utilities
│
├── main.py             # Entry point for running the agent
├── requirements.txt    # Python dependencies
└── README.md


## Requirements
- Python 3.10+
- Polars
- Your LLM client (OpenAI, Azure OpenAI, etc.)

Install dependencies:
pip install -r requirements.txt


## Contributing
This is a personal project, happy to take comments and feedback.

## License
MIT License
