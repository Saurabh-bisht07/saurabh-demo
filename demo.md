# Blood & Organ Donation Matcher - Demo Guide

## 🎯 Demo Overview

This guide will walk you through testing the key features of the Blood & Organ Donation Matcher application.

## 🚀 Quick Start Demo

### 1. Setup and Launch
```bash
# Run the setup script
./start.sh

# Start both servers
./start-dev.sh
```

### 2. Access Points
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🧪 Demo Scenarios

### Scenario 1: New User Registration & Donor Setup

1. **Register as a Donor**
   - Go to http://localhost:3000
   - Click "Get Started" → "Register"
   - Fill in registration form:
     - Name: "John Doe"
     - Email: "john@example.com"
     - Phone: "1234567890"
     - Role: "Donate blood/organs"
     - Password: "password123"

2. **Complete Donor Profile**
   - After registration, go to "Donor Registration"
   - Fill in donor details:
     - Blood Group: "A+"
     - Age: "28"
     - Location: "Mumbai, Maharashtra"
     - Can donate blood: Yes
     - Can donate organs: No

3. **Verify Profile**
   - Check "Profile" page
   - View donor statistics

### Scenario 2: Patient Request Creation

1. **Register as a Patient**
   - Open new incognito window
   - Register with different email: "patient@example.com"
   - Role: "Request donations"

2. **Create Donation Request**
   - Go to "Create Request"
   - Fill request details:
     - Blood Group: "A+"
     - Request Type: "Blood"
     - Urgency: "High"
     - Location: "Mumbai, Maharashtra"
     - Contact: "Emergency Contact"
     - Description: "Urgent blood needed for surgery"

3. **Check Matching**
   - The system should automatically find the donor from Scenario 1
   - Check notification system

### Scenario 3: Admin Dashboard

1. **Access Admin Panel**
   - Register as admin user: "admin@example.com"
   - Role: "Admin" (you may need to manually set user_type in database)

2. **View Analytics**
   - Go to Admin Dashboard
   - Check user statistics
   - View request analytics
   - Monitor donor reliability scores

3. **Train ML Model**
   - Use "Train ML Model" feature
   - Check model performance metrics

## 🔧 API Testing

### Test Authentication
```bash
# Register user
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User",
    "phone": "1234567890",
    "user_type": "patient"
  }'

# Login
curl -X POST "http://localhost:8000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123"
  }'
```

### Test Donor Search
```bash
# Search for donors (use token from login)
curl -X GET "http://localhost:8000/api/donors/search?blood_group=A+&request_type=blood&latitude=19.0760&longitude=72.8777&radius_km=50" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Test Request Creation
```bash
# Create donation request
curl -X POST "http://localhost:8000/api/requests/create" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "request_type": "blood",
    "blood_group": "A+",
    "latitude": 19.0760,
    "longitude": 72.8777,
    "city": "Mumbai",
    "state": "Maharashtra",
    "urgency_level": "high",
    "contact_person": "Emergency Contact",
    "contact_phone": "1234567890"
  }'
```

## 📱 Frontend Features to Test

### 1. User Interface
- ✅ Responsive design (test on mobile/tablet)
- ✅ Navigation menu and breadcrumbs
- ✅ Form validation and error handling
- ✅ Loading states and progress indicators
- ✅ Toast notifications

### 2. Authentication Flow
- ✅ Registration with validation
- ✅ Login/logout functionality
- ✅ Protected route access
- ✅ Token persistence

### 3. Donor Features
- ✅ Donor registration form
- ✅ Profile management
- ✅ Statistics display
- ✅ Availability settings

### 4. Request Features
- ✅ Request creation wizard
- ✅ Request listing and filtering
- ✅ Status tracking
- ✅ Match management

### 5. Admin Features
- ✅ Dashboard analytics
- ✅ User management
- ✅ System monitoring
- ✅ ML model controls

## 🤖 ML Model Testing

### 1. Model Training
```bash
cd ml_model
python train_model.py
```

### 2. Check Model Performance
- View training metrics in console output
- Check generated files:
  - `donor_reliability_model.pkl`
  - `feature_importance.png`
  - `model_metadata.json`

### 3. Test Predictions
- Register multiple donors with different characteristics
- Check reliability scores in admin dashboard
- Verify score updates after donations

## 📧 Notification Testing

### 1. SMS Notifications (Twilio)
- Set up Twilio credentials in `.env`
- Create urgent donation request
- Check SMS delivery

### 2. Email Notifications (SendGrid)
- Set up SendGrid credentials in `.env`
- Complete donation matching
- Check email delivery

## 🐛 Troubleshooting

### Common Issues

1. **Backend won't start**
   - Check Python version (3.8+)
   - Verify virtual environment activation
   - Check port 8000 availability

2. **Frontend won't start**
   - Check Node.js version (16+)
   - Verify npm dependencies installation
   - Check port 3000 availability

3. **Database errors**
   - Check database connection string
   - Verify PostgreSQL installation (if using)
   - Check SQLite file permissions

4. **ML model errors**
   - Install scikit-learn: `pip install scikit-learn`
   - Check Python dependencies
   - Verify model file permissions

### Debug Mode

Enable debug logging:
```bash
# Backend
export LOG_LEVEL=DEBUG
python main.py

# Frontend
REACT_APP_DEBUG=true npm start
```

## 📊 Performance Testing

### Load Testing
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test API endpoints
ab -n 100 -c 10 http://localhost:8000/health
ab -n 100 -c 10 http://localhost:8000/api/donors/search
```

### Database Performance
- Monitor query execution times
- Check connection pooling
- Verify index usage

## 🎉 Demo Completion Checklist

- ✅ Application starts successfully
- ✅ User registration works
- ✅ Donor profile creation
- ✅ Request creation and matching
- ✅ Admin dashboard access
- ✅ ML model training
- ✅ Notification system
- ✅ API documentation access
- ✅ Responsive design testing
- ✅ Error handling verification

## 📞 Support

For issues during demo:
1. Check console logs for errors
2. Verify environment variables
3. Test individual components
4. Check network connectivity
5. Review API documentation

---

**Happy Testing! 🚀**