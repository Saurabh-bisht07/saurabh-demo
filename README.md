# Blood & Organ Donation Matcher Web App

A comprehensive full-stack application that connects blood and organ donors with patients in need, featuring intelligent matching algorithms and real-time notifications.

## Features

- **Donor Registration**: Blood group, location, and medical history tracking
- **Patient Search**: Find nearest compatible donors with location-based matching
- **Smart Matching**: ML-powered donor reliability prediction based on donation history
- **Real-time Notifications**: SMS and email alerts for urgent requests
- **Location Services**: Geospatial matching for optimal donor-patient pairing
- **Admin Dashboard**: Comprehensive management interface

## Tech Stack

- **Frontend**: React with TypeScript, Material-UI, Mapbox for location services
- **Backend**: Python FastAPI with async/await support
- **Database**: PostgreSQL with PostGIS for geospatial queries
- **ML Model**: Scikit-learn for donor reliability prediction
- **Notifications**: Twilio SMS + SendGrid email integration
- **Authentication**: JWT-based secure authentication

## Project Structure

```
donation-matcher/
├── frontend/          # React TypeScript application
├── backend/           # FastAPI Python application
├── ml_model/          # Machine learning models
├── database/          # Database migrations and schemas
└── docs/             # API documentation
```

## Quick Start

1. **Setup Database**:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Start Backend**:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

3. **Start Frontend**:
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. **Setup ML Model**:
   ```bash
   cd ml_model
   python train_model.py
   ```

## Environment Variables

Create `.env` files in both frontend and backend directories with:

**Backend (.env)**:
```
DATABASE_URL=postgresql://user:password@localhost/donation_matcher
JWT_SECRET=your-secret-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
SENDGRID_API_KEY=your-sendgrid-key
```

**Frontend (.env)**:
```
REACT_APP_API_URL=http://localhost:8000
REACT_APP_MAPBOX_TOKEN=your-mapbox-token
```

## API Endpoints

- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User authentication
- `POST /api/donors` - Register as donor
- `GET /api/donors/search` - Search for donors
- `POST /api/requests` - Create donation request
- `GET /api/requests` - Get donation requests
- `POST /api/notifications` - Send notifications

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details 
