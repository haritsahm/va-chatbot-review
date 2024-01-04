# Virtual Assistance for Product Review

TBA

## Dataset

This project is using the dataset from [Kaggle Dataset: 3.4 Million Spotify Google Store Reviews](https://www.kaggle.com/datasets/bwandowando/3-4-million-spotify-google-store-reviews/data). It contains text reviews, ratings, likes, and app_version that can be used for various application.

## Setup

### 1. Install Requirements

```
 # for exploring data with notebook and downloading dataset
pip install -r requirements.dev.txt

# for running streamlit app
pip install -r requirements.app.txt

```

### 2. Setup Environment Keys

Create a `.env` file and add the following keys

```
ACTIVELOOP_TOKEN=your_activeloop_token
OPENAI_API_KEY=your_openai_key
```

If you don't have the account, please register to the following websites:

- [OpenAI-API](https://platform.openai.com/docs/overview)
- [Activeloop Deep Lake](https://app.activeloop.ai/)

Sign in or register to [Kaggle](kaggle.com) and follow the instruction to setup the `kaggle.json` file.

## Preparation

### 1. Download Dataset

```
kaggle datasets download -d bwandowando/3-4-million-spotify-google-store-reviews
unzip 3-4-million-spotify-google-store-reviews.zip -d data/
# rm 3-4-million-spotify-google-store-reviews.zip
```

### 2. \[Optional\] Prepare and Generate Vector Store

```
```
