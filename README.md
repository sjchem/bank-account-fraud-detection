Bank acount fraud detection
- Document your project here
- Description
- Data used
- Where your API can be accessed
- ...
bank-account-fraud-detection/
│
├── api/
│   └── fastapi.py
│
├── logic-main
│   ├── config.py
│   ├── features.py
│   ├── preprocessing.py
│   ├── model.py
│   ├── train.py
│   ├── inference.py
│   └── utils.py
│
├── models/
│   ├── lgb_modified.pkl
│   └── lgb_modified.txt
│
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_modeling_lightgbm.ipynb
│   └── 04_shap.ipynb
│
├── raw_data/
│
├── Dockerfile
├── Makefile
├── README.md
├── requirements.txt
├── .env.sample
└── .gitignore



# API
Document main API endpoints here

# Setup instructions
Document here for users who want to setup the package locally

# Usage
Document main functionalities of the package here
