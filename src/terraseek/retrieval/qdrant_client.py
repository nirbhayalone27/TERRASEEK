"""Qdrant vector search client with in-memory fallback support."""

import logging
from typing import Any, Dict, List, Optional
from qdrant_client import QdrantClient
from qdrant_client.http import models as qmodels

from terraseek.config import settings

logger = logging.getLogger("terraseek.retrieval")


class VectorIndexManager:
    def __init__(self, url: Optional[str] = None, collection_name: Optional[str] = None):
        self.collection_name = collection_name or settings.vector_db.collection_name
        self.dimension = settings.vector_db.embedding_dimension
        self.url = url or settings.vector_db.url
        self.client = self._init_client()
        self.ensure_collection()

    def _init_client(self) -> QdrantClient:
        if settings.vector_db.prefer_in_memory or self.url == ":memory:":
            return QdrantClient(":memory:")

        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                api_key = settings.vector_db.api_key if self.url.startswith("https://") else None
                client = QdrantClient(
                    url=self.url,
                    api_key=api_key,
                    timeout=1.0,
                    check_compatibility=False,
                )
                client.get_collections()
                return client
            except Exception:
                logger.info(f"Qdrant remote connection not active at {self.url}; operating in high-performance in-memory vector mode.")
                return QdrantClient(":memory:")

    def is_healthy(self) -> bool:
        try:
            self.client.get_collections()
            return True
        except Exception:
            return False

    def ensure_collection(self):
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            if not exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=qmodels.VectorParams(
                        size=self.dimension,
                        distance=qmodels.Distance.COSINE,
                    ),
                )
                logger.info(f"Created Qdrant collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Failed to ensure collection {self.collection_name}: {e}")

    def _format_point_id(self, point_id: str) -> str:
        import uuid
        try:
            uuid.UUID(str(point_id))
            return str(point_id)
        except (ValueError, AttributeError):
            return str(uuid.uuid5(uuid.NAMESPACE_DNS, str(point_id)))

    def upsert_observation(
        self,
        point_id: str,
        vector: List[float],
        payload: Dict[str, Any],
    ):
        clean_id = self._format_point_id(point_id)
        point = qmodels.PointStruct(
            id=clean_id,
            vector=vector,
            payload=payload,
        )
        self.client.upsert(
            collection_name=self.collection_name,
            points=[point],
        )

    def search_similar(
        self,
        vector: List[float],
        limit: int = 10,
        score_threshold: float = 0.0,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        query_filter = None
        if filters:
            must_conditions = []
            for k, v in filters.items():
                must_conditions.append(
                    qmodels.FieldCondition(
                        key=k,
                        match=qmodels.MatchValue(value=v),
                    )
                )
            if must_conditions:
                query_filter = qmodels.Filter(must=must_conditions)

        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=limit,
            score_threshold=score_threshold,
            query_filter=query_filter,
        )

        return [
            {
                "id": str(r.id),
                "score": float(r.score),
                "payload": r.payload or {},
            }
            for r in results
        ]

    def delete_point(self, point_id: str):
        self.client.delete(
            collection_name=self.collection_name,
            points_selector=qmodels.PointIdsList(points=[point_id]),
        )


_index_manager: Optional[VectorIndexManager] = None


def get_vector_manager() -> VectorIndexManager:
    global _index_manager
    if _index_manager is None:
        _index_manager = VectorIndexManager()
    return _index_manager
