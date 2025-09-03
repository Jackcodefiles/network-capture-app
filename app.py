import streamlit as st
import asyncio
import sys
from playwright.sync_api import sync_playwright
import json

# Fix for Windows event loop
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

st.set_page_config(page_title="Network Capture App", layout="wide")
st.title("🌐 Network Capture (Playwright + Streamlit)")

# Sidebar inputs
st.sidebar.header("Settings")
url = st.sidebar.text_input("Target URL", "https://example.com")
keywords_input = st.sidebar.text_input("Keywords (comma separated)", "user,token,error")
keywords = [k.strip() for k in keywords_input.split(",") if k.strip()]

file_types = st.sidebar.multiselect(
    "Filter by file type",
    ["json", "html", "js", "css", "xml", "txt", "other"],
    default=["json", "html"],
)

capture_btn = st.sidebar.button("🚀 Capture Requests")


def guess_file_type(content_type: str, url: str) -> str:
    """Guess file type from content-type header or URL."""
    if not content_type:
        if url.endswith(".js"):
            return "js"
        if url.endswith(".css"):
            return "css"
        if url.endswith(".json"):
            return "json"
        if url.endswith(".xml"):
            return "xml"
        if url.endswith(".txt"):
            return "txt"
        if url.endswith(".html") or url.endswith(".htm"):
            return "html"
        return "other"

    if "json" in content_type:
        return "json"
    if "html" in content_type:
        return "html"
    if "javascript" in content_type:
        return "js"
    if "css" in content_type:
        return "css"
    if "xml" in content_type:
        return "xml"
    if "text/plain" in content_type:
        return "txt"
    return "other"


def capture_requests(url, keywords, file_types):
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        def handle_response(response):
            try:
                u = response.url
                ct = response.headers.get("content-type", "")
                ftype = guess_file_type(ct, u)

                if ftype not in file_types:
                    return  # skip unwanted file types

                body_text = ""
                try:
                    body_text = response.text()
                except Exception:
                    return  # skip binary/unreadable

                if any(kw.lower() in body_text.lower() for kw in keywords):
                    results.append(
                        {
                            "method": response.request.method,
                            "url": u,
                            "status": response.status,
                            "file_type": ftype,
                            "headers": dict(response.request.headers),
                            "post_data": response.request.post_data,
                            "body_snippet": body_text[:1000],
                        }
                    )
            except Exception as e:
                print("Error handling response:", e)

        page.on("response", handle_response)
        page.goto(url, wait_until="networkidle")
        browser.close()

    # helpers to convert into code
    def to_curl(r):
        parts = [f"curl -X {r['method']} '{r['url']}'"]
        for k, v in r["headers"].items():
            parts.append(f"-H '{k}: {v}'")
        if r["post_data"]:
            parts.append(f"--data-raw '{r['post_data']}'")
        return " \\\n  ".join(parts)

    def to_python(r):
        return f"""import requests

url = "{r['url']}"
headers = {json.dumps(r['headers'], indent=2)}
{"data = " + json.dumps(r['post_data']) if r['post_data'] else ""}
response = requests.{r['method'].lower()}(url, headers=headers{", data=data" if r['post_data'] else ""})
print(response.status_code)
print(response.text[:500])
"""

    enriched = []
    for r in results:
        enriched.append(
            {
                "method": r["method"],
                "url": r["url"],
                "status": r["status"],
                "file_type": r["file_type"],
                "curl": to_curl(r),
                "python": to_python(r),
                "body_snippet": r.get("body_snippet", ""),
            }
        )

    return enriched


if capture_btn:
    if not url:
        st.error("Please enter a valid URL.")
    else:
        with st.spinner(f"Capturing requests from {url} ..."):
            captured = capture_requests(url, keywords, file_types)

        st.success(
            f"Captured {len(captured)} matching requests (body contains keywords, type in {file_types})."
        )
        for i, r in enumerate(captured, 1):
            with st.expander(
                f"{i}. [{r['file_type']}] {r['method']} {r['status']} → {r['url']}"
            ):
                st.subheader("cURL")
                st.code(r["curl"], language="bash")
                st.subheader("Python (requests)")
                st.code(r["python"], language="python")
                if r["body_snippet"]:
                    st.subheader("Response Snippet")
                    st.code(r["body_snippet"], language="json")
