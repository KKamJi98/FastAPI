def doh2():
    yield "Homer: D'oh!"
    yield "Marge: D'oh!"
    yield "Bart: D'oh!"
    yield "Lisa: D'oh!"
    yield "Maggie: D'oh!"
    
    
for line in doh2():
    print(line)
