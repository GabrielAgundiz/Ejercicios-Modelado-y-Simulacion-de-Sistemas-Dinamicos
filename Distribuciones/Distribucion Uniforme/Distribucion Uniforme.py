def main():
    a = float(input("Ingrese el valor de a: "))
    b = float(input("Ingrese el valor de b: "))
    n = int(input("Ingrese la cantidad de números rectangulares: "))
    
    numero = []
    
    for i in range(n):
        num = float(input(f"Ingrese el número {i + 1}: "))
        numero.append(num)
    
    suma = 0
    x = []
    
    for i in range(n):
        x_i = a + (b - a) * numero[i]
        x.append(x_i)
        print(f"x{i} = {x_i}")
        suma += x_i
    
    print(f"x total: {suma}")
    print(f"x promedio: {suma / n}")

if __name__ == "__main__":
    main()
