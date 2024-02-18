# Spotify Grapher

## 📖 Description

A tiny Python project that generates visualizations of your Spotify streaming history, made so I can practice working with Pandas data frames. :)

Go to your Spotify account and request your data. You'll get a zip file with a bunch of JSON files. This project will generate a couple of graphs from that data.

Features:

- Generate a bar chart of the top 10 songs played.
- Generate a line chart of the listening history for the top 5 artists.

## 🛠️ Setup & Installation
To set up the project, clone the repository and install the required dependencies:

```
git clone https://github.com/emsuru/spotify-grapher.git
```

## 👩‍💻 Usage

To run the script and generate your own graphs, copy the zip you get from Spotify into this project's directory (it will be called 'my_spotify_data.zip') then execute:

```

python main.py

```

The graphs will be saved as `top_10_songs.png` and `top_5_artists.png`.

## 📂 Project background
This is my first personal project after starting to learn Python.

The project is inspired by [Eric Chiang's inquiry](https://ericchiang.github.io/post/spotify/) into his own streaming history.

Eric had access to his entire Spotify streaming history. I'm still waiting for mine (it takes up to 30 days) but meanwhile I got a small data set from Spotify, covering only the past year and a subset of info. 16,490 events iso the 120,000 Eric had.

## Visuals 

My top song of the past year is actually my toddler's top song.. 

![top-songs](top_10_songs.png)

Spot when my toddler started having a say in what we listen to..

![top-artists](top_5_artists.png)


---

Thanks for visiting my project page!

Connect with me on [LinkedIn](https://www.linkedin.com/in/mirunasuru/) 

🤍
