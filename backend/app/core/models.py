import os

from langchain_core.language_models.chat_models import BaseChatModel

def get_model(model_backend: str, cloud_provider: str) -> BaseChatModel:
    """Factory to retrieve the configured language model."""
    provider = (cloud_provider or "").strip().lower()

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        # Support both GOOGLE_API_KEY and GEMINI_API_KEY for convenience.
        if not os.getenv("GOOGLE_API_KEY") and os.getenv("GEMINI_API_KEY"):
            os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY", "")

        model_name = model_backend if model_backend != "llama3" else "gemini-2.0-flash"
        return ChatGoogleGenerativeAI(model=model_name)
    
    if provider == "anthropic":
        from langchain_anthropic import ChatAnthropic
        # Default fallback to sonnet if provider is anthropic but model isn't specified correctly
        model_name = model_backend if model_backend != "llama3" else "claude-3-5-sonnet-20240620"
        return ChatAnthropic(model_name=model_name)
        
    elif provider == "openai":
        from langchain_openai import ChatOpenAI
        model_name = model_backend if model_backend != "llama3" else "gpt-4o"
        return ChatOpenAI(model=model_name)
        
    else:
        # Default to local Ollama
        from langchain_ollama import ChatOllama
        model_name = model_backend if model_backend else "llama3.1"
        return ChatOllama(model=model_name)
