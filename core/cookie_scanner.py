try:
    import browser_cookie3
except:
    browser_cookie3 = None

class CookieScanner:
    """Scan for browser cookies"""
    
    def scan_browser_cookies(self):
        """Extract cookies from browsers"""
        cookies = []
        
        if not browser_cookie3:
            return [{"error": "browser_cookie3 not installed"}]
        
        try:
            cj = browser_cookie3.load()
            for cookie in cj:
                cookies.append({
                    "domain": cookie.domain,
                    "name": cookie.name,
                    "value": cookie.value[:50] + "..." if len(cookie.value) > 50 else cookie.value,
                    "secure": cookie.secure,
                    "expires": cookie.expires
                })
        except Exception as e:
            cookies.append({"error": str(e)})
        
        return cookies
