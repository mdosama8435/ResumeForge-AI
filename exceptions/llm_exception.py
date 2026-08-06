from exceptions.base import ResumeForgeException
class LLMException(ResumeForgeException):
    pass
class LLMTimeoutException(LLMException):
    pass
class LLMRateLimitException(LLMException):
    pass
class LLMValidationException(LLMException):
    pass
