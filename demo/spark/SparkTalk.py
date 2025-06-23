from demo.spark import SparkApi

# 以下密钥信息从控制台获取
appid = "ffa4749a"  # 填写控制台中获取的 APPID 信息
api_secret = "YzI4YjU0YzIzMDhiNTFkM2MwYzI1NzNm"  # 填写控制台中获取的 APISecret 信息
api_key = "b45fb240f420c5319b895c804cef32ad"  # 填写控制台中获取的 APIKey 信息

# 用于配置大模型版本
# domain = "general"  # v1.5版本
# 云端环境的服务地址
# Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址

# 用于配置大模型版本
domain = "4.0Ultra"  # v2.0版本
# 云端环境的服务地址
Spark_url = "wss://spark-api.xf-yun.com/v4.0/chat"  # v2.0环境的地址

text = []


def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while (getlength(text) > 8000):
        del text[0]
    return text


if __name__ == '__main__':
    text.clear
    username = "不逆"
    while (True):
        Input = input("\n" + username + ":")
        question = checklen(getText("user", Input))
        SparkApi.answer = ""
        print("星火:", end="")
        SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
        getText("assistant", SparkApi.answer)
