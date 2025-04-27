""" MA3.py

Student: Supraja Muralidharan
Mail: supraja.muralidharan.9814@student.uu.se
Reviewed by:
Date reviewed:

"""
import random as r
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc
import functools

def approximate_pi(n): # Ex1
    #n is the number of points
    # Write your code here
    nc=0
    inside_x=[]
    inside_y=[]
    outside_x=[]
    outside_y=[]
    for _ in range(n):
        a=r.uniform(-1,1)
        b=r.uniform(-1,1)
        if a**2 + b**2 <= 1:
            nc+=1
            inside_x.append(a)
            inside_y.append(b)
        else:
            outside_x.append(a)
            outside_y.append(b)
    plt.scatter(inside_x,inside_y,color='red')
    plt.scatter(outside_x,outside_y,color='blue')
    plt.show()
    return 4*(nc/n)

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 
    x=[[r.uniform(-1,1) for j in range(d)] for i in range(n)]
    nc = sum(map(lambda point: 1 if sum(x**2 for x in point) <= 1 else 0, x))
    v=(2**d)*(nc/n)
    return v

def hypersphere_exact(d): #Ex2, real value
    # d is the number of dimensions of the sphere 
    v=(m.pow((m.pi),(d/2)))/(m.gamma((d/2)+1))
    return v

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n,d,np=8):
    # n is the number of points
    # d is the number of dimensions of the sphere
    # np is the number of processes
    # sphere_volume for 10^5 is run for 10 iterations; each iteraction is processed in parallel
    with future.ProcessPoolExecutor() as ex:
        results = list(ex.map(sphere_volume, [n]*np, [d]*np))
    return mean(results)

#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n,d,np=10):
    #n is the number of points
    # d is the number of dimensions of the sphere
    #np is the number of processes
    #n is split into 10 chunks with 10^5 datapoints each and processed in parallel; average of which gives ~sphere_volume(10^6 datapoints)
    data_chunks = [(n // np, d)] * np
    if n % np != 0:
        data_chunks[-1] = (n // np + n % np, d)

    with future.ProcessPoolExecutor() as ex:
        results = list(ex.map(sphere_volume, [chunk[0] for chunk in data_chunks], [chunk[1] for chunk in data_chunks]))
    return mean(results)
    
def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)
    #Ex2
    n = 100000
    d = 2
    #sphere_volume(n,d)
    print("Ex:2")
    print(f"Exact volume of {d} dimensional sphere = {sphere_volume(n,d)}")
    print(f"Actual volume of {d} dimensional sphere = {hypersphere_exact(d)}")

    n = 100000
    d = 11
    #sphere_volume(n,d)
    print(f"Exact volume of {d} dimensional sphere = {sphere_volume(n,d)}")
    print(f"Actual volume of {d} dimensional sphere = {hypersphere_exact(d)}")

    #Ex3
    n = 100000
    d = 11
    res = []
    start = pc()
    for i in range (10):
        res.append(sphere_volume(n,d))
    stop = pc()
    print("\nEx:3")
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    print(f"Average volume = {mean(res)}")
    #print("What is parallel time?")
    start = pc()
    res = sphere_volume_parallel1(n,d)
    stop = pc()
    print(f"Ex3: Parallel time of {d} and {n}: {stop-start}")
    print(f"Average volume = {res}")

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    res = sphere_volume(n,d)
    stop = pc()
    print("\nEx:4")
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    print(f"Volume : {res}")
    #print("What is parallel time?")
    start = pc()
    res = sphere_volume_parallel2(n,d)
    stop = pc()
    print(f"Ex4: Parallel time of {d} and {n}: {stop-start}")
    print(f"Volume : {res}")
    

if __name__ == '__main__':
	main()