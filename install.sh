#!/usr/bin/env bash
# wtfgit installer — curl -fsSL https://raw.githubusercontent.com/Mungbeanbeanie/wtfgit/main/install.sh | bash
set -euo pipefail

RAW_URL="https://raw.githubusercontent.com/Mungbeanbeanie/wtfgit/main/wtfgit"
BIN_DIR="${HOME}/.local/bin"

command -v python3 >/dev/null 2>&1 || {
    echo "wtfgit needs python3, which wasn't found. Install it from https://python.org first."
    exit 1
}
command -v git >/dev/null 2>&1 || {
    echo "wtfgit diagnoses git, but git itself isn't installed. Get it at https://git-scm.com."
    exit 1
}

mkdir -p "$BIN_DIR"
curl -fsSL "$RAW_URL" -o "$BIN_DIR/wtfgit"
chmod +x "$BIN_DIR/wtfgit"

echo "✓ Installed wtfgit to $BIN_DIR/wtfgit"

case ":$PATH:" in
    *":$BIN_DIR:"*) echo "✓ Ready — cd into any repo and run: wtfgit" ;;
    *)
        echo "⚠ $BIN_DIR isn't on your PATH. Add this line to your ~/.zshrc or ~/.bashrc:"
        echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo "  then restart your terminal and run: wtfgit"
        ;;
esac
