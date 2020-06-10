from mpi4py import MPI
import numpy as np
import math
import time
import sys
comm = MPI.COMM_WORLD   # Defines the default communicator
num_procs = comm.Get_size()  # Stores the number of processes in num_procs.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process

def vPrime(num):
    esprimo = True
    if(num < 2):
        return False
    i = 2
    while(i <= math.sqrt(num) and esprimo):
        if num % i == 0:
            esprimo = False
        i = i+1
    return esprimo

# def sumaconsecutivos(n1,n2):
#     sum = (n2*(n2+1)/2)-(n1*(n1+1)/2)
#     return sum

def costototal(n1,n2):
    rn1 = math.floor(math.sqrt(n1))
    rn2 = math.floor(math.sqrt(n2))
    c1=rn1*(math.pow(rn1+1,2)-n1)
    c2=rn2*(n2-math.pow(rn2,2)+1)
    c3=0
    for i in range(int(rn1+1),int(rn2)):
        c3=c3+i*(math.pow(i+1,2)-math.pow(i,2))
    costo=c1+c2+c3
    return costo

def limsuperior(costo,n):
    rn = math.floor(math.sqrt(n))
    c1=rn*(math.pow(rn+1,2)-n)
    c2=0
    if c1>=costo:
        lim=costo/rn+n
        return lim
    else:
        i=rn
        while(c1+c2<costo):
            i=i+1
            ci=i*(math.pow(i+1,2)-math.pow(i,2))
            c2=c2+ci            
        c3=costo-c2+ci-c1
        lim=c3/i+math.pow(i,2)-1
        return lim

def dividetrabajo(n1,n2,costo,nblq):
    ci = costo/nblq
    m = np.zeros((2,nblq))
    lim=n1
    for i in range(nblq):
        m[0,i]=int(lim)
        m[1,i]=int(limsuperior(ci,lim))
        if i==nblq-1:
            m[1,i]=n2
        lim=m[1,i]+1
    return m


if rank==0:
    print("Buscando primos de 12 digitos: ")
    start_time = time.time()
    n1=100000000000
    n2=999999999999
    costot = costototal(n1,n2)
    m = dividetrabajo(n1,n2,costot,num_procs-1)
    # for i in range(num_procs-1):
    #     print("M[0]"+"["+str(i)+"]="+str(m[0][i]))
    #     print("M[1]"+"["+str(i)+"]="+str(m[1][i]))
    for i in range(num_procs-1):
        v=m[:,i]
        comm.send(v,dest=i+1,tag=i+1)
    cont=0
    ve = np.zeros((num_procs-1))
    for i in range(1,num_procs):
        ne=comm.recv(source=i)
        ve[i-1]=ne
        cont = cont+ne
    for i in range(1,num_procs):
        nv=m[1][i-1]-m[0][i-1]+1
        ne = ve[i-1]
        print("El proceso "+str(i)+" verificó "+str(nv)+" números y encontró "+str(ne)+" primos")
    elapsed_time = time.time() - start_time
    print("Tiempo total de ejecución por parte del root: %.10f seconds." % elapsed_time)
    print("Primos totales encontrados por el root: "+str(cont))
else:
    v = comm.recv(source=0,tag=rank)
    desde = int(v[0])
    hasta = int(v[1])
    cont=0
    contv=0
    for i in range(desde,hasta+1):
        contv+=1
        if contv==10:
            print(".", end="", flush=True)
            contv=0
        if vPrime(i)==True:
            cont=cont+1
    comm.send(cont,dest=0)
