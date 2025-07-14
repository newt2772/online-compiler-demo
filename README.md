# online-compiler-demo

https://allthepics.net/image/Screenshot-2025-07-13-221219.QjVj1https://allthepics.net/image/Screenshot-2025-07-13-221219.QjVj1

A minimal online C++ compiler built with Flask, running entirely in GitHub Codespaces. Perfect for quick code testing without local setup.

## Features

- 💻 Compile and run C++ code in-browser
- ⚡ Real-time output display
- 📱 Responsive web interface
- 🐳 Containerized development environment
- 🔒 No persistent storage (ephemeral execution)

## Tech Stack

| Component       | Technology |
|----------------|------------|
| Backend        | Python/Flask |
| Frontend       | HTML5, CSS3, Vanilla JS |
| Compiler       | GCC (g++) |
| Deployment     | GitHub Codespaces |
| WSGI Server    | Waitress (production-ready) |

## Getting Started

### Prerequisites
- GitHub account
- Basic familiarity with Codespaces

### Installation
1. **Open in Codespaces**:
   - Click "Code" → "Codespaces" → "New codespace"
   
2. **Automatic Setup**:
   - The dev container will:
     - Install g++ compiler
     - Set up Python environment
     - Forward port 5000

### Usage
1. Start the server:
   ```bash
   python3 src/app.py