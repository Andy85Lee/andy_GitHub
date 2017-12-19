 # -*- coding: UTF-8 -*- 
import httplib,urllib,urllib2
import time,json

def gettoken(client_id,client_secret):
    url='http://webapi.cninfo.com.cn/api-cloud-platform/oauth2/token' #api.before.com需要根据具体访问域名修改
    post_data="grant_type=client_credentials&client_id=%s&client_secret=%s"%(client_id,client_secret)
    req = urllib.urlopen(url, post_data)
    responsecontent = req.read()
    responsedict=json.loads(responsecontent)
    token=responsedict["access_token"]

    return token

def apiget(scode,edate,token):
    val={}
    val['scode']=scode
    val['edate']=edate
    val['access_token']=token
    url = "http://webapi.cninfo.com.cn/api/stock/p_stock2402" #apitest2.com需要根据具体访问域名修改
    data=urllib.urlencode(val)
    print data
    url=url+'?'+data
    #conn = httplib.HTTPConnection("webapi.cninfo.com.cn")
    #conn.request(method="GET",url=url)
    #response = conn.getresponse()
    request=urllib2.Request(url)
    response=urllib2.urlopen(request)
    rescontent= response.read()
    #print rescontent
    responsedict=json.loads(rescontent)
    resultcode=responsedict["resultcode"]
    print responsedict["resultmsg"],responsedict["resultcode"]
    if(responsedict["resultmsg"]=="success" and len(responsedict["records"])>=1):
        print 'downloading data'  #接收到的具体数据内容
        file=open('/users/andylee/andy_files/test1','w')
        file.write(str(responsedict["records"]))          #接收到的具体数据内容
        file.close()
    else:
        print 'no data'
    return resultcode

def apipost(scode,edate,tokent):
    url = "http://webapi.cninfo.com.cn/api/stock/p_stock2402"  #apitest2.com需要根据具体访问域名修改
    post_data="scode=%s&edate=%s&access_token=%s"%(scode,edate,tokent)
    req = urllib.urlopen(url, post_data)
    content = req.read()
    responsedict=json.loads(content)
    resultcode=responsedict["resultcode"]    
    print responsedict["resultmsg"],responsedict["resultcode"]
    if(responsedict["resultmsg"]=="success" and len(responsedict["records"])>=1):
        print responsedict["records"]  #接收到的具体数据内容
    else:
        print 'no data'
    return resultcode
        

if __name__=="__main__":
    client_id,client_secret="5d771dee5e244dc2a647630cf88778d2","c43bd71fc7c2483ba5e5441cd3c17ded" #client_id,client_secret通过我的凭证获取
    token=gettoken(client_id,client_secret)
    for i in range(0,1): #注：3600为循环访问API的次数
        scode='000725' #股票代码，根据自己需要传入
        edate='20171212'
        resultcode=apiget(scode=scode,edate=edate,token=token)   #以http get方法获取数据
        #resultcode=apipost(scode,edate,token) #以http post方法获取数据
        if resultcode==200:
            break
        if resultcode==405: #token失效，重新获取
            token=gettoken(client_id,client_secret)
            apiget(scode,edate,token)  #get请求
            #apipost(scode,edate,token)#post请求

        time.sleep(1)

