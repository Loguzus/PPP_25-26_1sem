from random import *
n = int(input("Количество строк: "))
m = int(input("Количество столбцов : "))
matrix = [[randint(-1000, 1001) for i in range(m)] for j in range(n)]
for row in matrix:
    print(*row)
maximpostrok = [max(row) for row in matrix]
maxpostolb = [max(matrix[i][j] for i in range(n)) for j in range(m)]
print("\nМаксимумы по строкам:", maximpostrok)
print("Максимумы по столбцам:", maxpostolb)
if n==m:
    diagsum = sum(matrix[i][i] for i in range(n))
    secdiagsum = sum(matrix[i][m - 1 - i] for i in range(m))
    print("\nСумма главной диагонали:", diagsum)
    print("Сумма побочной диагонали:", secdiagsum)
else:
    print("Для неквадратной матрицы суммы диагоналей просчитать нельзя!")
summastrok = [sum(row) for row in matrix]
maxsummastrok = max(summastrok)
maxstrok = summastrok.index(maxsummastrok)
print(f"Строка с наибольшей суммой ({maxsummastrok}) - это строка номер {maxstrok + 1}: ({matrix[maxstrok]})")
