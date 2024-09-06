import requests

def check_proxy(proxy):
    try:
        response = requests.get('https://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False

# Example usage
proxies = [
    'http://68.169.51.92:80',
    'http://159.54.145.18:80',
    'http://203.115.101.55:80',
    'http://195.189.70.51:3128',
    'http://50.174.7.154:80',
    'http://50.174.7.162:80',
    'http://207.154.219.88:80',
]

valid_proxies = [proxy for proxy in proxies if check_proxy(proxy)]
print("Valid proxies:", valid_proxies)
