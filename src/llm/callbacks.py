import time
from typing import Any, Dict, List
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from loguru import logger

class ExecutionTrackingCallbackHandler(BaseCallbackHandler):
    """Callback handler for tracking execution time, prompt size, etc."""
    
    def __init__(self):
        self.start_times: Dict[str, float] = {}
        self.metrics: List[Dict[str, Any]] = []

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""
        run_id = str(kwargs.get("run_id", ""))
        self.start_times[run_id] = time.time()
        
        prompt_length = sum(len(p) for p in prompts)
        estimated_tokens = prompt_length // 4
        logger.info(f"LLM Start [{run_id}]: Prompt length: {prompt_length} chars, Est Tokens: ~{estimated_tokens}")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Run when LLM ends running."""
        run_id = str(kwargs.get("run_id", ""))
        start_time = self.start_times.pop(run_id, None)
        
        if start_time:
            execution_time = time.time() - start_time
            logger.info(f"LLM End [{run_id}]: Execution time: {execution_time:.2f}s")
            self.metrics.append({
                "run_id": run_id,
                "execution_time": execution_time
            })

    def on_retriever_start(
        self, serialized: Dict[str, Any], query: str, **kwargs: Any
    ) -> None:
        """Run when Retriever starts."""
        logger.info(f"Retriever Start: Query='{query[:50]}...'")

    def on_retriever_end(
        self, documents: List[Any], **kwargs: Any
    ) -> None:
        """Run when Retriever ends."""
        logger.info(f"Retriever End: Retrieved {len(documents)} chunks")
