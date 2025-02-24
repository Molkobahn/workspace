def main():
    def fizzbuzz(n):
        result = []

        mp = {3: "Fizz", 5: "Buzz", 7: "Jazz"}
        div = [3, 5, 7]

        for i in range(1, n + 1):
            res = ""

            for d in div:
                if i % d == 0:
                    res += mp[d]
                
            if not res:
                res += str(i)

            result.append(res)

        return result
    
    print(fizzbuzz(100))

main()