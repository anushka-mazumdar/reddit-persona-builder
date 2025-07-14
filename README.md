# Reddit User Persona Generator

Persona Builder is a tool designed to automate the creation and management of Reddit profiles for research, marketing, or personal use. It streamlines the process of setting up new accounts, configuring personas, and interacting with Reddit's API.

---

## 📌 Features

- Takes a Reddit username as input
- Scrapes user posts and comments using `praw`
- Builds a qualitative user persona with LLM-based interpretation
- Saves output as a formatted `.txt` file
- Includes citations from original Reddit content for each trait

---

## 🛠️ Tech Stack

- Python 3.8+
- [PRAW (Python Reddit API Wrapper)](https://praw.readthedocs.io/)
- Reddit API credentials (client ID, client secret, user agent)
---

## 📁 Folder Structure

```

├── main.py                          # Entry point
├── scraping/
│   └── reddit\_scraper.py           # Scrapes Reddit user data
├── processing/
│   └── persona\_generator.py        # Generates persona using LLM
├── data/
│   └── <username>\_raw\.json         # Saved raw Reddit data
├── output/
│   └── <username>\_persona.txt      # Final persona text with citations
├── requirements.txt                # Python dependencies

````

---

## 🚀 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/reddit-persona-generator.git
cd reddit-persona-generator
````

### 2. Install Dependencies

It's recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add Reddit API Credentials

Create a `praw.ini` in the root directory or set environment variables. Here's an example `praw.ini`:

```ini
[default]
client_id=your_client_id
client_secret=your_client_secret
user_agent=your_user_agent
```

You can get these credentials from [Reddit Developer Apps](https://www.reddit.com/prefs/apps).

---

## 🧪 How to Run

### Modify `main.py`

Replace the placeholder usernames with actual Reddit usernames:

```python
usernames = ["kojied", "Hungry-Move-6603"]
```

Then run the script:

```bash
python main.py
```

Output personas will be saved in the `output/` directory.

---

## 📄 Output Example

Each persona file will look like this:

```
Username: kojied

Personality Traits:
- Curious and detail-oriented [Source: Comment on r/AskScience]
- Enjoys gaming and anime culture [Source: Post on r/gaming]

Interests:
- Psychology, Anime, Gaming
...

```

---

## 🧼 Coding Standards

This code adheres to [PEP8](https://peps.python.org/pep-0008/) standards and is modular for scalability.

---


