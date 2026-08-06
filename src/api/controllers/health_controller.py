class HealthController:
    @staticmethod
    def check_status() -> dict:
        # In a real scenario, ping the FAISS store, LLM API, etc.
        return {
            "api_status": "operational",
            "llm_status": "operational",
            "embedding_status": "operational",
            "faiss_status": "operational"
        }
