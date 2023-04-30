from manim import *
def get_random_points(n_points=11,width=6,height=6):
    return np.array([
        [
            -width/2+np.random.random()*width,
            -height/2+np.random.random()*height,
            0
        ]
        for _ in range(n_points)
    ])
numeros=get_random_points()
print(numeros)
# lista1=[1,2,3]
# lista2=list([1,2,3])
# print(lista2)