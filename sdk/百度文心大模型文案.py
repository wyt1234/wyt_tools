import requests
import urllib

# 文案生成


def f(text, minDecLen=32, seqLen=1000):
    url = "https://wenxin.baidu.com/moduleApi/portal/api/invoke"

    # 转url编码
    text_url = urllib.parse.quote(text)
    payload = f'text={text_url}&modelId=1&minDecLen={minDecLen}&seqLen={seqLen}&topp=0.9&penaltyScore=1.2&apiId=20022&taskPrompt=1.0%2Cadtext%2C1.0%2C1.0%2C%2C%2C%2C0%2C1'
    headers = {
        'Cookie': 'BIDUPSID=75F09E27BF7453004FEB6F9B8E1BE3F3; PSTM=1641951942; BAIDUID=75F09E27BF745300136436BD9D34270C:FG=1; __yjs_duid=1_5a49405dc8d7bb5405048a1e2bd768e01642483795912; BDUSS=0dTNEI4eDJCWk43c1RWZGJNZ2M4bVA0SVczUGM1Q1FLVzM5eUhiYkZWTkhuelJpSVFBQUFBJCQAAAAAAAAAAAEAAABpAEpGveCw18Dxt~4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEcSDWJHEg1iM; BDUSS_BFESS=0dTNEI4eDJCWk43c1RWZGJNZ2M4bVA0SVczUGM1Q1FLVzM5eUhiYkZWTkhuelJpSVFBQUFBJCQAAAAAAAAAAAEAAABpAEpGveCw18Dxt~4AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEcSDWJHEg1iM; ZFY=rDv6:ACSH2aExNwTrJaz5nzhGNrY2ZeL45GqCj9nRf:B8:C; BAIDUID_BFESS=75F09E27BF745300136436BD9D34270C:FG=1; BDRCVFR[mkUqnUt8juD]=mk3SLVN4HKm; H_PS_PSSID=36548_37356_37300_37486_37403_37398_36789_26350_37365_37461; BA_HECTOR=210g8k0k01a42l200k0ka1ln1hjlr0o1b; delPer=1; PSINO=7; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BCLID=6789564938451441140; BCLID_BFESS=6789564938451441140; BDSFRCVID=FDtOJexroG0u3HJjM9Vmbo1eV9HDvd6TDYrEALqZNdWfoxAVJeC6EG0Pts1-dEu-EHtdogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; BDSFRCVID_BFESS=FDtOJexroG0u3HJjM9Vmbo1eV9HDvd6TDYrEALqZNdWfoxAVJeC6EG0Pts1-dEu-EHtdogKK3gOTH4PF_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF=tR3f0Rry2Ru_HRjYbb__-P4DePjR-URZ56bHWh0MbCO1ORcEeqjV-4RLbJD8BU3q5ncnKUT-3ljdqfc8bhJthnkF346-35543bRTLP8hHRbpfj6HybOfhP-UyNbMWh37JNRlMKoaMp78jR093JO4y4Ldj4oxJpOJ5JbMopCafJOKHICRDT8h3e; H_BDCLCKID_SF_BFESS=tR3f0Rry2Ru_HRjYbb__-P4DePjR-URZ56bHWh0MbCO1ORcEeqjV-4RLbJD8BU3q5ncnKUT-3ljdqfc8bhJthnkF346-35543bRTLP8hHRbpfj6HybOfhP-UyNbMWh37JNRlMKoaMp78jR093JO4y4Ldj4oxJpOJ5JbMopCafJOKHICRDT8h3e; Hm_lvt_1d14624ccaaf7fc81005e4565416f194=1664806131; Hm_lvt_ebb78972b12bd9aef5154dd056e04b1b=1664806131; Hm_lvt_89be97848720f62fa00a07b1e0d83ae6=1664806131; Hm_lpvt_ebb78972b12bd9aef5154dd056e04b1b=1664806140; Hm_lpvt_89be97848720f62fa00a07b1e0d83ae6=1664806140; Hm_lpvt_1d14624ccaaf7fc81005e4565416f194=1664806140; Hm_lvt_56eff24245c08a007389c15d2e7ee0eb=1664806142; Hm_lpvt_56eff24245c08a007389c15d2e7ee0eb=1664806142; ab_sr=1.0.1_NDVkYTkwNmE5NDFjZTc3OTI1ZDZiZTZjNjJkYzc0ODA0ODhjZjY4MWU2NGJhMDQwOTE1M2JmMzcwZjViMDMzMzc0NWI4ZWE0ZGJjZjhmMmIzMDUyNjE1Y2NjM2M0ODNlZTgyMWY0ZGQ1ZmJjOGE5NjI3ZTZhMDc4ODkwZjhiMTcxZjIzOGRkNGY1MWNjMTJkYmE3NDEzMTdmYTVkMmE3ZQ==; RT="z=1&dm=baidu.com&si=5pletzcw8hp&ss=l8sul41r&sl=b&tt=4xfp&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ul=dwlg&hd=dwlj&ld=f1k1"',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    res = str(response.json()['data']['result']).split('\n')
    for re in res:
        print(re)
    print()


if __name__ == '__main__':
    # 肖申克的救赎电影推荐\日式小户型榻榻米折叠储物收纳茶几餐桌两用简约客厅北欧小茶几\类型:裤。版型:宽松;裤型:阔腿裤|版型:宽松|材质|图案:线条;风格:性感|颜色,风格
    # 类型:上衣。颜色:绿色;衣样式:衬衫;风格:清新|衣领型:翻领;图案:线条
    # 手工日式竹编包手提包女竹包茶道手拎包茶人禅意便携茶具收纳包
    title = "零卡糖代糖赤藓糖醇甜菊糖无糖0卡糖代替白砂糖0糖0脂红烧"
    for i in range(3):
        f(title, minDecLen=2, seqLen=256)
