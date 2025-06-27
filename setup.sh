#!/bin/bash

# Media Authentication System Setup Script
echo "🚀 Setting up Media Authentication System..."

# Create necessary directories
mkdir -p uploads/{images,videos,audio,temp}
mkdir -p ml_models
mkdir -p logs
mkdir -p docs

# Setup Python backend
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Setup Node.js frontend
cd frontend
npm install
cd ..

# Create environment files
cp env.example backend/.env
cp env.example frontend/.env

# Setup monitoring
mkdir -p monitoring/{prometheus,grafana/{dashboards,datasources}}

# Create startup scripts
cat > start_backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
EOF
chmod +x start_backend.sh

cat > start_frontend.sh << 'EOF'
#!/bin/bash
cd frontend
npm start
EOF
chmod +x start_frontend.sh

cat > start_docker.sh << 'EOF'
#!/bin/bash
docker-compose up --build
EOF
chmod +x start_docker.sh

echo "🎉 Setup completed! Run ./start_backend.sh and ./start_frontend.sh to start the application." 