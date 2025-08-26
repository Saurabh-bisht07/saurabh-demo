import pickle
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session

from app.models.donor import Donor
from app.models.donation_history import DonationHistory, DonationOutcome
from app.core.config import settings

class DonorReliabilityPredictor:
    """ML model for predicting donor reliability scores."""
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = [
            'age', 'total_donations', 'successful_donations', 'success_rate',
            'avg_response_time', 'punctuality_score', 'communication_score',
            'days_since_last_donation', 'donation_frequency'
        ]
    
    def load_model(self, model_path: str = None):
        """Load the trained model from file."""
        if model_path is None:
            model_path = settings.ML_MODEL_PATH
        
        try:
            if os.path.exists(model_path):
                with open(model_path, 'rb') as f:
                    model_data = pickle.load(f)
                    self.model = model_data['model']
                    self.scaler = model_data['scaler']
                return True
            else:
                print(f"Model file not found: {model_path}")
                return False
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def extract_features(self, donor: Donor, db: Session) -> np.ndarray:
        """Extract features from donor data for prediction."""
        # Get donation history
        history = db.query(DonationHistory).filter(
            DonationHistory.donor_id == donor.id
        ).all()
        
        # Basic donor features
        age = donor.age
        total_donations = len(history)
        successful_donations = len([h for h in history if h.outcome == DonationOutcome.SUCCESSFUL])
        success_rate = (successful_donations / total_donations * 100) if total_donations > 0 else 0
        
        # Calculate response time and punctuality
        response_times = []
        punctuality_scores = []
        communication_scores = []
        
        for record in history:
            if record.response_time_hours is not None:
                response_times.append(record.response_time_hours)
            if record.punctuality_score is not None:
                punctuality_scores.append(record.punctuality_score)
            if record.communication_score is not None:
                communication_scores.append(record.communication_score)
        
        avg_response_time = np.mean(response_times) if response_times else 24.0  # Default 24 hours
        punctuality_score = np.mean(punctuality_scores) if punctuality_scores else 0.5
        communication_score = np.mean(communication_scores) if communication_scores else 0.5
        
        # Days since last donation
        if donor.last_donation_date:
            days_since_last = (datetime.utcnow() - donor.last_donation_date).days
        else:
            days_since_last = 365  # Default to 1 year if no previous donations
        
        # Donation frequency (donations per year)
        if total_donations > 0 and donor.created_at:
            years_active = (datetime.utcnow() - donor.created_at).days / 365.25
            donation_frequency = total_donations / max(years_active, 1)
        else:
            donation_frequency = 0
        
        # Create feature array
        features = np.array([
            age, total_donations, successful_donations, success_rate,
            avg_response_time, punctuality_score, communication_score,
            days_since_last, donation_frequency
        ]).reshape(1, -1)
        
        return features
    
    def predict(self, donor: Donor, db: Session) -> float:
        """Predict reliability score for a donor."""
        if self.model is None:
            # Load model if not loaded
            if not self.load_model():
                # Return default score if model not available
                return self._calculate_default_score(donor, db)
        
        try:
            # Extract features
            features = self.extract_features(donor, db)
            
            # Scale features if scaler is available
            if self.scaler is not None:
                features = self.scaler.transform(features)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            
            # Ensure prediction is between 0 and 1
            return max(0.0, min(1.0, prediction))
            
        except Exception as e:
            print(f"Error in prediction: {e}")
            # Return default score on error
            return self._calculate_default_score(donor, db)
    
    def _calculate_default_score(self, donor: Donor, db: Session) -> float:
        """Calculate a default reliability score when ML model is not available."""
        # Get donation history
        history = db.query(DonationHistory).filter(
            DonationHistory.donor_id == donor.id
        ).all()
        
        total_donations = len(history)
        successful_donations = len([h for h in history if h.outcome == DonationOutcome.SUCCESSFUL])
        
        # Base score from success rate
        if total_donations > 0:
            success_rate = successful_donations / total_donations
        else:
            success_rate = 0.5  # Default for new donors
        
        # Bonus for being available
        availability_bonus = 0.1 if donor.is_available else 0
        
        # Bonus for recent activity
        recency_bonus = 0
        if donor.last_donation_date:
            days_since = (datetime.utcnow() - donor.last_donation_date).days
            if days_since < 30:
                recency_bonus = 0.1
            elif days_since < 90:
                recency_bonus = 0.05
        
        # Age factor (prefer donors in prime age range)
        age_factor = 0
        if 18 <= donor.age <= 65:
            age_factor = 0.05
        
        # Calculate final score
        final_score = success_rate + availability_bonus + recency_bonus + age_factor
        
        return max(0.0, min(1.0, final_score))

# Global predictor instance
_predictor = None

def get_predictor() -> DonorReliabilityPredictor:
    """Get or create the global predictor instance."""
    global _predictor
    if _predictor is None:
        _predictor = DonorReliabilityPredictor()
        _predictor.load_model()
    return _predictor

def predict_donor_reliability(donor: Donor, db: Session = None) -> float:
    """Predict reliability score for a donor."""
    predictor = get_predictor()
    
    if db is None:
        # If no DB session provided, return a default score
        return 0.5
    
    return predictor.predict(donor, db)

def train_model(db: Session, save_path: str = None) -> bool:
    """Train the donor reliability prediction model."""
    if save_path is None:
        save_path = settings.ML_MODEL_PATH
    
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.preprocessing import StandardScaler
        from sklearn.model_selection import train_test_split
        
        # Get all donors with donation history
        donors = db.query(Donor).all()
        
        features_list = []
        scores_list = []
        
        predictor = DonorReliabilityPredictor()
        
        for donor in donors:
            # Extract features
            features = predictor.extract_features(donor, db)
            
            # Calculate actual reliability score (target)
            # This would ideally come from feedback/ratings
            # For now, we'll use a heuristic based on donation history
            history = db.query(DonationHistory).filter(
                DonationHistory.donor_id == donor.id
            ).all()
            
            total_donations = len(history)
            successful_donations = len([h for h in history if h.outcome == DonationOutcome.SUCCESSFUL])
            
            if total_donations > 0:
                # Calculate target score based on success rate and other factors
                success_rate = successful_donations / total_donations
                
                # Additional factors
                availability_bonus = 0.1 if donor.is_available else 0
                recency_bonus = 0
                if donor.last_donation_date:
                    days_since = (datetime.utcnow() - donor.last_donation_date).days
                    if days_since < 30:
                        recency_bonus = 0.1
                    elif days_since < 90:
                        recency_bonus = 0.05
                
                target_score = success_rate + availability_bonus + recency_bonus
                target_score = max(0.0, min(1.0, target_score))
            else:
                # For donors with no history, use a default score
                target_score = 0.5
            
            features_list.append(features.flatten())
            scores_list.append(target_score)
        
        if len(features_list) < 10:
            print("Not enough data to train model")
            return False
        
        # Convert to numpy arrays
        X = np.array(features_list)
        y = np.array(scores_list)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train model
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        model.fit(X_train_scaled, y_train)
        
        # Evaluate model
        train_score = model.score(X_train_scaled, y_train)
        test_score = model.score(X_test_scaled, y_test)
        
        print(f"Model training completed:")
        print(f"Training R² score: {train_score:.3f}")
        print(f"Testing R² score: {test_score:.3f}")
        
        # Save model
        model_data = {
            'model': model,
            'scaler': scaler,
            'feature_names': predictor.feature_names,
            'train_score': train_score,
            'test_score': test_score
        }
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        # Update global predictor
        global _predictor
        _predictor = predictor
        _predictor.model = model
        _predictor.scaler = scaler
        
        return True
        
    except Exception as e:
        print(f"Error training model: {e}")
        return False