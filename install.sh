#!/bin/bash

# Advanced SEO Audit Tool - Installation Script
# This script sets up the SEO audit tool with all dependencies

set -e

echo "🚀 Advanced SEO Audit Tool - Installation"
echo "========================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3.8+ is installed
check_python() {
    print_status "Checking Python version..."
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        REQUIRED_VERSION="3.8"
        
        if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
            print_success "Python $PYTHON_VERSION found"
            PYTHON_CMD="python3"
        else
            print_error "Python $PYTHON_VERSION found, but Python 3.8+ is required"
            exit 1
        fi
    else
        print_error "Python 3 not found. Please install Python 3.8 or higher"
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip..."
    
    if command -v pip3 &> /dev/null; then
        print_success "pip3 found"
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        print_success "pip found"
        PIP_CMD="pip"
    else
        print_error "pip not found. Please install pip"
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating virtual environment..."
    
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
        print_success "Virtual environment activated"
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
        print_success "Virtual environment activated"
    else
        print_error "Could not find virtual environment activation script"
        exit 1
    fi
}

# Install dependencies
install_dependencies() {
    print_status "Installing dependencies..."
    
    if [ -f "requirements.txt" ]; then
        pip install --upgrade pip
        pip install -r requirements.txt
        print_success "Dependencies installed successfully"
    else
        print_error "requirements.txt not found"
        exit 1
    fi
}

# Install Chrome/Chromium for Selenium (optional)
install_chrome() {
    print_status "Checking for Chrome/Chromium..."
    
    if command -v google-chrome &> /dev/null || command -v chromium-browser &> /dev/null; then
        print_success "Chrome/Chromium found"
    else
        print_warning "Chrome/Chromium not found. Selenium features may not work."
        echo "To install Chrome:"
        echo "  Ubuntu/Debian: sudo apt-get install google-chrome-stable"
        echo "  CentOS/RHEL: sudo yum install google-chrome-stable"
        echo "  macOS: brew install --cask google-chrome"
    fi
}

# Create configuration file
create_config() {
    print_status "Creating configuration file..."
    
    if [ ! -f "config.py" ]; then
        cat > config.py << EOF
# SEO Audit Tool Configuration
# Customize these settings as needed

# Request timeouts (seconds)
REQUEST_TIMEOUT = 30
AUDIT_TIMEOUT = 300

# User agent string
USER_AGENT = "SEO-Audit-Tool/1.0"

# Flask settings
DEBUG = False
HOST = '0.0.0.0'
PORT = 5000

# Google PageSpeed Insights API Key (optional)
# Get your key at: https://developers.google.com/speed/docs/insights/v5/get-started
PAGESPEED_API_KEY = None

# Maximum concurrent audits
MAX_CONCURRENT_AUDITS = 5

# Results cache settings
CACHE_EXPIRY_HOURS = 24
MAX_CACHED_RESULTS = 100
EOF
        print_success "Configuration file created"
    else
        print_warning "Configuration file already exists"
    fi
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    # Test core imports
    python3 -c "
import requests
import bs4
import flask
from seo_audit import SEOAuditor
print('✅ Core imports successful')
"
    
    if [ $? -eq 0 ]; then
        print_success "Installation test passed"
    else
        print_error "Installation test failed"
        exit 1
    fi
}

# Create startup scripts
create_scripts() {
    print_status "Creating startup scripts..."
    
    # CLI startup script
    cat > start_cli.sh << EOF
#!/bin/bash
# Start SEO Audit Tool - CLI Mode

cd "\$(dirname "\$0")"
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
python3 seo_audit.py "\$@"
EOF
    
    # Web interface startup script
    cat > start_web.sh << EOF
#!/bin/bash
# Start SEO Audit Tool - Web Interface

cd "\$(dirname "\$0")"
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
echo "🚀 Starting SEO Audit Tool Web Interface..."
echo "📍 Open your browser to: http://localhost:5000"
echo "📚 API Documentation: http://localhost:5000/api/docs"
echo "⏹️  Press Ctrl+C to stop"
python3 web_interface.py
EOF
    
    # Demo script
    cat > start_demo.sh << EOF
#!/bin/bash
# Start SEO Audit Tool - Demo Mode

cd "\$(dirname "\$0")"
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
python3 demo.py
EOF
    
    chmod +x start_cli.sh start_web.sh start_demo.sh
    print_success "Startup scripts created"
}

# Main installation process
main() {
    echo
    print_status "Starting installation process..."
    
    check_python
    check_pip
    create_venv
    activate_venv
    install_dependencies
    install_chrome
    create_config
    create_scripts
    test_installation
    
    echo
    print_success "Installation completed successfully!"
    echo
    echo "🎉 SEO Audit Tool is ready to use!"
    echo
    echo "Quick Start:"
    echo "  📱 Web Interface:    ./start_web.sh"
    echo "  💻 Command Line:     ./start_cli.sh"
    echo "  🎮 Demo Mode:        ./start_demo.sh"
    echo
    echo "Next Steps:"
    echo "  1. (Optional) Get Google PageSpeed Insights API key"
    echo "  2. Edit config.py to customize settings"
    echo "  3. Run ./start_web.sh to start the web interface"
    echo
    echo "📚 Documentation: http://localhost:5000/api/docs"
    echo "🐛 Issues: https://github.com/yourusername/seo-audit-tool/issues"
    echo
}

# Handle script interruption
trap 'echo -e "\n${YELLOW}Installation interrupted${NC}"; exit 1' INT

# Run installation
main