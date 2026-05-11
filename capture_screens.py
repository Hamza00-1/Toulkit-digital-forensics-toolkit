import time
from playwright.sync_api import sync_playwright

def take_screenshots():
    print("[*] Starting Playwright...")
    with sync_playwright() as p:
        # Launch Chromium visually so we can take screenshots, but headless is cleaner
        # we will use dark mode preference
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            color_scheme='dark'
        )
        page = context.new_page()
        
        base_url = "http://127.0.0.1:5000"
        
        screens = {
            "web_dashboard": "/",
            "log_analyzer": "/logs",
            "metadata_extractor": "/metadata",
            "virus_hasher": "/hasher"
        }
        
        import os
        os.makedirs("docs/screenshots", exist_ok=True)
        
        for name, route in screens.items():
            print(f"[*] Capturing {name}...")
            # Route to page
            page.goto(base_url + route)
            
            # Additional UI interactions if needed (e.g. click a button to show some data)
            time.sleep(1) # wait for animations to settle
            
            path = f"docs/screenshots/{name}.png"
            page.screenshot(path=path)
            print(f"[+] Saved {path}")
            
        browser.close()
        print("[*] Finished capturing all screenshots.")

if __name__ == "__main__":
    take_screenshots()
