import time
from loguru import logger
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from .base_provider import BaseLLMProvider
from exceptions.llm_exception import LLMException, LLMTimeoutException, LLMRateLimitException
from config.settings import settings

class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        raw_keys = settings.GEMINI_API_KEY.split(',')
        keys = [k.strip() for k in raw_keys if k.strip()]
        if not keys:
            raise LLMException("GEMINI_API_KEY is not configured.")
            
        llms = [
            ChatGoogleGenerativeAI(
                model="gemini-flash-latest",
                google_api_key=key,
                temperature=0.2,
                convert_system_message_to_human=True,
                timeout=30.0,
                max_retries=1
            ) for key in keys
        ]
        
        self.llm = llms[0]
        if len(llms) > 1:
            self.llm = self.llm.with_fallbacks(llms[1:])

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((LLMTimeoutException, LLMRateLimitException)),
        reraise=True
    )
    def generate_structured(self, prompt: str) -> str:
        start_time = time.time()
        estimated_tokens = len(prompt) // 4
        logger.info(f"GeminiProvider starting generation. Prompt length: {len(prompt)} chars (~{estimated_tokens} tokens)")
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            duration = time.time() - start_time
            logger.info(f"GeminiProvider completed in {duration:.2f}s")
            return response.content
        except Exception as e:
            error_str = str(e).lower()
            if "timeout" in error_str or "deadline" in error_str:
                logger.warning(f"GeminiProvider timeout: {e}")
                raise LLMTimeoutException(f"Timeout connecting to Gemini: {e}")
            elif "429" in error_str or "quota" in error_str or "rate limit" in error_str:
                logger.warning(f"GeminiProvider rate limit hit: {e}")
                raise LLMRateLimitException(f"Gemini Rate Limit exceeded: {e}")
            else:
                logger.error(f"GeminiProvider generic failure: {e}")
                raise LLMException(f"GeminiProvider failed: {e}")
