import dotenv


def load_openai_api_key():
    """Loads the OpenAI API key from a .env file or environment variables."""
    return dotenv.get_key(key_to_get="OPENAI_API_KEY", dotenv_path=".env")
