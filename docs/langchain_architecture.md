# LangChain Architecture in Resume_Forge_AI

This document explains the rationale and architecture for adopting LangChain in the Resume_Forge_AI orchestration layer. This forms a perfect discussion piece for technical interviews on GenAI system design.

## Why LangChain?
LangChain provides standard interfaces for chaining together Prompts, Language Models, and Output Parsers. In a production application, standardizing on a well-maintained abstraction prevents technical debt associated with writing custom API wrappers, manual retries, and bespoke chunking/vector management scripts.

## Why LCEL (LangChain Expression Language)?
LCEL allows us to define the orchestration flow using declarative syntax (`prompt | llm | output_parser`). 
- **Readability**: The pipeline flow is visually evident in a single line.
- **Parallelism**: Using `RunnableParallel`, LCEL can execute independent requests (like generating a Cover Letter, Interview Questions, and Recruiter Feedback) concurrently without us writing custom `asyncio.gather` boilerplates.
- **Observability**: Built-in callbacks hook right into LCEL to monitor execution time, prompt size, and token generation seamlessly.

## Why PromptTemplate?
Hardcoding prompts in python strings makes them difficult to manage, test, and adapt.
`ChatPromptTemplate` naturally structures our instructions into `SystemMessage` and `HumanMessage`. By injecting our strict anti-hallucination guardrails into the `SystemMessage`, we ensure the model sees these constraints as a fundamental rule of engagement, leading to fewer hallucination attempts.

## Why VectorStoreRetriever and FAISS?
Instead of a bespoke search script, `FAISS` within LangChain provides an efficient vector store that runs locally. `VectorStoreRetriever` normalizes the output into `Document` objects and gives us easy access to configuration strategies like `Top K` search or `Similarity Score Thresholds` natively. 

## Why PydanticOutputParser?
Instead of manual string parsing or regular expressions to pull JSON from markdown ticks, `PydanticOutputParser` inherently validates the schema. If the model strays, the parser throws a structured exception (which LangChain can also automatically retry against if configured to). It guarantees type-safety when our application consumes the LLM output.

## How are Hallucinations Prevented?
1. **Low Temperature Configuration**: We explicitly configured the `GeminiProvider` with a temperature of `0.2` to ensure deterministic, highly factual answers.
2. **System Message Guardrails**: The strict instruction `"HALLUCINATION PREVENTION: You must NEVER invent... If information is unavailable in the resume, you MUST respond with 'Information not found'"` acts as a hard boundary.
3. **Retrieval Grounding**: By retrieving context chunks with strict relevance thresholds via `VectorStoreRetriever`, we force the LLM to only read from explicitly supplied candidate facts.

## How the Resume flows through the system
1. The user uploads a resume (PDF).
2. The `IntelligentChunker` splits the parsed text via `RecursiveCharacterTextSplitter` into `Document` chunks with precise metadata.
3. The chunks are embedded via `HuggingFaceEmbeddings` and stored in the `FAISS` Vector Store.
4. An endpoint requests resume optimization.
5. `VectorStoreRetriever` fetches the most relevant `Document` chunks corresponding to a Job Description.
6. The `ContextBuilder` formats these chunks and metadata into the prompt.
7. The LCEL Chain invokes: `RESUME_OPTIMIZATION_PROMPT | ChatGoogleGenerativeAI | PydanticOutputParser`.
8. The strictly validated `OptimizedResumeSchema` is returned to the user via the FastAPI backend.
