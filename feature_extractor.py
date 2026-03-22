import re
import urllib.parse

def extract_features(url):
    features = {}

    # 1. Using IP address instead of domain
    ip_pattern = re.compile(
        r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.){3}([01]?\d\d?|25[0-5])'
    )
    features['UsingIP'] = -1 if ip_pattern.search(url) else 1

    # 2. Long URL
    features['LongURL'] = -1 if len(url) >= 54 else 1

    # 3. Short URL (bit.ly, tinyurl etc)
    shorteners = r'bit\.ly|goo\.gl|tinyurl|ow\.ly|t\.co|is\.gd'
    features['ShortURL'] = -1 if re.search(shorteners, url) else 1

    # 4. @ Symbol in URL
    features['Symbol@'] = -1 if '@' in url else 1

    # 5. Redirecting // in URL
    features['Redirecting//'] = -1 if url.rfind('//') > 6 else 1

    # 6. Prefix Suffix - in domain
    domain = urllib.parse.urlparse(url).netloc
    features['PrefixSuffix-'] = -1 if '-' in domain else 1

    # 7. Sub Domains count
    subdomains = domain.split('.')
    if len(subdomains) <= 2:
        features['SubDomains'] = 1
    elif len(subdomains) == 3:
        features['SubDomains'] = 0
    else:
        features['SubDomains'] = -1

    # 8. HTTPS
    features['HTTPS'] = 1 if url.startswith('https') else -1

    # 9. Domain Registration Length (we default to 0 without WHOIS)
    features['DomainRegLen'] = 0

    # 10. Favicon (default)
    features['Favicon'] = 1

    # 11. NonStdPort
    port = urllib.parse.urlparse(url).port
    features['NonStdPort'] = -1 if port and port not in [80, 443] else 1

    # 12. HTTPS in Domain URL
    features['HTTPSDomainURL'] = -1 if 'https' in domain else 1

    # 13. Request URL (default safe)
    features['RequestURL'] = 1

    # 14. Anchor URL (default)
    features['AnchorURL'] = 0

    # 15. Links in Script Tags (default)
    features['LinksInScriptTags'] = 0

    # 16. Server Form Handler (default)
    features['ServerFormHandler'] = 0

    # 17. Info Email
    features['InfoEmail'] = -1 if 'mailto:' in url else 1

    # 18. Abnormal URL
    features['AbnormalURL'] = -1 if domain not in url else 1

    # 19. Website Forwarding (default)
    features['WebsiteForwarding'] = 0

    # 20. Status Bar Customization (default)
    features['StatusBarCust'] = 0

    # 21. Disable Right Click (default)
    features['DisableRightClick'] = 0

    # 22. Popup Window (default)
    features['UsingPopupWindow'] = 0

    # 23. Iframe (default)
    features['IframeRedirection'] = 0

    # 24. Age of Domain (default)
    features['AgeofDomain'] = 0

    # 25. DNS Recording (default)
    features['DNSRecording'] = 0

    # 26. Website Traffic (default)
    features['WebsiteTraffic'] = 0

    # 27. Page Rank (default)
    features['PageRank'] = 0

    # 28. Google Index (default)
    features['GoogleIndex'] = 1

    # 29. Links Pointing to Page (default)
    features['LinksPointingToPage'] = 0

    # 30. Stats Report (default)
    features['StatsReport'] = 0

    return list(features.values())