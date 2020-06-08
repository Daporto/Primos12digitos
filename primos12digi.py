from mpi4py import MPI
import numpy as np
comm = MPI.COMM_WORLD   # Defines the default communicator
num_procs = comm.Get_size()  # Stores the number of processes in num_procs.
rank = comm.Get_rank()  # Stores the rank (pid) of the current process
import math
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

def sumaconsecutivos(n1,n2):
    sum = (n2*(n2+1)/2)-(n1*(n1+1)/2)
    return sum

def costototal(n1,n2):
    rn1 = math.floor(math.sqrt(n1))
    rn2 = math.floor(math.sqrt(n2))
    c1=rn1*(math.pow(rn1+1,2)-n1)
    c2=rn2*(n2-math.pow(rn2,2)+1)
    c3=0
    for i in range(rn1+1,rn2):
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
        m[0,i]=lim
        m[1,i]=limsuperior(ci,lim)
        if i==nblq-1:
            m[1,i]=n2
        lim=m[1,i]+1
    return m

def main():
    if rank==0:
        n1=100000000000
        n2=999999999999
        costot = costototal(n1,n2)
        m = dividetrabajo(n1,n2,costot,num_procs-1)
        for i in range(num_procs-1):
            v=m[:,i]
            comm.send(v,dest=i+1,tag=i+1)
        cont=0
        for i in range(1,num_procs):
            cont = cont+comm.recv(source=i)
        print("Primos totales encontrados: "+str(cont))
    else:
        v = comm.recv(source=0,tag=rank)
        desde = math.floor(v[0])
        #print("desde:"+str(desde))
        hasta = math.floor(v[1])
        #print("hasta:"+str(hasta))
        cont=0
        for i in range(desde,hasta+1):
            if vPrime(i)==True:
                print(str(i)+" es primo")
                cont=cont+1
        comm.send(cont,dest=0)
main()