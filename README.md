# movie-recommender-system-tmdb-dataset
A content-based movie recommender system using cosine similarity, built with Streamlit.

## Quickstart (Local)

1) Create and activate a virtual environment
```
python3 -m venv .venv
source .venv/bin/activate
```

2) Install dependencies
```
pip install -r requirements.txt
```

3) Provide TMDB API key (optional for posters)
- Option A (env):
```
export TMDB_API_KEY="YOUR_TMDB_KEY"
```
- Option B (Streamlit secrets): create `.streamlit/secrets.toml`
```
[general]
TMDB_API_KEY = "YOUR_TMDB_KEY"
```

4) Ensure model files exist
- Place `movie_list.pkl` and `similarity.pkl` under `model/`:
```
model/
  movie_list.pkl
  similarity.pkl
```

5) Run the app locally
```
streamlit run app.py
```

## Project Structure
```
app.py                      # Streamlit app
requirements.txt            # Python dependencies
model/                      # Pickle files (not committed)
  movie_list.pkl
  similarity.pkl
```

## Deployment

### Deploy to Streamlit Community Cloud
1. Push this repo to GitHub.
2. Create a new app in Streamlit Cloud pointing to `app.py`.
3. In the app settings, set Secrets:
```
TMDB_API_KEY = "YOUR_TMDB_KEY"
```
4. Deploy. The app will install `requirements.txt` automatically.

Alternative: Add a local secrets file for development
```
.streamlit/secrets.toml
TMDB_API_KEY = "YOUR_TMDB_KEY"
```

### Deploy with Docker (optional)
Create `Dockerfile`:
```
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PORT=8501
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
Build and run:
```
docker build -t movie-recsys .
docker run -p 8501:8501 -e TMDB_API_KEY=YOUR_TMDB_KEY movie-recsys
```

## Notes
- Posters require a valid TMDB API key. Without it, recommendations still work but posters may show as unavailable.
- If you modify the model artifacts, regenerate `movie_list.pkl` and `similarity.pkl` accordingly.
