print ("Fibonacci")

m=0
n=0

while m<100000:
    if m==0:
        print(m)
        m=m+1
        print(m)
    print(m+n)
    n=m+n
    print(n+m)
    m=m+n
