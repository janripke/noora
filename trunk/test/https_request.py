import urllib
import ssl

c = ssl.SSLContext(ssl.PROTOCOL_SSLv3)
print c

https_sslv3_handler = urllib.HTTPSHandler(context=ssl.SSLContext(ssl.PROTOCOL_SSLv3))
opener = urllib.build_opener(https_sslv3_handler)
urllib.install_opener(opener)
urllib.urlopen('https://fed.princeton.edu')

