#!/usr/bin/env bash
#
# style_check.sh — Check Markdown files for AI-style writing patterns.
#
# Detects:
# 1. Banned transition words and phrases
# 2. List-stacking in body text (bullet points in paragraphs)
# 3. Empty emphasis sentences
# 4. Subjective expressions
# 5. Formatting issues (bold in body, missing blank lines)
#
# Usage:
#   bash scripts/style_check.sh chapters/introduction.md
#   bash scripts/style_check.sh chapters/*.md
#

set -euo pipefail

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Counters
total_issues=0
files_checked=0
files_clean=0

# -------------------------------------------------------------------------
# Banned patterns (English academic writing)
# -------------------------------------------------------------------------

# Mechanical transitions
BANNED_TRANSITIONS=(
    "Firstly" "Secondly" "Thirdly" "Lastly"
    "Moreover" "Furthermore" "Additionally"
    "In addition" "Besides"
)

# Empty emphasis
BANNED_EMPHASIS=(
    "It is worth noting that"
    "It should be pointed out that"
    "It is important to note that"
    "Importantly,"
    "Significantly,"
    "It is obvious that"
    "Needless to say"
    "Clearly,"
)

# Subjective expressions
BANNED_SUBJECTIVE=(
    "We believe" "We think" "We feel"
    "In our opinion" "In our view"
    "I believe" "I think" "I feel"
)

# -------------------------------------------------------------------------
# Check functions
# -------------------------------------------------------------------------

check_file() {
    local file="$1"
    local file_issues=0

    if [[ ! -f "$file" ]]; then
        echo -e "${RED}File not found: $file${NC}"
        return
    fi

    files_checked=$((files_checked + 1))

    echo "Checking: $file"

    # 1. Check banned transitions
    for pattern in "${BANNED_TRANSITIONS[@]}"; do
        count=$(grep -ciw "$pattern" "$file" 2>/dev/null || echo "0")
        if [[ "$count" -gt 0 ]]; then
            echo -e "  ${RED}✗ Banned transition: '$pattern' (found $count)${NC}"
            file_issues=$((file_issues + count))
        fi
    done

    # 2. Check banned emphasis
    for pattern in "${BANNED_EMPHASIS[@]}"; do
        count=$(grep -ci "$pattern" "$file" 2>/dev/null || echo "0")
        if [[ "$count" -gt 0 ]]; then
            echo -e "  ${RED}✗ Empty emphasis: '$pattern' (found $count)${NC}"
            file_issues=$((file_issues + count))
        fi
    done

    # 3. Check banned subjective expressions
    for pattern in "${BANNED_SUBJECTIVE[@]}"; do
        count=$(grep -ci "$pattern" "$file" 2>/dev/null || echo "0")
        if [[ "$count" -gt 0 ]]; then
            echo -e "  ${RED}✗ Subjective expression: '$pattern' (found $count)${NC}"
            file_issues=$((file_issues + count))
        fi
    done

    # 4. Check bullet lists in body text (lines starting with - or * that are not in headings)
    # Skip lines that are clearly in a checklist or plan section
    bullet_count=$(grep -cE '^\s*[-*] ' "$file" 2>/dev/null || echo "0")
    if [[ "$bullet_count" -gt 5 ]]; then
        echo -e "  ${YELLOW}⚠ Excessive bullet points: $bullet_count (consider converting to paragraphs)${NC}"
        file_issues=$((file_issues + 1))
    fi

    # 5. Check bold text in body (excluding headings and first definitions)
    bold_count=$(grep -cE '\*\*[^*]+\*\*' "$file" 2>/dev/null || echo "0")
    if [[ "$bold_count" -gt 8 ]]; then
        echo -e "  ${YELLOW}⚠ Excessive bold text: $bold_count occurrences (avoid bold in body text)${NC}"
        file_issues=$((file_issues + 1))
    fi

    # 6. Word count
    word_count=$(wc -w < "$file" 2>/dev/null || echo "0")
    echo -e "  ${GREEN}ℹ Word count: $word_count${NC}"

    # Summary for this file
    if [[ "$file_issues" -eq 0 ]]; then
        echo -e "  ${GREEN}✓ Clean${NC}"
        files_clean=$((files_clean + 1))
    else
        echo -e "  ${RED}✗ $file_issues issue(s) found${NC}"
    fi

    total_issues=$((total_issues + file_issues))
    echo ""
}

# -------------------------------------------------------------------------
# Main
# -------------------------------------------------------------------------

if [[ $# -eq 0 ]]; then
    echo "Usage: $0 <file1.md> [file2.md ...]"
    echo "  Check Markdown files for AI-style writing patterns."
    exit 1
fi

echo "=== De-AI Style Check ==="
echo ""

for f in "$@"; do
    check_file "$f"
done

echo "=== Summary ==="
echo "Files checked: $files_checked"
echo "Files clean: $files_clean"
echo "Total issues: $total_issues"
echo ""

if [[ "$total_issues" -eq 0 ]]; then
    echo -e "${GREEN}✅ All checks passed${NC}"
    exit 0
else
    echo -e "${RED}❌ Issues found — please fix before proceeding${NC}"
    exit 1
fi
