
# Movie Recommendation System with Gemini & LlamaIndex

This project demonstrates a semantic movie recommendation system using Google's Gemini embeddings, MongoDB Atlas Vector Search, and LlamaIndex.

## Features

*   **Semantic Search:** Find movies by describing the plot or theme (e.g., "machines fighting humans"), not just keywords.
*   **Hybrid Search:** Combines vector similarity with traditional text search for robust results.
*   **Gemini Integration:** Uses `gemini-embedding-001` (3072 dimensions) for high-quality embeddings and `gemini-1.5-flash` for response synthesis.
*   **MongoDB Atlas:** leverages Atlas Vector Search for scalable and fast retrieval.

## Dataset

The data for this project is sourced from **The Movies Dataset** on Kaggle.
*   **Source:** [The Movies Dataset by Rounak Banik](https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset)
*   **License:** CC0: Public Domain

*Note: The dataset files are tracked in this repository using Git LFS.*

## Setup & Usage

### Prerequisites
*   Python 3.8+
*   MongoDB Atlas Account (Free Tier is sufficient)
*   Google AI Studio API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd movieRec
    ```

2.  **Install dependencies:**
    ```bash
    pip install -qU pymongo llama-index llama-index-embeddings-google-genai llama-index-llms-gemini llama-index-vector-stores-mongodb pandas google-genai
    ```

### Running the Notebooks

1.  **Generate Embeddings (`generate_embeddings.ipynb`):**
    *   This notebook processes the raw CSV data.
    *   It uses the Gemini API to generate 3072-dimensional embeddings for each movie.
    *   Saves the result to `data/movies_with_embeddings.csv`.

2.  **Run Retrieval (`retrieval_strategies_mongodb_llamaindex.ipynb`):**
    *   Ingests the pre-computed embeddings into MongoDB Atlas.
    *   Performs Vector Search and Hybrid Search queries.
    *   **Configuration:** You will be prompted for your `MONGODB_URI` and `GOOGLE_API_KEY`.

## Project Structure

*   `data/`: Contains raw CSVs and the generated embeddings file (tracked via LFS).
*   `generate_embeddings.ipynb`: Notebook for data processing and embedding generation.
*   `retrieval_strategies_mongodb_llamaindex.ipynb`: Main demo notebook for vector search.

## License

This project code is available under the MIT License. Data is provided under CC0 by the original authors.
