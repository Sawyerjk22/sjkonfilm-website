---
description: Step-by-step setup and verification for working on sjkonfilm.work on a new MacBook
---

# Workflow: MacBook Environment Setup & Verification

## Objective
Quickly configure a new MacBook to run, develop, and publish `sjkonfilm.work` with full Antigravity context and automated image processing pipelines.

## Step 1: Clone Repository
Clone the repository to your chosen local development directory:
```bash
git clone https://github.com/Sawyerjk22/sjkonfilm-website.git
cd sjkonfilm-website
```

## Step 2: Install ImageMagick via Homebrew
The image processing pipeline (`scripts/process-staging.py`) uses ImageMagick to resize scans, generate responsive WebP/AVIF variants, and inject IPTC/EXIF metadata.
If Homebrew is not yet installed:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then install ImageMagick:
```bash
brew install imagemagick
```
Verify the installation:
```bash
magick -version
```

## Step 3: Verify Python 3
macOS comes with Python 3. Verify it is available:
```bash
python3 --version
```
All scripts in `/scripts/` run on standard Python 3 with zero required pip dependencies.

## Step 4: Preview the Site Locally
Launch a local development server from the repository root:
```bash
python3 -m http.server 8000
```
Open [http://localhost:8000](http://localhost:8000) in Safari or Chrome to inspect the portfolio and galleries.

## Step 5: Test Staging Automation (Dry Run)
Verify the staging script operates without errors:
```bash
python3 scripts/process-staging.py --dry-run
```

## Step 6: Connect Antigravity
Open the repository folder in Antigravity. Antigravity will automatically discover:
- `AGENTS.md` & `GEMINI.md` at root
- `.agents/rules/project-context.md`
- `.agents/workflows/`
All persona guidelines, site architecture constraints, and current milestones are loaded instantly.
