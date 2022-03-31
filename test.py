import re

string = """Hello my Number is 123456789 and 
             my friend's number is 987654321"""
    
# A sample regular expression to find digits. 
regex = '\d+'             
    
match = re.findall(regex, string) 
print(match) 