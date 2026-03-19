#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="/home/gabrielveliz/Github Projects/insta/.venv/bin/python"
CREDENTIALS_FILE="$ROOT_DIR/config/credentials.ini"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "No se encontró el intérprete de Python en: $PYTHON_BIN"
  echo "Revisa el entorno virtual antes de continuar."
  exit 1
fi

if [[ ! -f "$CREDENTIALS_FILE" ]]; then
  echo "No existe el archivo de credenciales: $CREDENTIALS_FILE"
  exit 1
fi

username_set="$(grep -E '^username\s*=\s*.+$' "$CREDENTIALS_FILE" || true)"
password_set="$(grep -E '^password\s*=\s*.+$' "$CREDENTIALS_FILE" || true)"
token_set="$(grep -E '^hikerapi_token\s*=\s*.+$' "$CREDENTIALS_FILE" || true)"

if [[ -z "$token_set" && ( -z "$username_set" || -z "$password_set" ) ]]; then
  echo "Debes configurar usuario+password o hikerapi_token en config/credentials.ini"
  exit 1
fi

if [[ $# -ge 1 ]]; then
  target="$1"
  shift
else
  read -r -p "Usuario objetivo (solo con autorización): " target
fi

if [[ -z "${target:-}" ]]; then
  echo "Debes indicar un usuario objetivo."
  exit 1
fi

exec "$PYTHON_BIN" "$ROOT_DIR/main.py" "$target" "$@"
