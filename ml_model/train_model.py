#!/usr/bin/env python3
"""
ML Model Training Script for Donor Reliability Prediction

This script trains a machine learning model to predict donor reliability
based on donation history and other factors.
"""

import sys
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import pickle
import json

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns

def generate_synthetic_data(n_samples=1000):
    """
    Generate synthetic training data for the ML model.
    This is used when there's insufficient real data.
    """
    np.random.seed(42)
    
    data = []
    
    for i in range(n_samples):
        # Generate realistic donor features
        age = np.random.normal(35, 12)
        age = max(18, min(70, age))  # Clamp to realistic range
        
        # Donation history features
        total_donations = np.random.poisson(3)  # Most donors have few donations
        successful_donations = np.random.binomial(total_donations, 0.85)  # 85% success rate
        
        success_rate = (successful_donations / total_donations * 100) if total_donations > 0 else 0
        
        # Response time (hours) - log-normal distribution
        avg_response_time = np.random.lognormal(2.5, 1.0)  # Mean ~12 hours
        
        # Punctuality and communication scores (0-1)
        punctuality_score = np.random.beta(2, 1)  # Slightly skewed towards higher scores
        communication_score = np.random.beta(2, 1)
        
        # Days since last donation
        days_since_last = np.random.exponential(90)  # Exponential distribution
        
        # Donation frequency (per year)
        years_active = np.random.uniform(0.5, 5)
        donation_frequency = total_donations / max(years_active, 1)
        
        # Calculate target reliability score
        # Base score from success rate
        base_score = success_rate / 100
        
        # Bonuses and penalties
        response_bonus = max(0, 1 - (avg_response_time / 48))  # Bonus for quick response
        punctuality_bonus = punctuality_score * 0.2
        communication_bonus = communication_score * 0.2
        recency_bonus = max(0, 1 - (days_since_last / 365))  # Bonus for recent activity
        frequency_bonus = min(0.1, donation_frequency / 10)  # Bonus for regular donations
        
        # Age factor (prefer donors in prime age range)
        age_factor = 0
        if 25 <= age <= 55:
            age_factor = 0.05
        
        # Calculate final reliability score
        reliability_score = (
            base_score * 0.4 +
            response_bonus * 0.2 +
            punctuality_bonus +
            communication_bonus +
            recency_bonus * 0.1 +
            frequency_bonus +
            age_factor
        )
        
        # Add some noise
        reliability_score += np.random.normal(0, 0.05)
        reliability_score = max(0.0, min(1.0, reliability_score))
        
        data.append({
            'age': age,
            'total_donations': total_donations,
            'successful_donations': successful_donations,
            'success_rate': success_rate,
            'avg_response_time': avg_response_time,
            'punctuality_score': punctuality_score,
            'communication_score': communication_score,
            'days_since_last_donation': days_since_last,
            'donation_frequency': donation_frequency,
            'reliability_score': reliability_score
        })
    
    return pd.DataFrame(data)

def train_model_with_synthetic_data():
    """
    Train the model using synthetic data.
    """
    print("Generating synthetic training data...")
    df = generate_synthetic_data(n_samples=2000)
    
    # Feature columns
    feature_columns = [
        'age', 'total_donations', 'successful_donations', 'success_rate',
        'avg_response_time', 'punctuality_score', 'communication_score',
        'days_since_last_donation', 'donation_frequency'
    ]
    
    X = df[feature_columns].values
    y = df['reliability_score'].values
    
    print(f"Training data shape: {X.shape}")
    print(f"Target distribution:")
    print(f"  Mean: {y.mean():.3f}")
    print(f"  Std: {y.std():.3f}")
    print(f"  Min: {y.min():.3f}")
    print(f"  Max: {y.max():.3f}")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train model
    print("\nTraining Random Forest model...")
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate model
    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)
    
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    print(f"\nModel Performance:")
    print(f"  Training R²: {train_r2:.3f}")
    print(f"  Testing R²: {test_r2:.3f}")
    print(f"  Training RMSE: {train_rmse:.3f}")
    print(f"  Testing RMSE: {test_rmse:.3f}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='r2')
    print(f"  Cross-validation R²: {cv_scores.mean():.3f} (+/- {cv_scores.std() * 2:.3f})")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print(f"\nFeature Importance:")
    for _, row in feature_importance.iterrows():
        print(f"  {row['feature']}: {row['importance']:.3f}")
    
    # Save model
    model_data = {
        'model': model,
        'scaler': scaler,
        'feature_names': feature_columns,
        'train_r2': train_r2,
        'test_r2': test_r2,
        'train_rmse': train_rmse,
        'test_rmse': test_rmse,
        'cv_scores': cv_scores.tolist(),
        'feature_importance': feature_importance.to_dict('records'),
        'training_date': datetime.utcnow().isoformat(),
        'data_source': 'synthetic'
    }
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname('donor_reliability_model.pkl'), exist_ok=True)
    
    with open('donor_reliability_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)
    
    print(f"\nModel saved to: donor_reliability_model.pkl")
    
    # Save feature importance plot
    plt.figure(figsize=(10, 6))
    sns.barplot(data=feature_importance, x='importance', y='feature')
    plt.title('Feature Importance for Donor Reliability Prediction')
    plt.xlabel('Importance')
    plt.tight_layout()
    plt.savefig('feature_importance.png', dpi=300, bbox_inches='tight')
    print(f"Feature importance plot saved to: feature_importance.png")
    
    return model_data

def create_model_metadata():
    """
    Create metadata file with model information.
    """
    metadata = {
        "model_name": "Donor Reliability Predictor",
        "version": "1.0.0",
        "description": "Random Forest model for predicting donor reliability based on donation history and behavior patterns",
        "features": [
            "age",
            "total_donations", 
            "successful_donations",
            "success_rate",
            "avg_response_time",
            "punctuality_score",
            "communication_score",
            "days_since_last_donation",
            "donation_frequency"
        ],
        "target": "reliability_score (0-1)",
        "algorithm": "Random Forest Regressor",
        "hyperparameters": {
            "n_estimators": 100,
            "max_depth": 10,
            "min_samples_split": 5,
            "min_samples_leaf": 2
        },
        "training_data": {
            "source": "synthetic",
            "samples": 2000,
            "features": 9
        },
        "performance_metrics": {
            "expected_r2": "0.75-0.85",
            "expected_rmse": "0.08-0.12"
        },
        "usage": {
            "input_format": "numpy array with 9 features",
            "output_format": "float between 0 and 1",
            "preprocessing": "StandardScaler required"
        }
    }
    
    with open('model_metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"Model metadata saved to: model_metadata.json")

if __name__ == "__main__":
    print("=" * 60)
    print("Donor Reliability Model Training")
    print("=" * 60)
    
    try:
        # Train model with synthetic data
        model_data = train_model_with_synthetic_data()
        
        # Create metadata
        create_model_metadata()
        
        print("\n" + "=" * 60)
        print("Training completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError during training: {e}")
        sys.exit(1)