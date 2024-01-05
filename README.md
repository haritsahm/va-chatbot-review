# Virtual Assistance for Product Review

<p align=center>
    <a href="https://youtu.be/KpJRGi1W6fI">
        <img src="figures/streamlit-app.png" alt="app-sample-streamlit" width="500"/>
    </a>
</p>

This project is a self-exploratory endeavor aimed at building a Chatbot utilizing [LangChain](https://www.langchain.com/), [OpenAI](https://openai.com/) services, and the [Deep Lake Vector Store](https://www.deeplake.ai/). The primary objective is to analyze Spotify application reviews sourced from a [Kaggle](https://www.kaggle.com/) dataset. The Chatbot, or virtual assistant, will employ the RAG (Retrieval-Augmented Generation) method to provide insightful and relevant responses to user inquiries related to the Spotify application.

The youtube example is available in [here](https://youtu.be/KpJRGi1W6fI).

## Dataset

This project is using the dataset from [Kaggle Dataset: 3.4 Million Spotify Google Store Reviews](https://www.kaggle.com/datasets/bwandowando/3-4-million-spotify-google-store-reviews/data). It contains text reviews, ratings, likes, and app_version that can be used for various application.

The embeddings are available to use from activeloop [hub](https:/app.activeloop.ai/haritsahm/spotify_reviews_cleaned_filtered_balanced_50K_docs_1000_chunk), feel free to access and experiment with it without preparing the vector store.

## Setup

### Hardware Requirements:

- Minimum memory size: 8Gb
- Minimum vCPU cores: 4

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
OPENAI_API_KEY=your_openai_key
[Optional] ACTIVELOOP_TOKEN=your_activeloop_token
```

If you don't have the account, please register to the following websites:

- [OpenAI-API](https://platform.openai.com/docs/overview)

Note that if you're planning to store Deep Lake Vector Store in Activeloop Cloud / Hub, then you must provide the `ACTIVELOOP_TOKEN` by registerin to their [website](https://app.activeloop.ai/). Otherwise, because we're using it locally then there is no need to use the token.

Sign in or register to [Kaggle](kaggle.com) and follow the instruction to setup the `kaggle.json` file.

## Preparation

### 1. Download Dataset

```
kaggle datasets download -d bwandowando/3-4-million-spotify-google-store-reviews
unzip 3-4-million-spotify-google-store-reviews.zip -d data/
# rm 3-4-million-spotify-google-store-reviews.zip
```

### 2. Prepare and Generate Vector Store

> Note: I added the publicly available dataset in Activeloop Hub so there's no need to preprocess this data, skip to [2. Download and Save Locally](#b-download-and-save-deep-lake-vector-store-locally). If you want to experiment with different chunk size, filter maximum number of data, or create a local dataset then you can proceed with this step.

#### a. Process dataset manually and save on local

Because the dataset is large and it will need ~1 hour to process the entire dataset, it's better to prepare and store the data before using it.

Follow the instructions from `notebooks/data-exploration.ipynb` and `notebooks/sentence_generator.ipynb`.

- 'data-exploration' notebook will apply dataset preprocessing and reduce the number of dataset from 3.4M to just 1.1M using naive methods.
- 'sentence_generator' will generate the text files containing the predefined text and storing it in the vector database.

```
# from the root of `va-chatbot-review/`
jupyter lab
```

#### b. Download and save Deep Lake Vector Store Locally.

Deep Lake supports streaming the dataset directly from the cloud store. But this approach depends on the internet speed/bandwidth and may cause a longer response time to our chatbot. The best way is to save the dataset locally and load it at runtime.

This vector store was computed using `chunk_size=1000`, `chunk_overlap=0`, `model=text-embedding-ada-002`, and `max_docs=50000`

```
python3 utils/download_deeplake_vs.py
```

The dataset should be available in `deeplake/spotify_reviews_cleaned_filtered_balanced_50K_docs_1000_chunk`

## Running the application

```
streamlit run app.py

# open localhost:8501 in browser
```

## Contribution

Contributions and feedback are welcome. Feel free to open issues, submit pull requests, or reach out for collaboration.

## License

This project is licensed under [MIT License](https://mit-license.org/) - see the [LICENSE](LICENSE) file for details.
