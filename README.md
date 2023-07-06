# dex_trades

# Installation

## 1. Setup virtual environment
```
python -m venv .venv 
```

## 2. Activate Virtual Environment
```
source .venv/bin/activate
```

## 3. Install Dependencies
```
pip install -e .
```

# Usage

## 1. Playgrounds API Key
Get API key from Playgrounds. Create a .env file in the root directory and add the following line:
```
PG_KEY =API KEY HERE
```

Add .env to .gitignore so that it doesn't get shared anywhere.

## 2. Run the test script
```
python tests/dextrades.py
```
