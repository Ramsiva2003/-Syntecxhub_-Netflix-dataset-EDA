# ------------------------------------------------------
# 🎬 Syntecxhub Internship | Project 2: Netflix Dataset EDA
# ------------------------------------------------------

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# ------------------------------------------------------
# Step 1: Setup & Load Dataset (LOCAL FILE)
# ------------------------------------------------------
os.makedirs("graphs", exist_ok=True)

# ✅ Your local dataset path
file_path = r"C:\Users\siva\Downloads\netflix_titles_2021.csv"

# Load dataset safely
try:
    df = pd.read_csv(file_path)
    print("✅ Dataset Loaded Successfully!")
    print("\n🔹 First 5 Rows:")
    print(df.head())
except FileNotFoundError:
    print("❌ ERROR: Could not find the file at the given path.")
    print("Please check that 'netflix_titles_2021.csv' is in the correct folder.")
    exit()

# ------------------------------------------------------
# Step 2: Inspect Data
# ------------------------------------------------------
print("\n📊 Dataset Info:")
print(df.info())
print("\n🧮 Missing Values:\n", df.isnull().sum())

# ------------------------------------------------------
# Step 3: Clean Data
# ------------------------------------------------------
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['country'].fillna('Unknown', inplace=True)
df['duration'].fillna('Unknown', inplace=True)

# ------------------------------------------------------
# Step 4: Visualizations (Show + Save)
# ------------------------------------------------------

# 1️⃣ Movies vs TV Shows
plt.figure(figsize=(6,4))
sns.countplot(data=df, x='type', palette='Set2')
plt.title('Count of Movies vs TV Shows')
plt.xlabel('Type'); plt.ylabel('Count')
plt.savefig("graphs/1_content_type.png", bbox_inches='tight')
plt.show()

# 2️⃣ Content Added Over Time
content_by_year = df['year_added'].value_counts().sort_index()
plt.figure(figsize=(10,5))
sns.lineplot(x=content_by_year.index, y=content_by_year.values, marker='o')
plt.title('Netflix Content Added Over the Years')
plt.xlabel('Year'); plt.ylabel('Number of Titles')
plt.savefig("graphs/2_content_by_year.png", bbox_inches='tight')
plt.show()

# 3️⃣ Top 10 Countries
top_countries = df['country'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=top_countries.values, y=top_countries.index, palette='magma')
plt.title('Top 10 Content-Producing Countries')
plt.xlabel('Number of Titles'); plt.ylabel('Country')
plt.savefig("graphs/3_top_countries.png", bbox_inches='tight')
plt.show()

# 4️⃣ Top 10 Genres
df['genre'] = df['listed_in'].str.split(',').str[0]
top_genres = df['genre'].value_counts().head(10)
plt.figure(figsize=(8,5))
sns.barplot(x=top_genres.values, y=top_genres.index, palette='coolwarm')
plt.title('Top 10 Genres on Netflix')
plt.xlabel('Count'); plt.ylabel('Genre')
plt.savefig("graphs/4_top_genres.png", bbox_inches='tight')
plt.show()

# 5️⃣ Movie Duration Distribution
movie_df = df[df['type'] == 'Movie']
movie_df['duration_num'] = (
    movie_df['duration'].str.replace(' min', '', regex=False)
    .replace('Unknown', np.nan).astype(float)
)
plt.figure(figsize=(8,5))
sns.histplot(movie_df['duration_num'].dropna(), bins=30, kde=True, color='skyblue')
plt.title('Movie Runtime Distribution')
plt.xlabel('Duration (minutes)'); plt.ylabel('Count')
plt.savefig("graphs/5_runtime_distribution.png", bbox_inches='tight')
plt.show()

# ------------------------------------------------------
# Step 5: Insights Summary
# ------------------------------------------------------
summary = """
📌 Netflix Dataset Insights:

1️⃣ Movies dominate Netflix content compared to TV Shows.
2️⃣ Content addition grew rapidly after 2015.
3️⃣ USA, India, and UK are top producers of Netflix titles.
4️⃣ Drama and Comedy are the most common genres.
5️⃣ Most movies run between 80–120 minutes.
"""

print(summary)

# ------------------------------------------------------
# Step 6: Export Outputs
# ------------------------------------------------------
df.to_csv("netflix_cleaned.csv", index=False)
with open("netflix_insights.txt", "w", encoding="utf-8") as f:
    f.write(summary)

print("\n✅ All graphs saved inside 'graphs/' folder.")
print("✅ Cleaned dataset and insights file exported successfully!")
