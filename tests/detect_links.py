from url_regex import UrlRegex

# Expected result: domain=youtube.com
check1 = UrlRegex("https://www.youtube.com/test_url")

# Expected result: domain=youtube.com
check2 = UrlRegex("https://youtube.com/test_url")

# Expected result: domain=youtube.com
check3 = UrlRegex("youtube.com/test_url")

# Expected result: domain=youtube.com
check4 = UrlRegex("www.youtube.com/test_url")

print(check1.debug)
print("---------------------")
print(check2.debug)
print("---------------------")
print(check3.debug)
print("---------------------")
print(check4.debug)
