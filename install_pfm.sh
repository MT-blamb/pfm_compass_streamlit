#!/bin/bash

# PFM Compass One-Click Installer
# This script automatically installs and sets up the PFM Compass application
# Compatible with macOS and Linux

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
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

# Check if running on macOS or Linux
detect_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="mac"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
    print_status "Detected OS: $OS"
}

# Check shell compatibility
check_shell() {
    print_status "Checking shell compatibility..."
    
    if [[ "$OS" == "mac" ]]; then
        # macOS 10.15+ uses zsh by default, older versions use bash
        # Both are fine, no additional installation needed
        SHELL_NAME=$(basename "$SHELL")
        print_status "Current shell: $SHELL_NAME"
        
        # zsh has been the default since macOS Catalina (2019)
        # bash is still available and supported
        # No need to install additional shells
        
        if [[ "$SHELL_NAME" != "zsh" && "$SHELL_NAME" != "bash" ]]; then
            print_warning "Uncommon shell detected: $SHELL_NAME"
            print_warning "The installer will work, but you may need to restart your terminal"
        fi
    fi
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Install Xcode Command Line Tools (macOS only)
install_xcode_tools() {
    if [[ "$OS" == "mac" ]]; then
        print_status "Checking for Xcode Command Line Tools..."
        if ! xcode-select -p &> /dev/null; then
            print_status "Installing Xcode Command Line Tools..."
            xcode-select --install
            print_warning "Please complete the Xcode installation popup, then run this script again."
            exit 0
        else
            print_success "Xcode Command Line Tools already installed"
        fi
    fi
}

# Detect shell and setup PATH appropriately
detect_and_setup_shell() {
    print_status "Setting up shell environment..."
    
    # Detect current shell
    CURRENT_SHELL=$(basename "$SHELL")
    print_status "Detected shell: $CURRENT_SHELL"
    
    # Setup Homebrew PATH for different shells
    if [[ -f "/opt/homebrew/bin/brew" ]]; then
        BREW_PATH='eval "$(/opt/homebrew/bin/brew shellenv)"'
        eval "$(/opt/homebrew/bin/brew shellenv)"
    elif [[ -f "/usr/local/bin/brew" ]]; then
        BREW_PATH='eval "$(/usr/local/bin/brew shellenv)"'
        eval "$(/usr/local/bin/brew shellenv)"
    else
        print_warning "Homebrew installation path not found"
        return
    fi
    
    # Add to appropriate shell configuration file
    case "$CURRENT_SHELL" in
        zsh)
            # zsh is default on macOS 10.15+ (already installed)
            if ! grep -q "brew shellenv" ~/.zprofile 2>/dev/null; then
                echo "$BREW_PATH" >> ~/.zprofile
                print_status "Added Homebrew to ~/.zprofile"
            fi
            if ! grep -q "brew shellenv" ~/.zshrc 2>/dev/null; then
                echo "$BREW_PATH" >> ~/.zshrc
                print_status "Added Homebrew to ~/.zshrc"
            fi
            ;;
        bash)
            if ! grep -q "brew shellenv" ~/.bash_profile 2>/dev/null; then
                echo "$BREW_PATH" >> ~/.bash_profile
                print_status "Added Homebrew to ~/.bash_profile"
            fi
            if ! grep -q "brew shellenv" ~/.bashrc 2>/dev/null; then
                echo "$BREW_PATH" >> ~/.bashrc
                print_status "Added Homebrew to ~/.bashrc"
            fi
            ;;
        *)
            # Fallback to zprofile (works for most shells on macOS)
            if ! grep -q "brew shellenv" ~/.zprofile 2>/dev/null; then
                echo "$BREW_PATH" >> ~/.zprofile
                print_status "Added Homebrew to ~/.zprofile"
            fi
            ;;
    esac
}

# Install Homebrew (macOS) or update package manager (Linux)
install_package_manager() {
    if [[ "$OS" == "mac" ]]; then
        if ! command_exists brew; then
            print_status "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            
            # Detect shell and add Homebrew to PATH
            detect_and_setup_shell
            
            print_success "Homebrew installed successfully"
        else
            print_success "Homebrew already installed"
        fi
    elif [[ "$OS" == "linux" ]]; then
        print_status "Updating package manager..."
        if command_exists apt-get; then
            sudo apt-get update
        elif command_exists yum; then
            sudo yum update
        elif command_exists dnf; then
            sudo dnf update
        fi
        print_success "Package manager updated"
    fi
}

# Install Python
install_python() {
    print_status "Checking for Python 3..."
    
    if [[ "$OS" == "mac" ]]; then
        if ! command_exists python3 || [[ $(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2) < "3.8" ]]; then
            print_status "Installing Python 3.10..."
            brew install python@3.10
            # Create symlink if needed
            if [[ -f "/opt/homebrew/bin/python3.10" ]]; then
                ln -sf /opt/homebrew/bin/python3.10 /opt/homebrew/bin/python3
            fi
        fi
    elif [[ "$OS" == "linux" ]]; then
        if ! command_exists python3 || [[ $(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2) < "3.8" ]]; then
            print_status "Installing Python 3..."
            if command_exists apt-get; then
                sudo apt-get install -y python3 python3-pip python3-venv
            elif command_exists yum; then
                sudo yum install -y python3 python3-pip
            elif command_exists dnf; then
                sudo dnf install -y python3 python3-pip
            fi
        fi
    fi
    
    # Verify Python installation
    if command_exists python3; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_success "Python $PYTHON_VERSION installed"
    else
        print_error "Failed to install Python"
        exit 1
    fi
}

# Install Git
install_git() {
    if ! command_exists git; then
        print_status "Installing Git..."
        if [[ "$OS" == "mac" ]]; then
            brew install git
        elif [[ "$OS" == "linux" ]]; then
            if command_exists apt-get; then
                sudo apt-get install -y git
            elif command_exists yum; then
                sudo yum install -y git
            elif command_exists dnf; then
                sudo dnf install -y git
            fi
        fi
        print_success "Git installed"
    else
        print_success "Git already installed"
    fi
}

# Get installation directory from user
get_installation_directory() {
    echo
    print_status "Choose installation directory:"
    echo "  1. Current directory ($(pwd))"
    echo "  2. Desktop (~Desktop/pfm_compass_streamlit)"
    echo "  3. Home directory (~/pfm_compass_streamlit)"
    echo "  4. Custom directory"
    echo
    
    while true; do
        read -p "Enter your choice (1-4): " choice
        case $choice in
            1)
                INSTALL_DIR="$(pwd)"
                PROJECT_DIR="pfm_compass_streamlit"
                FULL_PATH="$INSTALL_DIR/$PROJECT_DIR"
                break
                ;;
            2)
                INSTALL_DIR="$HOME/Desktop"
                PROJECT_DIR="pfm_compass_streamlit"
                FULL_PATH="$INSTALL_DIR/$PROJECT_DIR"
                break
                ;;
            3)
                INSTALL_DIR="$HOME"
                PROJECT_DIR="pfm_compass_streamlit"
                FULL_PATH="$INSTALL_DIR/$PROJECT_DIR"
                break
                ;;
            4)
                echo
                read -p "Enter full path for installation directory: " custom_dir
                # Expand ~ to home directory if present
                INSTALL_DIR="${custom_dir/#\~/$HOME}"
                PROJECT_DIR="pfm_compass_streamlit"
                FULL_PATH="$INSTALL_DIR/$PROJECT_DIR"
                
                # Create directory if it doesn't exist
                if [[ ! -d "$INSTALL_DIR" ]]; then
                    read -p "Directory $INSTALL_DIR doesn't exist. Create it? (y/N): " -n 1 -r
                    echo
                    if [[ $REPLY =~ ^[Yy]$ ]]; then
                        mkdir -p "$INSTALL_DIR" || {
                            print_error "Failed to create directory $INSTALL_DIR"
                            continue
                        }
                    else
                        continue
                    fi
                fi
                break
                ;;
            *)
                print_error "Invalid choice. Please enter 1, 2, 3, or 4."
                continue
                ;;
        esac
    done
    
    print_success "Installation directory: $FULL_PATH"
}

# Clone repository
clone_repository() {
    REPO_URL="https://github.com/MT-blamb/pfm_compass_streamlit.git"
    
    print_status "Checking for existing project directory..."
    
    # Navigate to installation directory
    cd "$INSTALL_DIR" || {
        print_error "Failed to navigate to $INSTALL_DIR"
        exit 1
    }
    
    if [[ -d "$PROJECT_DIR" ]]; then
        print_warning "Directory $PROJECT_DIR already exists in $INSTALL_DIR"
        read -p "Do you want to remove it and clone fresh? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$PROJECT_DIR"
            print_status "Removed existing directory"
        else
            print_status "Using existing directory"
            cd "$PROJECT_DIR"
            git pull origin main 2>/dev/null || true
            return
        fi
    fi
    
    print_status "Cloning repository to $FULL_PATH..."
    git clone "$REPO_URL" "$PROJECT_DIR" || {
        print_error "Failed to clone repository"
        exit 1
    }
    
    cd "$PROJECT_DIR"
    print_success "Repository cloned successfully to $FULL_PATH"
}

# Set up Python virtual environment
setup_virtual_environment() {
    print_status "Setting up Python virtual environment..."
    
    # Remove existing venv if it exists
    if [[ -d "venv" ]]; then
        rm -rf venv
    fi
    
    python3 -m venv venv || {
        print_error "Failed to create virtual environment"
        exit 1
    }
    
    # Activate virtual environment
    source venv/bin/activate || {
        print_error "Failed to activate virtual environment"
        exit 1
    }
    
    # Upgrade pip
    pip install --upgrade pip
    
    print_success "Virtual environment created and activated"
}

# Install Python dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    if [[ ! -f "requirements.txt" ]]; then
        print_error "requirements.txt not found"
        exit 1
    fi
    
    pip install -r requirements.txt || {
        print_error "Failed to install Python dependencies"
        exit 1
    }
    
    print_success "Python dependencies installed"
}

# Create launch scripts
create_launch_scripts() {
    print_status "Creating launch scripts..."
    
    # Simple app launcher
    cat > launch_simple.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
echo "Starting PFM Compass Simple App..."
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the application"
streamlit run app_bilingual.py
EOF
    
    # Advanced app launcher
    cat > launch_advanced.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
cd bling
echo "Starting PFM Compass Advanced App..."
echo "The app will open in your browser at http://localhost:8501"
echo "Press Ctrl+C to stop the application"
streamlit run app.py
EOF
    
    # Make scripts executable
    chmod +x launch_simple.sh
    chmod +x launch_advanced.sh
    
    print_success "Launch scripts created"
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    source venv/bin/activate
    
    # Test if streamlit is available
    if ! command_exists streamlit; then
        print_error "Streamlit not found in virtual environment"
        exit 1
    fi
    
    # Test if required files exist
    if [[ ! -f "app_bilingual.py" ]]; then
        print_error "app_bilingual.py not found"
        exit 1
    fi
    
    if [[ ! -f "bling/app.py" ]]; then
        print_error "bling/app.py not found"
        exit 1
    fi
    
    print_success "Installation test passed"
}

# Display completion message
show_completion_message() {
    echo
    echo "🎉 Installation completed successfully!"
    echo
    echo "📍 Project location: $FULL_PATH"
    echo
    echo "🚀 To run the applications:"
    echo
    echo "Option 1 - Simple App (Recommended for demos):"
    echo "  cd $FULL_PATH"
    echo "  ./launch_simple.sh"
    echo
    echo "Option 2 - Advanced App (Full features):"
    echo "  cd $FULL_PATH"
    echo "  ./launch_advanced.sh"
    echo
    echo "📖 Manual launch (if needed):"
    echo "  cd $FULL_PATH"
    echo "  source venv/bin/activate"
    echo "  streamlit run app_bilingual.py        # Simple version"
    echo "  cd bling && streamlit run app.py      # Advanced version"
    echo
    echo "🌐 The app will open automatically in your browser at http://localhost:8501"
    echo "🛑 Press Ctrl+C in the terminal to stop the application"
    echo
    echo "💡 If you encounter any issues, check the README.md file for troubleshooting tips."
    echo
    echo "📋 Quick start commands:"
    echo "  cd $FULL_PATH && ./launch_simple.sh"
}

# Main installation function
main() {
    echo "🚀 PFM Compass One-Click Installer"
    echo "=================================="
    echo
    
    # Check for sudo access early for Linux
    if [[ "$OS" == "linux" ]]; then
        print_status "Checking sudo access..."
        sudo -v || {
            print_error "This script requires sudo access for package installation"
            exit 1
        }
    fi
    
    detect_os
    check_shell
    install_xcode_tools
    install_package_manager
    install_python
    install_git
    get_installation_directory
    clone_repository
    setup_virtual_environment
    install_dependencies
    create_launch_scripts
    test_installation
    show_completion_message
}

# Handle interruption
trap 'echo -e "\n${RED}Installation interrupted${NC}"; exit 1' INT

# Run main function
main "$@"
