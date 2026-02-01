#!/bin/bash
# ============================================
# Compile script for NHANES Iron Deficiency Study Manuscript
# ============================================

# Configuration
STUDY_DIR="/home/joshbot/NHANES_BOT/studies/iron-deficiency-women-2026-01-31"
MANUSCRIPT_DIR="${STUDY_DIR}/manuscript"
MAIN_FILE="main.tex"
OUTPUT_PDF="manuscript.pdf"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "=========================================="
echo "NHANES Iron Deficiency Study Manuscript"
echo "LaTeX Compilation Script"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "${MANUSCRIPT_DIR}/${MAIN_FILE}" ]; then
    echo -e "${RED}Error: ${MAIN_FILE} not found in ${MANUSCRIPT_DIR}${NC}"
    echo "Please run this script from the manuscript directory"
    exit 1
fi

cd "${MANUSCRIPT_DIR}"

# Check for pdflatex
if ! command -v pdflatex &> /dev/null; then
    echo -e "${RED}Error: pdflatex not found${NC}"
    echo "Please install a LaTeX distribution (e.g., TeX Live, MiKTeX)"
    exit 1
fi

echo "Step 1: First pdflatex run..."
pdflatex -interaction=nonstopmode -file-line-error "${MAIN_FILE}" 2>&1 | tee compile_log.txt

# Check for errors
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: First pdflatex run failed${NC}"
    echo "Check compile_log.txt for details"
    
    # Show first few errors
    echo ""
    echo "First errors encountered:"
    grep -A 2 "^!" compile_log.txt | head -20
    exit 1
fi

echo ""
echo "Step 2: Running BibTeX..."
bibtex main 2>&1 | tee -a compile_log.txt

if [ $? -ne 0 ]; then
    echo -e "${YELLOW}Warning: BibTeX had issues (may be missing .bib file or citations)${NC}"
    echo "Continuing with compilation..."
fi

echo ""
echo "Step 3: Second pdflatex run..."
pdflatex -interaction=nonstopmode -file-line-error "${MAIN_FILE}" 2>&1 | tee -a compile_log.txt

echo ""
echo "Step 4: Final pdflatex run (for references)..."
pdflatex -interaction=nonstopmode -file-line-error "${MAIN_FILE}" 2>&1 | tee -a compile_log.txt

# Check final status
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}==========================================${NC}"
    echo -e "${GREEN}Compilation successful!${NC}"
    echo -e "${GREEN}==========================================${NC}"
    echo ""
    echo "Output files:"
    ls -lh "${MANUSCRIPT_DIR}/${OUTPUT_PDF}" 2>/dev/null || echo "PDF not found"
    ls -lh "${MANUSCRIPT_DIR}/"*.pdf 2>/dev/null
    echo ""
    
    # Check for warnings
    WARNINGS=$(grep -c "Warning" compile_log.txt || echo "0")
    if [ "$WARNINGS" -gt 0 ]; then
        echo -e "${YELLOW}Note: ${WARNINGS} warning(s) found in compilation${NC}"
        echo "Review compile_log.txt for details"
    fi
    
    # Check for undefined references
    UNDEF=$(grep -c "undefined" compile_log.txt || echo "0")
    if [ "$UNDEF" -gt 0 ]; then
        echo -e "${YELLOW}Note: ${UNDEF} undefined reference(s) found${NC}"
        echo "This is expected if tables/figures are in separate files"
    fi
    
    # Copy to final location with study name
    FINAL_PDF="${MANUSCRIPT_DIR}/iron-deficiency-women-nhanes-manuscript.pdf"
    cp "${MANUSCRIPT_DIR}/main.pdf" "${FINAL_PDF}" 2>/dev/null || true
    
    echo ""
    echo "Manuscript saved to:"
    echo "  - ${MANUSCRIPT_DIR}/main.pdf"
    echo "  - ${FINAL_PDF}"
    
else
    echo ""
    echo -e "${RED}==========================================${NC}"
    echo -e "${RED}Compilation failed${NC}"
    echo -e "${RED}==========================================${NC}"
    echo ""
    echo "Errors found:"
    grep "^!" compile_log.txt | head -10
    echo ""
    echo "See compile_log.txt for full details"
    exit 1
fi

# Optional: Compile supplementary materials
echo ""
echo "Compiling supplementary materials..."
if [ -f "${MANUSCRIPT_DIR}/supplementary_materials.tex" ]; then
    cd "${MANUSCRIPT_DIR}"
    pdflatex -interaction=nonstopmode supplementary_materials.tex 2>&1 | tee supp_compile_log.txt
    pdflatex -interaction=nonstopmode supplementary_materials.tex 2>&1 | tee -a supp_compile_log.txt
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Supplementary materials compiled successfully${NC}"
        cp "${MANUSCRIPT_DIR}/supplementary_materials.pdf" "${MANUSCRIPT_DIR}/supplementary-materials.pdf" 2>/dev/null || true
    else
        echo -e "${YELLOW}Warning: Supplementary materials compilation had issues${NC}"
    fi
fi

echo ""
echo "=========================================="
echo "Compilation complete"
echo "=========================================="
