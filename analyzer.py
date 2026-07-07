import re
from urllib.parse import urlparse


class URLAnalyzer:


    def __init__(self):

        self.suspicious_words = [
            "login",
            "verify",
            "account",
            "secure",
            "update",
            "password",
            "bank",
            "confirm"
        ]


    def analyze(self, url):

        score = 0
        warnings = []


        if not url.startswith(
            ("http://", "https://")
        ):
            url = "http://" + url


        parsed = urlparse(url)


        if parsed.scheme != "https":

            score += 20

            warnings.append(
                "Website does not use HTTPS"
            )


        if self.has_ip_address(parsed.hostname):

            score += 30

            warnings.append(
                "URL contains an IP address"
            )


        keyword_result = self.check_keywords(url)


        if keyword_result:

            score += 25

            warnings.append(
                "Suspicious keywords detected"
            )


        if len(url) > 75:

            score += 15

            warnings.append(
                "URL is unusually long"
            )


        if self.has_many_symbols(url):

            score += 10

            warnings.append(
                "URL contains many special characters"
            )


        if score >= 60:

            level = "High Risk"

        elif score >= 30:

            level = "Medium Risk"

        else:

            level = "Low Risk"



        return {

            "url": url,

            "risk_score": score,

            "risk_level": level,

            "warnings": warnings

        }



    def has_ip_address(self, hostname):

        if not hostname:
            return False


        pattern = r"^\d{1,3}(\.\d{1,3}){3}$"

        return re.match(
            pattern,
            hostname
        ) is not None



    def check_keywords(self, url):

        url = url.lower()


        for word in self.suspicious_words:

            if word in url:

                return True


        return False



    def has_many_symbols(self, url):

        symbols = [
            "@",
            "%",
            "=",
            "&"
        ]


        count = 0


        for symbol in symbols:

            count += url.count(symbol)


        return count >= 3
