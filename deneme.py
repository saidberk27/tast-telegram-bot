def addAsterisk(text):
    text = text.replace("*", "\\\*")
    print(text)


while True:
    addAsterisk(input("lutfen yazi giriniz"))
