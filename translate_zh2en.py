from deep_translator import GoogleTranslator

text = input("请输入中文：")
result = GoogleTranslator(source='zh-CN', target='en').translate(text)
print("英文翻译：", result)
