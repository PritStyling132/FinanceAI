from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.http.models import Distance, VectorParams, PointStruct
from typing import Optional

from app.config import get_settings
from app.services.embeddings import EmbeddingService


class VectorStoreService:
    def __init__(self):
        self.settings = get_settings()
        self.client = QdrantClient(
            host=self.settings.qdrant_host,
            port=self.settings.qdrant_port,
        )
        self.collection_name = self.settings.qdrant_collection_name
        self.embedding_service = EmbeddingService()

    def create_collection(self, recreate: bool = False) -> bool:
        """Create the vector collection if it doesn't exist."""
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)

        if exists and recreate:
            self.client.delete_collection(self.collection_name)
            exists = False

        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=self.embedding_service.dimension,
                    distance=Distance.COSINE,
                ),
            )
            return True
        return False

    def collection_exists(self) -> bool:
        """Check if collection exists."""
        collections = self.client.get_collections().collections
        return any(c.name == self.collection_name for c in collections)

    def get_collection_info(self) -> Optional[dict]:
        """Get collection statistics."""
        try:
            if not self.collection_exists():
                return None
            info = self.client.get_collection(self.collection_name)
            # Handle different qdrant-client versions
            points_count = getattr(info, 'points_count', 0) or 0
            return {
                "name": self.collection_name,
                "points_count": points_count,
            }
        except Exception:
            return None

    def upsert_documents(self, documents: list[dict]) -> int:
        """
        Upsert documents into the vector store.
        Each document should have: id, content, metadata (optional)
        """
        if not self.collection_exists():
            self.create_collection()

        points = []
        texts = [doc["content"] for doc in documents]
        embeddings = self.embedding_service.embed_texts(texts)

        for i, doc in enumerate(documents):
            point = PointStruct(
                id=hash(doc["id"]) % (2**63),
                vector=embeddings[i],
                payload={
                    "id": doc["id"],
                    "content": doc["content"],
                    **(doc.get("metadata", {})),
                },
            )
            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )
        return len(points)

    def search(
        self,
        query: str,
        top_k: int = 5,
        score_threshold: float = 0.0,
    ) -> list[dict]:
        """Search for similar documents."""
        if not self.collection_exists():
            return []

        query_embedding = self.embedding_service.embed_query(query)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_embedding,
            limit=top_k,
            score_threshold=score_threshold,
        )

        return [
            {
                "id": hit.payload.get("id"),
                "content": hit.payload.get("content"),
                "score": hit.score,
                "metadata": {
                    k: v for k, v in hit.payload.items()
                    if k not in ["id", "content"]
                },
            }
            for hit in results
        ]

    def delete_all(self) -> bool:
        """Delete all documents from the collection."""
        if self.collection_exists():
            self.client.delete_collection(self.collection_name)
            return True
        return False

    def initialize_knowledge_base(self) -> int:
        """Initialize the vector store with financial knowledge base."""
        from app.data.financial_knowledge import get_knowledge_documents

        self.create_collection(recreate=True)
        documents = get_knowledge_documents()
        return self.upsert_documents(documents)
