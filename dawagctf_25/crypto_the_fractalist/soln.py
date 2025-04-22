import matplotlib.pyplot as plt
import numba as np
nos = [
    -1.25-0.04j,
    -0.42+0.60j,
    -0.25-0.64j,
    -1.21-0.17j,
    0.08-0.63j,
    0.36-0.32j,
    0.33+0.52j,
    -0.17+0.65j,
    -0.24+0.75j,
    -0.70-0.27j,
    -0.57+0.57j,
    -0.55-0.65j,
    -0.57-0.50j,
    -0.71+0.29j,
    -0.37-0.64j,
    -0.75+0.03j,
    -1.26-0.09j,
    -1.01+0.28j,
    -1.34-0.06j,
    -0.57+0.50j,
    -0.75+0.04j,
    -0.48-0.63j,
    -1.06-0.26j,
    -0.78+0.13j,
    -0.22-0.74j,
    -0.78+0.15j,
    -0.48-0.62j,
    -0.19+0.67j,
    -0.42-0.60j,
    0.29+0.47j,
    -0.83-0.19j,
    -0.79+0.15j
]
def mandelbrot(c, max_iter=1000):
    z = 0
    for i in range(max_iter):
        z = z*z + c
        if abs(z) > 2:
            return i
    return -1  # flag as inside set

decoded = ""
for pt in nos:
    count = mandelbrot(pt)
    if 32 <= count <= 126:
        decoded += chr(count)
    else:
        decoded += '.'  # or skip
print(decoded)


# Example:
# for pt in points:
#     print(f"{pt}: {mandelbrot(pt)} iterations")


# plt.figure(figsize=(8, 6))
# plt.scatter(x, y, color='blue', marker='o')
# plt.title('Plot of Complex Numbers')
# plt.xlabel('Real Part')
# plt.ylabel('Imaginary Part')
# plt.grid(True)
# plt.axhline(0, color='black', linewidth=0.5)
# plt.axvline(0, color='black', linewidth=0.5)
# plt.show()
