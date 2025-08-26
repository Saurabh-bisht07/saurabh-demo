#!/bin/bash

echo "🚀 Starting Blood & Organ Donation Matcher Web App"
echo "=================================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16+ first."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create virtual environment if it doesn't exist
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
fi

# Activate virtual environment and install dependencies
echo "📦 Installing Python dependencies..."
cd backend
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install
cd ..

# Create environment files if they don't exist
if [ ! -f "backend/.env" ]; then
    echo "🔧 Creating backend environment file..."
    cat > backend/.env << EOF
DATABASE_URL=sqlite:///./donation_matcher.db
JWT_SECRET=your-secret-key-change-in-production
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
SENDGRID_API_KEY=your-sendgrid-key
EOF
fi

if [ ! -f "frontend/.env" ]; then
    echo "🔧 Creating frontend environment file..."
    cat > frontend/.env << EOF
REACT_APP_API_URL=http://localhost:8000
REACT_APP_MAPBOX_TOKEN=your-mapbox-token
EOF
fi

# Train ML model
echo "🤖 Training ML model..."
cd ml_model
python train_model.py
cd ..

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "To start the application:"
echo "1. Backend: cd backend && source venv/bin/activate && python main.py"
echo "2. Frontend: cd frontend && npm start"
echo ""
echo "Or run: ./start-dev.sh to start both simultaneously"
echo ""
echo "📱 Frontend will be available at: http://localhost:3000"
echo "🔧 Backend API will be available at: http://localhost:8000"
echo "📚 API Documentation will be available at: http://localhost:8000/docs"