arr=[]

with open('banned_tags.txt','r',encoding='utf-8') as text:
    arr=text.readlines() 
    print(len(arr))

for i in set(arr):
    if arr.count(i) > 1:del arr[arr.index(i)]

with open('tags.txt',mode='r',encoding='utf-8') as file:
    
    global data
    data = file.readlines()
    print(len(data))

    
def filter():        
    for tag in data:
        tag=tag.replace('#','')
        tag=tag.replace('\n','')
        tag=tag.lower()
        
        for i in arr:
            i=i.replace('#','')
            i=i.replace('\n','')
            i=i.lower()
            if i == tag:
                print(tag)
                #try:data.remove(name)
                #except:None

filter()                
r=input('\nPress Enter to close')
