from __future__ import annotations
from typing import List, Tuple
import numpy as np
from sklearn.linear_model import LogisticRegression
from ..db.session import SessionLocal
from ..db.models import Donor
import logging

logger = logging.getLogger(__name__)

class MLService:
	def __init__(self) -> None:
		self.model: LogisticRegression | None = None
		self.is_trained: bool = False

	def _extract_features(self) -> Tuple[np.ndarray, np.ndarray, List[int]]:
		session = SessionLocal()
		try:
			donors: List[Donor] = session.query(Donor).all()
			X_list: List[List[float]] = []
			y_list: List[int] = []
			ids: List[int] = []
			for d in donors:
				total_requests = max(d.requests_count, 1)
				response_rate = d.responses_count / total_requests
				no_show_rate = d.no_show_count / max(d.donations_count + d.no_show_count, 1)
				reliability_proxy = (0.7 * response_rate) + (0.3 * (1 - no_show_rate))
				label = 1 if reliability_proxy >= 0.5 else 0
				features = [
					float(d.donations_count),
					float(d.no_show_count),
					float(d.responses_count),
					float(d.requests_count),
					float(response_rate),
					float(no_show_rate),
				]
				X_list.append(features)
				y_list.append(label)
				ids.append(d.id)
			X = np.array(X_list, dtype=float) if X_list else np.zeros((0, 6), dtype=float)
			y = np.array(y_list, dtype=int) if y_list else np.zeros((0,), dtype=int)
			return X, y, ids
		finally:
			session.close()

	def train_if_needed(self) -> None:
		try:
			X, y, _ = self._extract_features()
			if X.shape[0] >= 5 and np.unique(y).size >= 2:
				self.model = LogisticRegression(max_iter=500)
				self.model.fit(X, y)
				self.is_trained = True
				logger.info("ML model trained on %d donors", X.shape[0])
			else:
				self.model = None
				self.is_trained = False
				logger.info("Not enough data to train ML model; using heuristic ranking")
		except Exception as exc:
			logger.exception("ML training failed: %s", exc)
			self.model = None
			self.is_trained = False

	def predict_reliability(self, donors: List[Donor]) -> List[float]:
		if self.is_trained and self.model is not None:
			X = []
			for d in donors:
				total_requests = max(d.requests_count, 1)
				response_rate = d.responses_count / total_requests
				no_show_rate = d.no_show_count / max(d.donations_count + d.no_show_count, 1)
				X.append([
					float(d.donations_count),
					float(d.no_show_count),
					float(d.responses_count),
					float(d.requests_count),
					float(response_rate),
					float(no_show_rate),
				])
			probs = self.model.predict_proba(np.array(X))[:, 1]
			return probs.tolist()
		# Fallback heuristic
		scores: List[float] = []
		for d in donors:
			total_requests = max(d.requests_count, 1)
			response_rate = d.responses_count / total_requests
			no_show_rate = d.no_show_count / max(d.donations_count + d.no_show_count, 1)
			score = (0.7 * response_rate) + (0.3 * (1 - no_show_rate))
			scores.append(float(score))
		return scores

	def rank_donors(self, donors: List[Donor]) -> List[Tuple[Donor, float]]:
		scores = self.predict_reliability(donors)
		pairs = list(zip(donors, scores))
		pairs.sort(key=lambda p: p[1], reverse=True)
		return pairs

ml_service = MLService()