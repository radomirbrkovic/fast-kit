#!/usr/bin/env bash
set -e

echo "🔧 Setting up FastKit CLI..."

# 1. Make main.py executable
chmod +x tools/cli/main.py

# 2. Create symlink to /usr/local/bin/fastkit
if [ -L /usr/local/bin/fastkit ]; then
    sudo rm /usr/local/bin/fastkit
fi
sudo ln -s $(pwd)/tools/cli/main.py /usr/local/bin/fastkit
echo "✅ Symlink created: 'fastkit' command is now available globally."

# 3. Copy .env.example -> .env if missing
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ .env file created from .env.example"
fi

# 4. Detect OS and set python command
PYTHON_CMD="python3"
OS_TYPE=$(uname)
if [[ "$OS_TYPE" == "Darwin" ]]; then
    echo "🍏 Detected macOS"
elif [[ "$OS_TYPE" == "Linux" ]]; then
    echo "🐧 Detected Linux"
else
    echo "⚠️  Unknown OS, defaulting to python3"
fi

# 5. Create virtual environment if missing
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    $PYTHON_CMD -m venv venv
else
    echo "⚙️  Virtual environment already exists, skipping..."
fi

# 6. Activate venv and install dependencies
echo "📦 Installing dependencies..."
if [[ "$OS_TYPE" == "Darwin" ]] || [[ "$OS_TYPE" == "Linux" ]]; then
    source venv/bin/activate
fi
pip install --upgrade pip
pip install -r requirements.txt

# 7. Start Docker containers
echo "🐳 Starting Docker containers..."
docker compose up -d

echo "🎉 FastKit setup completed successfully!"
echo ""
echo "You can now use: fastkit install | fastkit run | fastkit migrate | fastkit update"
