
import cookielib
import urllib2, urllib
import time
import re
import traceback

cj = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'),
                     ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'), 
                     ('Accept-Language', 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3'), 
                     ('Connection', 'keep-alive'), 
                     ('Host', 'www.sigmaaldrich.com'), 
                     ('Cookie', 'JSESSIONID=F1DEDA5AA51B2A6D2F3E75EC0379EEF3.stltcat01; TLTSID=7CBB232693BC10930208A9D6D34564B1; TLTUID=7CBB232693BC10930208A9D6D34564B1; GUID=ae001877-e667-484f-957d-b24cffb5c8c0|NULL|1392192257338; country=USA; SialLocaleDef=CountryCode~US|WebLang~-1|; cmTPSet=Y; SessionPersistence=CLICKSTREAMCLOUD%3A%3DvisitorId%3Danonymous%7CPROFILEDATA%3A%3Davatar%3D%2Fetc%2Fdesigns%2Fdefault%2Fimages%2Fcollab%2Favatar.png%2CauthorizableId%3Danonymous%2CauthorizableId_xss%3Danonymous%2CformattedName%3D%2CformattedName_xss%3D%7CSURFERINFO%3A%3DIP%3D141.247.239.190%2Ckeywords%3D%2Cbrowser%3DChrome%2COS%3DWindows%2Cresolution%3D1920x1080%7C; Cck=present; fsr.a=1392192378970; fsr.s={"f":1392192378655,"cp":{"REGION":"USA","ClientId":"Unknown","MemberId":"Unknown","SiteId":"SA","TLTSID":"7CBB232693BC10930208A9D6D34564B1","TLTUID":"7CBB232693BC10930208A9D6D34564B1","SialLocalDef":"CountryCode~US|WebLang~-1|"},"v":1,"rid":"d464cf6-82258558-bb67-35e3-80320","ru":"http://www.sigmaaldrich.com/catalog/search?interface=All&term=M5904-500ML&lang=en&region=US&focus=product&N=0+220003048+219853269+219853286&mode=match partialmax","r":"www.sigmaaldrich.com","st":"","to":3.1,"c":"http://www.sigmaaldrich.com/catalog/search","pv":6,"lc":{"d0":{"v":2,"s":false},"d1":{"v":4,"s":true}},"cd":1,"sd":1}')
                      ]
opener.addheaders.append( ('Accept-encoding', 'identity') )
opener.addheaders.append( ('Referer', '') )


def get_page(url, data=None):
    resp = None
    n = 0
    while n < 5:
        n = n + 1
        try:
            resp = opener.open(url, data, timeout=10)
            page = resp.read()
            return page
        except:
            traceback.print_exc()
            print "Will try after 2 seconds ..."
            time.sleep(2.0)
            continue
        break
    return "Null"


open("price.csv", "w").write("name,price\n")

lines = open("data.txt").readlines()

for line in lines:

    try:
        pname = line.strip()

        if pname:

            print pname
            ptype = pname.split("-")[0]

            url = "http://www.sigmaaldrich.com/catalog/search/SearchResultsPage?Query=%s&Scope=SearchAll"%pname
            p = get_page(url)

            brand = re.findall(r'href="/catalog/product/(.*?)/', p)[0]
            brand = brand.upper()

            link = "http://www.sigmaaldrich.com/catalog/PricingAvailability.do?productNumber=%s&brandKey=%s&divId=pricingContainerMessage&loadFor=PRD_RS"%(ptype, brand)

            p = get_page(link)
            price = re.findall(r"<p>%s</p>.*?class='price'.*?<p>(.*?)</p>"%pname, p)[0]

            print price
            
            open("price.csv", "a").write("%s,%s\n"%(pname, price))

    except:
        print "Err"

input("Finish! press Enter to exit")

