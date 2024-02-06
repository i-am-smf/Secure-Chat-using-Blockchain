a=int(input("Enter a Number:"))


if a == 1:
    print("1 has no divide factors")
    

if a>1:
    ans=1
    for i in range(a,0,-1):
        ans*=i

    print(ans)