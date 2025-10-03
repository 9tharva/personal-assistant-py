# Pinky: The Python Virtual Assistant

Pinky is a personal voice assistant, inspired by Jarvis, that can perform various tasks based on voice commands. It leverages speech recognition, text-to-speech, and third-party APIs for functionalities like fetching news, setting reminders, and answering general queries.

## Features

-   **Voice-Activated**: Listens for the wake word "Pinky" before processing commands.
-   **Web Browsing**: Opens popular websites like Google, YouTube, GitHub, and more.
-   **Real-Time Information**:
    -   Fetches the current time and date.
    -   Retrieves the top 5 latest news headlines from India.
    -   Performs Google searches for any query.
-   **Productivity**:
    -   Sets reminders for a specified time (e.g., "in 5 minutes").
    -   Handles multiple reminders using a background thread.
-   **Entertainment**:
    -   Plays songs from a predefined local library by opening them in the browser.
-   **AI-Powered Conversations**: Utilizes OpenRouter with a GPT model to handle any unrecognized commands, making the assistant conversational and extensible.
-   **Text-to-Speech**: Provides spoken feedback for all its actions.

## Tech Stack

-   **Language**: Python 3
-   **Core Libraries**:
    -   `SpeechRecognition`: For converting spoken language to text.
    -   `gTTS`: (Google Text-to-Speech) for converting text responses into speech.
    -   `playsound`: To play the generated audio files.
    -   `webbrowser`: To open websites and play music.
    -   `threading`: To run the reminder checking process in the background.
-   **APIs**:
    -   **OpenRouter**: For general AI-powered query handling (`openai/gpt-3.5-turbo`).
    -   **NewsAPI**: To fetch the latest news headlines.

## Setup and Installation

Follow these steps to get Pinky running on your local machine.

### 1. Prerequisites

-   Python 3.7 or higher
-   A working microphone

### 2. Clone the Repository

```bash
git clone [https://github.com/](https://github.com/)<Your-Username>/<Your-Repo-Name>.git
cd <Your-Repo-Name>
```

### 3. Install Dependencies

Install the required Python packages using pip. It's recommended to do this in a virtual environment.

```bash
pip install -r requirements.txt
```

*(You will need to create a `requirements.txt` file. See the section below.)*

### 4. Obtain API Keys

Pinky requires API keys for its core functionalities.

-   **OpenRouter**: Get your API key from [OpenRouter.ai](https://openrouter.ai/).
-   **NewsAPI**: Get your free API key from [NewsAPI.org](https://newsapi.org/).

### 5. Configure Environment Variables

Create a file named `.env` in the root of the project directory. **This file should not be committed to Git.** Add your API keys to this file as follows:

```env
OPENROUTER_API_KEY="your_openrouter_api_key_here"
NEWS_API_KEY="your_newsapi_key_here"
```

### 6. Run the Assistant

Execute the main script to start the assistant.

```bash
python main.py
```

The script will initialize Pinky, and the console will show that it is listening for the wake word.

## How to Use

1.  Say the wake word: **"Pinky"**.
2.  The assistant will respond with "Yes?".
3.  Give one of the supported commands.

**Example Commands:**

-   *"open google"*
-   *"what's the time?"*
-   *"search for the weather in Satara"*
-   *"play sunflower"*
-   *"what are the latest headlines?"*
-   *"remind me to check the oven in 10 minutes"*
-   *"who was the first man on the moon?"* (This will be handled by the AI)
-   *"goodbye"*

## Customization

To add more songs, simply edit the `music` dictionary in the `musicLibrary.py` file with the song title (in lowercase) and the corresponding YouTube URL.
