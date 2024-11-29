import math

def main():
    m = int(input("Introduzca el modulo m: "))
    pe = 0

    if m % 10 == 0:
        z = 10
        e = 0
        for i in range(4):
            if m == z:
                e = i + 1
                break
            else:
                z *= 10
        
        if e == 0:
            e = 5
            while pe == 0:
                if m == z:
                    pe = 5 * (pow(10, e - 2))
                else:
                    z *= 10
                    e += 1
        else:
            pe = (pow(5, e - 1)) * 4
    else:
        pe = m // 4

    print(f"El periodo esperado es {pe}")

if __name__ == "__main__":
    main()
