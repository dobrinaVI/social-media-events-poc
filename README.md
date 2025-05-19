# Social Media Analytic Pipeline
POC for a social media analytics pipeline. The raw data consists of user interactions and views on posts from both the app and website. 

## Objective
Transform raw event data into structured, analytics-ready datasets to support dashboarding and advanced analysis.

## Data Description
1. *Posts* dataset: Contains post metadata:
    * `hash`: string ID of the post
    * `author_uid`: numeric ID of the author of the post
    * `channel`: name of channel; posts can be optionally tagged with a topic/channel
    * `created_at`: timestamp of posting, in msec since Unix epoch

2. *Events* dataset: Contains user events:
    - `uid`: numeric ID of the user performing the action  
    - `ts`: timestamp of the event, in milliseconds since Unix epoch  
    - `type`: type of the event, either `post-view` or `post-interaction`  
    - `data`: serialized JSON with event-specific details  

    For `post_view` events:  
    - `post_hash`: hash of the post  
    - `on`: location where the action took place, possible values:  
        - `home`: home feed  
        - `trending`: trending posts feed  
        - `channel`: channel-specific feed (only if post has a channel tag)  
        - `notifications`: notifications tab (e.g., user notified about a post)  

    For `post_interaction` events:  
    - `post_hash`: hash of the post  
    - `on`: location where the action took place (same as above)  
    - `sub_type`: type of interaction, possible values:  
        - `open`: user opened the post in full  
        - `like`: user liked the post  
        - `play_video`: user played a video in the post  
        - `click_image`: user enlarged an image in the post  
        - `repost`: user reposted the post  
        - `reply`: user replied to the post  
        - `share`: user shared the post (e.g., copied direct link)  

## 🏁 Pipeline Steps
1. Ingestion: Reads raw .txt input files, applies schema, writes to Parquet.
```
python ingestion/main.py
```
2. (upcoming) DuckDB Creation : Loads Parquet files into DuckDB tables for further querying and analysis.
3. (upcoming) Set up a DBT project for transformation

## 🧪 Testing
1. Test Ingestion
```
pytest tests/test_ingestion.py
```
