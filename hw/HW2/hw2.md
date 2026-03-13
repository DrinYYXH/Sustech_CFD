# CFD_HW_1

**姓名：梁祝旸**  
**学号：12532299**  
**课程：计算流体力学**  
**日期：2026-03-09**

---


## Question 1: Code-Explaination

#### (a) Using the lecture notes as a guide, explain what flow problem this code is trying to solve;

The code simulates the transient development of a 1-D viscous channel flow driven by a constant pressure gradient.
The governing equation is :
$$
\frac{\partial u}{\partial t}=\nu \frac{\partial^2 u}{\partial y^2}+g
$$

With a constant body force **g** :
$$
g = \frac{2\nu u_0}{a_L^2}
$$

And B.C.s :
$$
\begin{cases}
    u(-a_L,t) = 0 \\
    u(a_L,t) = 0
\end{cases}
$$

#### (b)   Provide a sketch of the flow domain and the locations of the grid points;

The plot is kind of like :
<img src="hw_2_1_b.jpg" width="500"  alt="二维管道流图解">

As a 1-D flow, the grid points are just saperated along **y**-axis. And the number of points is **N + 1**.
The sketch of flow shape is just a **sketch**, the **u** at walls have to be **0**.

#### (c)    Describe, in your own words, all the input parameters for this code and their meaning;

```
integer,parameter      :: N=8, Ntime=64
real*8,parameter       ::  dt = 0.032d0

real*8,parameter       :: u0=1.0d0, aL=1.0d0, anu=0.1
! u0 maximum velocity,aL channel half width,anu kinematic viscosity
! body force is then  g = 2*nu*u0/al^2
!real*8, dimension(1:N+1) :: uold, u, uana  [uana is not used, can be removed.]
real*8, dimension(1:N+1) :: uold, u
real*8                   ::theta0, theta1, theory1,ss,ycc,CFL
integer                  :: j,it,nsteps,k
real*8                   :: dy,pi,t,Tend
```
**N** means the number of grids. (number of grid ponits is **N + 1**)

**Ntime** is used for control the frequency for print out the theory solution for comparison every **Ntime** steps. But, the code in BB has a problem :
```
      if(mod(it,NTime).eq.0) then
```
This NTime has a wrong "T", as the input is "N**t**ime".

**dt** is the time step for the 

















EOF