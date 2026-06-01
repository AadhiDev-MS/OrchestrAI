# OrchestrAI

OrchestrAI is a production-grade multi-agent research and intelligence platform. It is designed to ingest complex academic documents and technical papers, perform granular chunking and vector-based semantic search, and provide highly intelligent synthesized answers using state-of-the-art AI models.

## 🚀 Current Status & Features

The platform has successfully moved from a prototype to a highly functional minimum viable product (MVP). Here are the key accomplishments so far:

*   **Intelligent Agentic RAG**: Powered by Google's latest **Gemini 3 Flash**, the system synthesizes search results into coherent, professional, and well-organized paragraphs rather than just listing raw evidence.
*   **Robust Document Ingestion**: We built a custom parser capable of detecting and splitting academic PDFs based on logical sections (e.g., "Abstract", "1 Introduction"), ensuring much more accurate vector chunking.
*   **Vector Database**: Integrated **PostgreSQL with pgvector**, utilizing HNSW indexes (768 dimensions) to rapidly perform semantic searches over the parsed chunks.
*   **Premium Web Interface**: Developed a sleek, dark-mode Next.js frontend utilizing Tailwind CSS. It features real-time "Thinking..." skeletons, high-contrast glow effects, and a prominent "AI Research Intelligence" section to clearly separate AI insights from raw data.
*   **Containerized Architecture**: The entire stack (Frontend, FastAPI Backend, Postgres, Redis) is managed seamlessly via `docker-compose`.
*   **Smart Query Filtering**: Built-in relevance checks to prevent the system from performing deep research on simple greetings or non-technical queries.

## 🔮 Future Roadmap

While the core functionality is robust, the platform is currently paused. Here are the planned next steps and future features:

1.  **Conversational Memory (Multi-Turn Chat)** 🧠
    *   Transition from single-shot questions to a continuous chat interface, allowing users to ask follow-up questions and dig deeper into specific points.
2.  **Multi-Document Intelligence** 📚
    *   Implement a "Library" view to manage multiple uploaded papers.
    *   Add the ability to compare and contrast findings across different papers simultaneously (e.g., "Compare the scaling laws of BitNet vs. Llama 3").
3.  **Export & Sharing** 📄
    *   Introduce a "Download Report" feature to convert the AI's synthesized summaries into professional PDF or Markdown documents for personal notes.
4.  **AI Observability (LangSmith Integration)** 🔍
    *   Connect the backend to LangSmith to monitor and trace exactly which document chunks the AI retrieves and how it formulates its answers, aiding in debugging and prompt refinement.
5.  **Cloud Deployment** ☁️
    *   Establish a CI/CD pipeline (e.g., via GitHub Actions) for automatic deployment to cloud providers like Google Cloud Run or AWS ECS, making the platform publicly accessible.

## 🛠️ Tech Stack

*   **Frontend**: Next.js, React, Tailwind CSS
*   **Backend**: Python, FastAPI, LangGraph (planned), Google GenAI SDK
*   **Database**: PostgreSQL + pgvector, Redis
*   **Infrastructure**: Docker, Docker Compose

---
*Note: Development is temporarily paused as of June 2026. The repository reflects the latest stable version of the core RAG and Synthesis engine.*
