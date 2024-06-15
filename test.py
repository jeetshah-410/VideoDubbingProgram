def add_comma(string):
    specific_words = ["mobile", "screwdriver", "Trademark"]
    for word in specific_words:
        string = string.replace(word, word + ',')
    return string

sent = "hello"
punct = add_comma(sent)  
print(punct) 
