import pandas as pd
#install lxml

#tw台銀
#(a)原始-匯率+查詢鈕
i=pd.read_html('https://rate.bot.com.tw/xrt?Lang=zh-TW')
#print(len(i))
#print(i[0])

#(b)排除查詢鈕欄位
tw=i[0]
tw=tw.iloc[:,0:5]

#(c)重新命名欄
tw.columns=[u'幣別',u'台銀_現金匯率_本行買入',u'台銀_現金匯率_本行賣出',
                u'台銀_即期匯率_本行買入',u'台銀_即期匯率_本行賣出']

#(d)將幣別名稱簡化至代號
tw[u'幣別']=tw[u'幣別'].str.extract('\((\w+)\)')

#(e)將列index改為幣別中文名
tw.index=['美金','港幣','英鎊','澳幣','加幣','新幣',
            '瑞士法郎','日圓','南非幣','瑞典幣','紐元',
            '泰幣','菲國比索','印尼幣','歐元','韓元',
            '越南盾','馬幣','人民幣']

#print(tw)

#print("-------------------")



#tcb台中銀
#(a)
j=pd.read_html('https://ibank.tcbbank.com.tw/PIB/cb5/cb501005/CB501005_01.faces')
#print(len(j))
#print(j[1])

#(b)
tcb=j[1]
tcb=tcb.iloc[1:,0:5]

#(c)
tcb.columns=[u'幣別',u'台中銀_現金匯率_本行買入',u'台中銀_現金匯率_本行賣出',
            u'台中銀_即期匯率_本行買入',u'台中銀_即期匯率_本行賣出']

#(d)
tcb[u'幣別']=tcb[u'幣別'].str[-3:]

#(e)
tcb.index=['美金','港幣','英鎊','澳幣','加幣',
            '新幣','瑞士法郎','日圓','南非幣','瑞典幣',
            '紐元','歐元','人民幣']

#print(tcb)

#print("-------------------")



#yd元大
#(a)
k=pd.read_html('https://www.yuantabank.com.tw/bank/exchangeRate/hostccy.do')
#print(len(k))
#print(k[0])

#(b)
yd=k[0]
yd=yd.iloc[:,0:5]

#(c)此銀行即期匯率在前
yd.columns=[u'幣別',u'元大_即期匯率_本行買入',u'元大_即期匯率_本行賣出',
            u'元大_現金匯率_本行買入',u'元大_現金匯率_本行賣出']

#(d)
yd[u'幣別']=yd[u'幣別'].str.extract('\((\w+)\)')

#(e)
yd.index=['美金','人民幣','日圓','歐元','港幣','澳幣',
            '紐元','南非幣','加幣','英鎊','新幣',
            '瑞士法郎','瑞典幣','泰幣']

#print(yd)

#print("-------------------")



#將三間銀行合併
w=pd.merge(tw,tcb,how="outer")
x=pd.merge(w,yd,how="outer")

x.index=['美金','港幣','英鎊','澳幣','加幣','新幣',
           '瑞士法郎','日圓','南非幣','瑞典幣','紐元',
           '泰幣','菲國比索','印尼幣','歐元','韓元',
           '越南盾','馬幣','人民幣']
           
print("現在台灣銀行、台中銀行、元大銀行匯率如下表:")
print(x)

print("--------------------------------------")



#查詢功能
q=input("請輸入幣別代號:")
c=x["幣別"].str.contains(q)
print(x[c])

print("--------------------------------------")


#判斷哪間銀行換"現鈔"最划算
a=x.values

#買外幣(本行賣出)
bcash_tw=a[:,2]
bcash_tcb=a[:,6]
bcash_yd=a[:,12]
#賣外幣(本行買入)
scash_tw=a[:,1]
scash_tcb=a[:,5]
scash_yd=a[:,11]

#0=美金,1=港幣,7=日圓,14=歐元,18=人民幣
#(僅此5種外幣每間銀行皆可換現鈔)
dic = {' 美金': 0, '港幣': 1, '日圓': 7, '歐元': 14, '人民幣': 18} 
#買外幣
for key,value in dic.items(): 

    if bcash_tcb[value] > bcash_tw[value] and bcash_yd[value] > bcash_tw[value]:
        print("買",key,"_台灣銀行最划算")
    
    if bcash_tw[value] > bcash_tcb[value] and bcash_yd[value] > bcash_tcb[value]:
        print("買",key,"_台中銀行最划算")
        
    if bcash_tw[value] > bcash_yd[value] and bcash_tcb[value] > bcash_yd[value]:
        print("買",key,"_元大銀行最划算")

#賣外幣
for key,value in dic.items(): 

    if scash_tcb[value] < scash_tw[value] and scash_yd[value] < scash_tw[value]:
        print("賣",key,"_台灣銀行最划算")
    
    if scash_tw[value] < scash_tcb[value] and scash_yd[value] < scash_tcb[value]:
        print("賣",key,"_台中銀行最划算")
        
    if scash_tw[value] < scash_yd[value] and scash_tcb[value] < scash_yd[value]:
        print("賣",key,"_元大銀行最划算")