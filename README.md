# Video Game Recommendation and Analysis System with FastAPI

![Project Image](img/Header.jpg)

## Project Description

This project develops a RESTful API using **FastAPI**, which enables the consumption of information about video games, user reviews, and sentiment analysis to improve business decision-making. The API also includes a recommendation system based on item or user similarity.

### MVP Features:
- **Data Processing and Dataset Preparation**: Data cleaning and consolidation.
- **Sentiment Analysis**: Transform user reviews into a scale of values (0 = bad, 1 = neutral, 2 = positive) using NLP (Natural Language Processing) techniques.
- **Exploratory Data Analysis (EDA)**: Identify patterns and relationships among variables in the dataset.
- **API Deployment**: Create endpoints for specific queries related to games, users, developers, and review analysis.
- **Recommendation System**:
  - **Item-Item**: Based on cosine similarity between games.
  - **User-Item**: Collaborative filtering using user similarity.

## Project Structure and Transformations:
- **Data Optimization**: Remove unnecessary columns to enhance API performance and model training efficiency.
- **Sentiment Analysis Column**: Replace user review text (`user_reviews.review`) with a numerical sentiment score. Reviews with no text are given a neutral value of 1.

### Feature Engineering:
- Transform user reviews into a numeric column (`sentiment_analysis`) for model input.

### Exploratory Data Analysis (EDA):
- Detect variable patterns and outliers.
- Create word clouds to identify common terms in game titles.

## RESTful API Overview:
Endpoints developed using **FastAPI** and accessible via any device connected to the internet:

- **/developer**: Returns the number of items and percentage of free content per year for a given developer.
- **/userdata**: Provides user data including total spending, recommendation rate based on reviews, and number of items.
- **/UserForGenre**: Finds the user with the most accumulated play hours in a specific genre, including hourly distribution by release year.
- **/best_developer_year**: Lists the top 3 developers with the most user-recommended games in a specified year.
- **/developer_reviews_analysis**: Analyzes review sentiment (positive/negative) for a given developer.

## Recommendation System:
Two approaches for video game recommendations:
- **Item-Item Recommendation**: Utilizes cosine similarity between games. Input a product ID to get 5 similar game recommendations.
- **User-Item Recommendation**: Employs collaborative filtering based on user similarity. Input a user ID to get 5 games liked by similar users.

## Deployment:
- Deployment using **Ngrok** for easy access.

## About:
A RESTful API built with **FastAPI** that processes and transforms data related to Steam games and offers a machine learning-based recommendation system. The API provides endpoints for game data retrieval, review analysis, and personalized recommendations.

### Topics:
- Python
- Data Science
- Machine Learning
- Machine Learning Algorithms

### Resources:
- **Readme**

### License:
- **GPL-3.0 License**
