# snaplens – Automated Web Preview & Screenshot Tool

snaplens is a lightweight automation tool that:

- takes a user-provided search query  
- fetches top results from DuckDuckGo  
- visits each website in a headless browser  
- captures full-page screenshots (stitched from multiple scrolls)  
- generates a clean, static HTML gallery with Base64-embedded images  

This makes it easier to visually inspect websites quickly during reconnaissance, OSINT work, or general research.

---

## ✨ Features

- **Automated Search**
  - Fetches top results from DuckDuckGo using a simple HTML interface.
  - No API keys or authentication needed.

- **Full-Page Screenshots**
  - Uses Selenium to capture scrollable, stitched screenshots.
  - Optionally supports JS-disabled mode for better stability on bot-protected sites.

- **Parallel Processing**
  - Captures multiple screenshots at the same time for faster performance.

- **Static HTML Report**
  - All screenshots are embedded as Base64.
  - Creates a single portable `output.html` file.
  - No external folders or image files required.

- **Local-Only**
  - No screenshot data or search history is uploaded anywhere.
  - All processing happens on the user’s machine.

---

## 🚀 Installation

Install the required Python packages:

```bash
pip install selenium webdriver-manager pillow requests beautifulsoup4
