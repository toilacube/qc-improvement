from typing import Optional
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from settings import settings
from langchain_google_genai import ChatGoogleGenerativeAI
'''
- Input: Requirements
- Ouput: Test case scenarios:
    + A structure table
    + 


'''

class LLMFactory:
    @staticmethod
    def create(
        provider: Optional[str] = None,
        temperature: float = 0,
        streaming: bool = True,
    ) -> BaseChatModel:
        """
        Create a LLM instance based on the provider
        """
        # If no provider specified, use the one from settings
        provider = provider or settings.CHAT_PROVIDER
        print(f"Creating LLM with provider: {provider}")

        if provider.lower() == "openai":
            return ChatOpenAI(
                temperature=temperature,
                streaming=streaming,
                model=settings.OPENAI_MODEL,
                openai_api_key=settings.OPENAI_API_KEY,
                openai_api_base=settings.OPENAI_API_BASE
            )
        elif provider.lower() == "ollama":
            # Initialize Ollama model
            return OllamaLLM(
                model=settings.OLLAMA_MODEL,
                base_url=settings.OLLAMA_API_BASE,
                temperature=temperature,
                streaming=streaming
            )
        elif provider.lower() == "gemini":
            # Initialize Ollama model
            return ChatGoogleGenerativeAI(
                temperature=temperature,
                streaming=streaming,
                model=settings.GEMINI_MODEL,
                google_api_key=settings.GEMINI_API_KEY,
            )
        # Add more providers here as needed
        # elif provider.lower() == "anthropic":
        #     return ChatAnthropic(...)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")