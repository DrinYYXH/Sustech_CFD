# CFD_HW_5
  
**姓名：梁祝旸**  
**学号：12532299**  
**课程：计算流体力学**  
**日期：2026-04-7**
  
  
  
## Question 14: Exact Solution of Finite-Difference Scheme

#### （a）

The original Lagrangian interpolation scheme is given by:
$$u_{j}^{n+1}=-\frac{(\Delta x-a\Delta t)a\Delta t}{2(\Delta x)^{2}}u_{j-2}^{n}+\frac{(2\Delta x-a\Delta t)a\Delta t}{(\Delta x)^{2}}u_{j-1}^{n}+\frac{(\Delta x-a\Delta t)(2\Delta x-a\Delta t)}{2(\Delta x)^{2}}u_{j}^{n} \tag{1}$$

Let the CFL to be $C \equiv \frac{a\Delta t}{\Delta x}$:
$$u_j^{n+1} = -\frac{C(1-C)}{2} u_{j-2}^n + C(2-C) u_{j-1}^n + \frac{(1-C)(2-C)}{2} u_j^n \tag{2}$$

Rearranging in the order of $C$:
$$u_j^{n+1} - u_j^n = -\frac{C}{2} [3u_j^n - 4u_{j-1}^n + u_{j-2}^n] + \frac{C^2}{2} [u_{j-2}^n - 2u_{j-1}^n + u_j^n] \tag{3}$$

Divide both sides by $\Delta t$ and substitute $C = \frac{a\Delta t}{\Delta x}$ back into the equation:
$$\frac{u_j^{n+1} - u_j^n}{\Delta t} = -\frac{a}{2\Delta x} [3u_j^n - 4u_{j-1}^n + u_{j-2}^n] + \frac{a^2 \Delta t}{2(\Delta x)^2} [u_{j-2}^n - 2u_{j-1}^n + u_j^n] \tag{4}$$

Rearranging the spatial derivative term to the left side yields the target equation:
$$\frac{u_j^{n+1} - u_j^n}{\Delta t} + \frac{a}{2\Delta x} [3u_j^n - 4u_{j-1}^n + u_{j-2}^n] = \frac{a^2 \Delta t}{2} \frac{[u_{j-2}^n - 2u_{j-1}^n + u_j^n]}{(\Delta x)^2} \tag{5}$$


#### （b）

To perform the von Neumann stability analysis, we assume a discrete Fourier mode for the numerical solution:
$$u_j^n = G^n e^{i j \theta} \tag{6}$$

where $G$ is the amplification factor, $\theta = k\Delta x$ is the phase angle, and $i = \sqrt{-1}$.

Substituting this into $(2)$:
$$G = \frac{C(C-1)}{2} e^{-i 2\theta} + C(2-C) e^{-i \theta} + \frac{(C-1)(C-2)}{2} \tag{7}$$

Using Euler's formula $e^{-i\theta} = \cos\theta - i\sin\theta$, we can separate $G$ into its real part ($G_R$) and imaginary part ($G_I$):

$$
G_R = \frac{C(C-1)}{2} \cos(2\theta) + C(2-C) \cos\theta + \frac{(C-1)(C-2)}{2}
 \tag{8.1}
$$

$$
G_I = -\frac{C(C-1)}{2} \sin(2\theta) - C(2-C) \sin\theta
 \tag{8.2}
$$

The magnitude of the amplification factor is $|G| = \sqrt{G_R^2 + G_I^2}$.

<img src="hw5_1.png" width="600"  alt="未找到文件">
  

#### （c）

The 1D advection equation has an exact solution. It means the wave simply moves at a constant speed $a$:

$$
\frac{\partial u}{\partial t} + a \frac{\partial u}{\partial x} = 0 \tag{9}
$$

$$
u(x, t+\Delta t) = u(x - a\Delta t, t) \tag{10}
$$

On our grid, this means:
$$
u_j^{n+1} = u(x_j - a\Delta t, t^n) \tag{11}
$$

The error in our scheme comes from the interpolation step. If the point $x_j - a\Delta t$ lands exactly on a grid point that we already use (like point $j-1$ or $j-2$), we don't need to do any interpolation. In this case, the scheme has zero truncation error.

There are two special cases for $C = \frac{a\Delta t}{\Delta x}$:

**1. The point lands exactly on $j-1$:**
$$
a\Delta t = \Delta x \implies C = 1 \tag{12}
$$

If we plug $C=1$ into our scheme, we get:
$$
u_j^{n+1} = 0 \cdot u_{j-2}^n + 1 \cdot u_{j-1}^n + 0 \cdot u_j^n = u_{j-1}^n \tag{13}
$$
This matches the exact solution.

**2. The point lands exactly on $j-2$:**
$$
a\Delta t = 2\Delta x \implies C = 2 \tag{14}
$$

If we plug $C=2$ into our scheme, we get:
$$
u_j^{n+1} = 1 \cdot u_{j-2}^n + 0 \cdot u_{j-1}^n + 0 \cdot u_j^n = u_{j-2}^n \tag{15}
$$

This also matches the exact solution perfectly.

So, the two special values of $C$ is **1** and **2**.



## Question 15: Derivation of the Modified Equation

From Problem 14, our scheme looks like this:
$$
\begin{aligned}
\frac{u_j^{n+1} - u_j^n}{\Delta t} &+ \frac{a}{2\Delta x} [3u_j^n - 4u_{j-1}^n + u_{j-2}^n] 
= \frac{a^2 \Delta t}{2(\Delta x)^2} [u_{j-2}^n - 2u_{j-1}^n + u_j^n]
\end{aligned} \tag{1}
$$

First, let's do Taylor expansions around the point $(x_j, t^n)$. To make it easier to write, I'll use subscripts for derivatives (like $u_x$ instead of $\frac{\partial u}{\partial x}$):
$$u_j^{n+1} = u + u_t \Delta t + \frac{1}{2} u_{tt} \Delta t^2 + \frac{1}{6} u_{ttt} \Delta t^3 + \frac{1}{24} u_{tttt} \Delta t^4 + \dots \tag{2}$$

$$u_{j-1}^n = u - u_x \Delta x + \frac{1}{2} u_{xx} \Delta x^2 - \frac{1}{6} u_{xxx} \Delta x^3 + \frac{1}{24} u_{xxxx} \Delta x^4 - \dots \tag{3}$$

$$u_{j-2}^n = u - 2u_x \Delta x + 2u_{xx} \Delta x^2 - \frac{4}{3} u_{xxx} \Delta x^3 + \frac{2}{3} u_{xxxx} \Delta x^4 - \dots \tag{4}$$

Plugging these back into the three parts of our scheme:

**1. Time derivative part:**
$$\frac{u_j^{n+1} - u_j^n}{\Delta t} = u_t + \frac{1}{2} u_{tt} \Delta t + \frac{1}{6} u_{ttt} \Delta t^2 + \frac{1}{24} u_{tttt} \Delta t^3 + \dots \tag{5}$$

**2. Spatial convection part:**
$$\frac{a}{2\Delta x} [3u_j^n - 4u_{j-1}^n + u_{j-2}^n] = a u_x - \frac{a}{3} u_{xxx} \Delta x^2 + \frac{a}{4} u_{xxxx} \Delta x^3 + \dots \tag{6}$$

**3. Artificial diffusion part (right side):**
$$\frac{a^2 \Delta t}{2(\Delta x)^2} [u_{j-2}^n - 2u_{j-1}^n + u_j^n] = \frac{a^2 \Delta t}{2} u_{xx} - \frac{a^2 \Delta t \Delta x}{2} u_{xxx} + \frac{7 a^2 \Delta t (\Delta x)^2}{24} u_{xxxx} + \dots \tag{7}$$

Putting it all together and moving the truncation error terms to the right side:
$$
\begin{aligned}
u_t + a u_x = &\frac{\Delta t}{2} (a^2 u_{xx} - u_{tt}) + \left[ \frac{a\Delta x^2}{3} - \frac{a^2 \Delta t \Delta x}{2} \right] u_{xxx} - \frac{\Delta t^2}{6} u_{ttt} \\
&+ \left[ \frac{7 a^2 \Delta t \Delta x^2}{24} - \frac{a\Delta x^3}{4} \right] u_{xxxx} - \frac{\Delta t^3}{24} u_{tttt}
\end{aligned} \tag{8}
$$

Now, we need to replace the time derivatives ($u_{tt}, u_{ttt}$, etc.) with spatial derivatives. 
Using the simple first-order relation $u_t \approx -a u_x$, we can easily get:
$$u_{ttt} \approx -a^3 u_{xxx} \tag{9}$$

$$u_{tttt} \approx a^4 u_{xxxx} \tag{10}$$

To replace the $(a^2 u_{xx} - u_{tt})$ term without losing our 3rd-order accuracy, we need to include the leading error. Let $u_t = -a u_x + \mu u_{xxx}$. Taking the time derivative gives us:
$$u_{tt} = -a u_{xt} + \mu u_{xxxt} = -a(-a u_{xx} + \mu u_{xxxx}) - a \mu u_{xxxx} = a^2 u_{xx} - 2a \mu u_{xxxx} \tag{11}$$
So, the difference is just:
$$\frac{\Delta t}{2} (a^2 u_{xx} - u_{tt}) = a \mu \Delta t u_{xxxx} \tag{12}$$

Let $C = \frac{a\Delta t}{\Delta x}$. We first collect all the $u_{xxx}$ terms (which are $\mathcal{O}(\Delta^2)$) to find $\mu$ and our coefficient $A$:
$$A \cdot a \Delta x^2 \cdot u_{xxx} = \mu \cdot u_{xxx} = \left( \frac{a\Delta x^2}{3} - \frac{a^2 \Delta t \Delta x}{2} + \frac{a^3 \Delta t^2}{6} \right) u_{xxx} \tag{13}$$
Factoring out $a \Delta x^2$:
$$A = \frac{1}{3} - \frac{1}{2} C + \frac{1}{6} C^2 \tag{14}$$
**$$A = \frac{(C-1)(C-2)}{6} \tag{15}$$**

Next, we collect all the $u_{xxxx}$ terms (which are $\mathcal{O}(\Delta^3)$) to find $B$:
$$B \cdot a \Delta x^3 = a \mu \Delta t + \frac{7 a^2 \Delta t \Delta x^2}{24} - \frac{a \Delta x^3}{4} - \frac{a^4 \Delta t^3}{24} \tag{16}$$
Divide everything by $a \Delta x^3$ and plug in $C$:
$$B = \frac{\mu \Delta t}{\Delta x^3} + \frac{7}{24} C - \frac{1}{4} - \frac{1}{24} C^3 \tag{17}$$
Since we already know $\frac{\mu \Delta t}{\Delta x^3} = C \cdot A = \frac{C(C-1)(C-2)}{6}$, we can substitute that in:
$$
\begin{aligned}
B &= \frac{C(C^2 - 3C + 2)}{6} + \frac{7C - 6 - C^3}{24} \\
&= \frac{4C^3 - 12C^2 + 8C + 7C - 6 - C^3}{24}
\end{aligned} \tag{18}
$$
$$B = \frac{3C^3 - 12C^2 + 15C - 6}{24} = \frac{C^3 - 4C^2 + 5C - 2}{8} \tag{19}$$
Factoring the top part gives us our final expression for $B$:
**$$B = \frac{(C-1)^2(C-2)}{8} \tag{20}$$**

Because there are no first-order error terms (like $\mathcal{O}(\Delta x)$ or $\mathcal{O}(\Delta t)$ in the modified equation), this proves the scheme is second-order accurate in both space and time.




## Question 16: Derivation of the Modified Equation


We consider the Lax scheme for the 1D advection equation:

$$
\frac{u_j^{n+1} - \frac{u_{j+1}^n + u_{j-1}^n}{2}}{\Delta t} + \frac{u_{j+1}^n - u_{j-1}^n}{2\Delta x} = 0
$$

Define the CFL number:

$$
C = \frac{a\Delta t}{\Delta x}
$$

#### (a) Von Neumann Stability Analysis

Assume a Fourier mode:

$$
u_j^n = G^n e^{ikj\Delta x}
$$

Substitute into the scheme:

$$
G = \frac{1}{2}\left(e^{ik\Delta x} + e^{-ik\Delta x}\right) + \frac{a\Delta t}{2\Delta x}\left(e^{ik\Delta x} - e^{-ik\Delta x}\right)
  $$

Using Euler identities:

$$
G = \cos(k\Delta x) - i C \sin(k\Delta x)
$$

Compute the amplification factor:

$$
|G|^2 = \cos^2(k\Delta x) + C^2 \sin^2(k\Delta x)
$$

For stability, require:

$$
|G| \le 1 \quad \forall k
$$

Thus:

$$
C^2 \le 1
$$

$$
\boxed{|C| \le 1}
$$


#### (b) Taylor Expansion and Order of Accuracy

Time term:

$$
\frac{u_j^{n+1} - u_j^n}{\Delta t}
= u_t + \frac{\Delta t}{2}u_{tt} + O(\Delta t^2)
$$

Averaging term:

$$
\frac{u_{j+1} + u_{j-1}}{2}
= u + \frac{\Delta x^2}{2}u_{xx} + O(\Delta x^4)
$$

Central difference:

$$
\frac{u_{j+1} - u_{j-1}}{2\Delta x}
= u_x + \frac{\Delta x^2}{6}u_{xxx} + O(\Delta x^4)
$$

Substitute into the scheme:

$$
u_t + \frac{\Delta t}{2}u_{tt} +  a\left(u_x + \frac{\Delta x^2}{6}u_{xxx}\right)
  = \frac{\Delta x^2}{2\Delta t}u_{xx}
$$

Rearrange:

$$
u_t + a u_x = \frac{\Delta x^2}{2\Delta t}u_{xx}+ \frac{\Delta t}{2}u_{tt} + \frac{a\Delta x^2}{6}u_{xxx}
  $$

Using the PDE:

$$
u_t = -a u_x
$$

we obtain:

$$
u_{tt} = a^2 u_{xx}
$$

Thus:

$$
u_t + a u_x=\left(\frac{\Delta x^2}{2\Delta t} - \frac{a^2 \Delta t}{2}\right) u_{xx}+ \frac{a\Delta x^2}{6}u_{xxx}
  $$

---

**Order of Accuracy**:

* Time: first-order
* Space: second-order


#### (c) Modified Equation (First-order Error Only)

Retain only the leading error term:

$$
u_t + a u_x = \alpha \Delta x , u_{xx}
$$

From part (b):

$$
\alpha \Delta x = \frac{\Delta x^2}{2\Delta t} - \frac{a^2 \Delta t}{2}
$$

Divide by $\Delta x$:

$$
\alpha = \frac{\Delta x}{2\Delta t} - \frac{a^2 \Delta t}{2\Delta x}
$$

Using the CFL number:

$$
C = \frac{a\Delta t}{\Delta x}
$$

we obtain:

$$
\alpha = \frac{a}{2}\left(\frac{1}{C} - C\right)
$$

---

Stability Condition from Modified Equation

For numerical stability, require:

$$
\alpha \ge 0
$$

$$
\frac{1}{C} - C \ge 0
\Rightarrow C^2 \le 1
$$

$$
\boxed{|C| \le 1}
$$


