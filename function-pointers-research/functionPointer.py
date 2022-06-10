def f(text):
    print(text)

testing = f

testing("Some text")

# By dictionary
a_dictionary = {"functionPointer": f}

a_dictionary["functionPointer"]("sending text to stored function in dictionary")