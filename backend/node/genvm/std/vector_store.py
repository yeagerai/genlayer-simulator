# backend/node/genvm/std/vector_store.py

import numpy as np
from backend.node.genvm.std.models import get_model


class VectorStore:
    def __init__(self, model_name: str = None):
        """
        Initialize the VectorStore with a custom embedding model.

        Args:
            model: A model with an encode method to generate embeddings.
        """
        self.vector_data = {}  # Dictionary to store vectors
        self.metadata = {}  # Dictionary to store metadata
        self.model_name = model_name

    def add_text(self, text, metadata):
        """
        Add a new text to the store with its metadata.

        Args:
            text (str): The text to be added.
            metadata (dict): The metadata containing log_id.
        """
        if "log_id" not in metadata or not isinstance(metadata["log_id"], int):
            raise ValueError("Metadata must contain an integer 'log_id'")

        model = get_model(self.model_name)
        embedding = model.encode([text])[0]
        vector_id = len(self.vector_data)
        self.vector_data[vector_id] = embedding
        self.metadata[vector_id] = metadata

    def get_closest_vector(self, text):
        """
        Get the closest vector to the given text along with the similarity percentage and metadata.

        Args:
            text (str): The text for which to find the closest vector.

        Returns:
            tuple: A dictionary containing the similarity percentage, the closest vector, and the metadata.
        """
        result = self.get_k_closest_vectors(text, k=1)
        return result[0]

    def get_k_closest_vectors(self, text, k=5):
        """
        Get the closest k vectors to the given text along with the similarity percentages and metadata.

        Args:
            text (str): The text for which to find the closest vectors.
            k (int): The number of closest vectors to return.

        Returns:
            list: A list of dictionaries, each containing the similarity percentage, the vector, and the metadata.
        """
        model = get_model(self.model_name)
        query_embedding = model.encode([text])[0]

        # Convert vector_data to a NumPy array for efficient calculations
        all_embeddings = np.array(list(self.vector_data.values()))
        all_ids = np.array(list(self.vector_data.keys()))

        # Compute cosine similarities
        dot_products = np.dot(all_embeddings, query_embedding)
        norms = np.linalg.norm(all_embeddings, axis=1) * np.linalg.norm(query_embedding)
        similarities = dot_products / norms

        # Get the top k similarities
        top_k_indices = similarities.argsort()[-k:][::-1]
        results = [
            (
                float(similarities[i] * 100),
                int(all_ids[i]),
                self.metadata[all_ids[i]],
                self.vector_data[all_ids[i]].tolist(),
            )
            for i in top_k_indices
        ]
        return results

    def update_text(self, vector_id, new_text, new_metadata):
        """
        Update the text and metadata of an existing vector.

        Args:
            vector_id (int): The identifier of the vector to update.
            new_text (str): The new text to update.
            new_metadata (dict): The new metadata to update.
        """
        if vector_id not in self.vector_data:
            raise ValueError("Vector ID does not exist")

        if "log_id" not in new_metadata or not isinstance(new_metadata["log_id"], int):
            raise ValueError("Metadata must contain an integer 'log_id'")

        model = get_model(self.model_name)
        embedding = model.encode([new_text])[0]
        self.vector_data[vector_id] = embedding
        self.metadata[vector_id] = new_metadata

    def delete_vector(self, vector_id):
        """
        Delete a vector and its metadata from the store.

        Args:
            vector_id (int): The identifier of the vector to delete.
        """
        if vector_id in self.vector_data:
            del self.vector_data[vector_id]
            del self.metadata[vector_id]
        else:
            raise ValueError("Vector ID does not exist")

    def get_vector(self, vector_id):
        """
        Retrieve a vector and its metadata from the store.

        Args:
            vector_id (int): The identifier of the vector to retrieve.

        Returns:
            tuple: The vector and its metadata.
        """

        vector_id = int(vector_id)
        if vector_id in self.vector_data:
            return self.vector_data[vector_id], self.metadata[vector_id]
        else:
            raise ValueError("Vector ID does not exist")

    def cosine_similarity(self, a, b):
        """
        Calculate the cosine similarity between two vectors.

        Args:
            a (numpy.ndarray): First vector.
            b (numpy.ndarray): Second vector.

        Returns:
            float: Cosine similarity between the vectors.
        """
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        return dot_product / (norm_a * norm_b)
