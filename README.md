# 🌐 Network Capture App

A **Streamlit + Playwright** tool to capture and analyze network requests in real-time.  
With this app, you can filter requests by file type (JSON, HTML, JS, etc.), search response bodies for keywords,  
and export them as **cURL** or **Python requests** code for easy reuse.

---

## 🚀 Features

- Capture **all network requests** from a given URL.  
- Filter responses by **file type** (`json`, `html`, `js`, `css`, `xml`, `txt`, or `other`).  
- Search response bodies for **keywords** (comma separated).  
- Export requests as:
  - **cURL commands**  
  - **Python `requests` snippets**  
- View **response body snippets** directly in the UI.  

---

## 🛠 Installation

Clone the repository:

```bash
git clone https://github.com/Jackcodefiles/network-capture-app.git
cd network-capture-app
```

Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

---

## ▶️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Then open the link in your browser (usually: [http://localhost:8501](http://localhost:8501)).  

---

## 📂 Project Structure

```
network-capture-app/
│-- app.py              # Main Streamlit application
│-- requirements.txt    # Python dependencies
│-- README.md           # Project documentation
│-- .gitignore          # Ignore unnecessary files
```

---

## 📸 Screenshots (Optional)

_Add screenshots or GIFs here to demonstrate the app UI._  

---

## 📜 License

This project is released under the **MIT License**.  
You are free to use, modify, and distribute it with attribution.  
