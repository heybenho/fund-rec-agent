# Fund Recommendation Agent
This is a RAG-based agent that recommends gift funds to donors based on their intent, interests, and capacity.

5,000 synthetic gift funds are generated in Postgres, including the fund terms, benefitting unit, purpose, and sub-purpose. They are embedded and indexed into OpenSearch. A donor's interests and capacity are run through a hybrid OpenSearch query that finds appropriate funds using semantic similarity and capacity scoring. The FastAPI service generates a short, grounded rationale for each top result via a locally-run LLM (Llama 3.2:1b). The Next.js app lets a donor submit their interests and capacity, and receive the recommendations.

## Motivation
This is a project to get hands-on experience with a specific tech stack: Python, TypeScript, Next.js, Node.js, PostgreSQL, OpenSearch, and Docker.
