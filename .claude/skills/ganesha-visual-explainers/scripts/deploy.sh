#!/bin/bash
set -e

HTML_FILE="${1:?使い方: deploy.sh <HTMLファイル> [スラッグ]}"
SLUG="${2:-}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
AVATARS_DIR="$(cd "$(dirname "$0")/../../.." && pwd)/assets/avatars"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

if ! command -v node &>/dev/null; then
    echo -e "${RED}エラー: Node.js がインストールされていません${NC}" >&2
    echo "Node.js をインストールしてから、もう一度試してください。" >&2
    exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
    echo -e "${RED}エラー: $HTML_FILE が見つかりません${NC}" >&2
    exit 1
fi

if [ -n "$SLUG" ]; then
    RAND=$(head -c 4 /dev/urandom | xxd -p | cut -c1-4)
    DOMAIN="ganesha-${SLUG}-${RAND}.surge.sh"
else
    DOMAIN="ganesha-$(date +%y%m%d%H%M).surge.sh"
fi

TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

# HTMLをindex.htmlとしてコピー
cp "$HTML_FILE" "$TEMP_DIR/index.html"
printf "User-agent: *\nDisallow: /\n" > "$TEMP_DIR/robots.txt"

# HTML内で参照されているアバター画像をコピー
mkdir -p "$TEMP_DIR/images"
for img in "$AVATARS_DIR"/ganesha/*.png; do
    [ -f "$img" ] && cp "$img" "$TEMP_DIR/images/"
done
for img in "$AVATARS_DIR"/natsuki/*.png; do
    [ -f "$img" ] && cp "$img" "$TEMP_DIR/images/"
done

echo -e "${YELLOW}公開中...${NC}"
npx --yes surge "$TEMP_DIR" --domain "$DOMAIN"

# デプロイ履歴を記録
touch "$SKILL_DIR/deploy-history.log"
echo "$(date '+%Y-%m-%d %H:%M:%S') | https://${DOMAIN}" >> "$SKILL_DIR/deploy-history.log"

# content.json に登録
REGISTER_SCRIPT="/Users/okumuranatsuki/Desktop/okumura_life/scripts/register-content.sh"
if [ -f "$REGISTER_SCRIPT" ]; then
    TITLE=$(sed -n 's/.*<title>\([^<]*\)<\/title>.*/\1/p' "$HTML_FILE" | head -1)
    SKILL_NAME=$(basename "$SKILL_DIR")
    PROJECT_NAME=$(basename "$(cd "$SKILL_DIR/../.." && pwd)")
    bash "$REGISTER_SCRIPT" \
        --project "$PROJECT_NAME" \
        --skill "$SKILL_NAME" \
        --title "${TITLE:-$SLUG}" \
        --slug "$SLUG" \
        --url "https://${DOMAIN}" \
        --source "$(cd "$(dirname "$HTML_FILE")" && pwd)/$(basename "$HTML_FILE")"
fi

echo ""
echo -e "${GREEN}完了！${NC}"
echo "URL: https://${DOMAIN}"

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "https://${DOMAIN}" | pbcopy
    echo -e "${GREEN}URLをクリップボードにコピーしました${NC}"
    open "https://${DOMAIN}"
elif command -v clip.exe &>/dev/null; then
    echo -n "https://${DOMAIN}" | clip.exe
    echo -e "${GREEN}URLをクリップボードにコピーしました${NC}"
    start "https://${DOMAIN}" 2>/dev/null || true
elif command -v xdg-open &>/dev/null; then
    xdg-open "https://${DOMAIN}"
fi

# 一覧ページを再ビルド＋デプロイ
INDEX_SCRIPT="/Users/okumuranatsuki/Desktop/okumura_life/scripts/build-content-index.sh"
if [ -f "$INDEX_SCRIPT" ]; then
    echo -e "${YELLOW}一覧ページを更新中...${NC}"
    bash "$INDEX_SCRIPT" --deploy
fi

echo -e "${YELLOW}削除するとき: npx surge teardown ${DOMAIN}${NC}"
