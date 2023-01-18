def test(a,b, *args, **karg):
    print(a,b)
    print(args)
    print(karg)

test(10,20,30,40,50,pk=123,asdf=1234)

# 10 20
# (30, 40, 50)
# {'pk': 123, 'asdf': 1234}