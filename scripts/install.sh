#!/bin/sh
# install.sh — macOS/Linux installer for pdf-diff
# Run with: sh install.sh

echo "Installing pdf-diff..."

# Install uv if not already present
if ! command -v uv >/dev/null 2>&1; then
    echo "uv not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Refresh PATH so uv is available in the current session
    export PATH="$HOME/.local/bin:$PATH"

    if ! command -v uv >/dev/null 2>&1; then
        echo "uv installation failed. Please restart your terminal and re-run this script."
        exit 1
    fi
    echo "uv installed successfully."
else
    echo "uv already installed."
fi

# Install pdf-diff
echo "Installing pdf-diff tool..."
uv tool install git+https://github.com/damilojohn/PDF-Diff.git

if [ $? -eq 0 ]; then
    echo ""
    echo "pdf-diff installed successfully!"
    echo "Usage: pdf-diff doc_a.pdf doc_b.pdf"
else
    echo "Installation failed. Please check the error above."
    exit 1
fi
