import math
a = 121
b = math.sqrt(a)

if b.is_integer():
  print(True)
else:
  print(False)


print(int((b + 1) ** 2))