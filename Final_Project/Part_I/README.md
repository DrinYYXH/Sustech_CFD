# Part I — 1D Linear Advection Equation with Discontinuous Initial Condition

**MAE5005 / MAE403 Computational Fluid Dynamics, Spring 2026**

---

## 1. Problem Statement

Solve the 1D linear advection equation:

$$\frac{\partial u}{\partial t} + a \frac{\partial u}{\partial x} = 0, \quad a = 1$$

on a periodic domain $x \in [-1, 1]$ with the discontinuous initial condition:

$$u(x, t=0) = \begin{cases} 1.0 & \text{if } -0.5 < x < 0.5 \\ 0.0 & \text{otherwise} \end{cases}$$

The analytical solution is $u(x, t) = u_0(x - at)$ with periodic extension. At $t = 2.0$ and $t = 8.0$, the wave has travelled exactly 1 and 4 full periods respectively, so the exact solution coincides with the initial square wave.

---

## 2. Numerical Method: Unified MUSCL Framework

All three schemes are implemented within the same cell-wise linear reconstruction framework (Eq. 3 in the project statement):

$$u_j^{n+1} = u_j^n - \nu\left(u_j^n - u_{j-1}^n\right) - \frac{\nu(1-\nu)}{2}\left(\delta_j - \delta_{j-1}\right)$$

where $\nu = a\Delta t / \Delta x$ is the CFL number, and $\delta_j = \sigma_j \Delta x$ is the limited slope in cell $j$. The three schemes differ only in how $\delta_j$ is defined.

### 2.1 Grid and Time Parameters

| Parameter | Value |
|-----------|-------|
| $N$ | 160 |
| $\Delta x$ | $2/N = 0.0125$ |
| CFL ($\nu$) | 0.8 |
| $\Delta t$ | $\nu \cdot \Delta x / a = 0.01$ |

### 2.2 Scheme Definitions

**Lax-Wendroff (downwind slope, no limiter):**
$$\delta_j^{\text{LW}} = u_{j+1} - u_j$$

**van Leer limiter (form 2):**
$$\delta_j^{\text{VL}} = \phi_{\text{VL}}(r_j) \cdot (u_{j+1} - u_j), \quad \phi_{\text{VL}}(r) = \frac{r + |r|}{1 + |r|}$$
$$r_j = \frac{u_j - u_{j-1}}{u_{j+1} - u_j}$$

**SUPERBEE limiter:**
$$\delta_j^{\text{SB}} = \phi_{\text{SB}}(r_j) \cdot (u_{j+1} - u_j), \quad \phi_{\text{SB}}(r) = \max\big(0, \min(2r, 1), \min(r, 2)\big)$$

---

## 3. Results

### 3.1 Solutions at $t = 2.0$ and $t = 8.0$ (Tasks 1–2)

| Scheme | $\min(u)$ at $t=8$ | $\max(u)$ at $t=8$ | TV at $t=0$ | TV at $t=2$ | TV at $t=8$ |
|--------|-------------------|--------------------|-------------|-------------|-------------|
| Lax-Wendroff | −0.214 | 1.214 | 2.00 | 3.14 | 3.56 |
| van Leer | 0.000 | 1.000 | 2.00 | 2.00 | 2.00 |
| SUPERBEE | 0.000 | 1.000 | 2.00 | 2.00 | 2.00 |

**Analysis:**

- **Lax-Wendroff** produces dispersive oscillations (Gibbs phenomenon) near discontinuities — the solution overshoots to 1.214 and undershoots to −0.214. The total variation grows monotonically from 2.00 to 3.56, confirming LW is **not TVD**. This is a direct consequence of the scheme's dispersion error: third-order spatial derivatives in the leading truncation error term cause phase errors that manifest as $2\Delta x$ oscillations near sharp gradients.

- **van Leer** is **TVD** — the solution stays within $[0, 1]$, and TV remains exactly 2.00 at all times. The limiter provides a good compromise between sharpness and monotonicity. The discontinuity is spread over ~7 cells at $t=8.0$.

- **SUPERBEE** is also **TVD** and gives the sharpest discontinuity capture (~5 cells). However, it can over-sharpen smooth extrema (the "staircasing" effect), which is the price paid for the most compressive limiter in the TVD class.

### 3.2 Order of Accuracy (Task 3)

Convergence was studied using a **smooth initial condition** $u(x,0) = \sin(\pi x)$ to avoid the singularity that would otherwise limit the convergence rate. Grids of $N = 20, 40, 80, 160, 320$ were used at CFL = 0.8, run to $t = 1.0$.

| Scheme | $L_1$ slope | $L_\infty$ slope |
|--------|------------|------------------|
| Lax-Wendroff | **1.99** | **1.98** |
| van Leer | **2.02** | 1.39 |
| SUPERBEE | **1.88** | 1.10 |

**Analysis:**

- **LW** achieves the theoretical $\mathcal{O}(\Delta x^2)$ in both norms — the scheme is truly second-order on smooth solutions.
- **VL and SB** achieve second-order in the $L_1$ norm, but the $L_\infty$ convergence degrades to ~1.1–1.4. This is expected: TVD limiters must locally reduce to first order at smooth extrema (Harten's theorem) to maintain the TVD property. The $L_\infty$ norm is sensitive to these isolated clipping points, while the global $L_1$ norm still benefits from second-order accuracy in smooth regions.

> **Design note:** A smooth initial condition was essential for this study. With the discontinuous square wave, all schemes would converge at sub-first-order rates ($\sim\mathcal{O}(\Delta x^{0.5})$) because the solution itself lacks sufficient regularity.

### 3.3 Numerical Stability (Task 4)

**Theoretical conditions:**

- **LW:** von Neumann analysis gives the amplification factor $|G|^2 = 1 - 4\nu^2(1-\nu^2)\sin^4(k\Delta x/2)$. The condition $|G| \leq 1$ requires $\nu \leq 1$.
- **VL and SB:** As TVD schemes, Harten's theorem guarantees $\text{TV}(u^{n+1}) \leq \text{TV}(u^n)$ for $\nu \leq 1$, ensuring monotonicity and $L_\infty$ stability.

**Numerical verification** (smooth IC, $N=80$, $t_{\text{end}}=10$):

| CFL | LW | van Leer | SUPERBEE |
|-----|-----|----------|----------|
| 0.50 | ✓ stable | ✓ stable | ✓ stable |
| 0.80 | ✓ stable | ✓ stable | ✓ stable |
| 1.00 | ✓ stable | ✓ stable | ✓ stable |
| 1.05 | ✗ blowup at $t \approx 8.6$ | ✗ blowup at $t \approx 8.6$ | ✗ blowup at $t \approx 8.5$ |
| 1.10 | ✗ blowup at $t \approx 4.8$ | ✗ blowup at $t \approx 4.7$ | ✗ blowup at $t \approx 4.6$ |

All three schemes become **numerically unstable for $\nu > 1$**, confirming the CFL stability bound. The instability manifests as exponential growth with the growth rate increasing with $\nu$.

### 3.4 Open-Ended Improvement: Adaptive Lax-Wendroff (Task 5)

**Idea:** Use a local smoothness sensor to adaptively blend between the second-order Lax-Wendroff slope (smooth regions) and the first-order upwind slope (near discontinuities).

**Implementation — Shock Sensor:**

$$\theta_j = \frac{|u_{j+1} - 2u_j + u_{j-1}|}{|u_{j+1} - u_j| + |u_j - u_{j-1}| + \varepsilon}$$

$$\delta_j^{\text{ALW}} = (1 - \theta_j) \cdot (u_{j+1} - u_j)$$

- $\theta_j \approx 1$ near discontinuities (large second derivative relative to first) → $\delta_j \approx 0$ (upwind, monotone)
- $\theta_j \approx 0$ in smooth regions (vanishing second derivative) → $\delta_j \approx u_{j+1}-u_j$ (full LW, second-order)

**Results:**

| Scheme | $\min(u)$, $t=8$ | $\max(u)$, $t=8$ | TV at $t=8$ | Monotone? |
|--------|-------------------|-------------------|-------------|-----------|
| LW (original) | −0.214 | 1.214 | 3.56 | ✗ |
| van Leer | 0.000 | 1.000 | 2.00 | ✓ |
| SUPERBEE | 0.000 | 1.000 | 2.00 | ✓ |
| **ALW (improved)** | **0.000** | **1.000** | **2.00** | **✓** |

The adaptive LW scheme **completely eliminates** the oscillations that plague the original LW scheme, achieving exact TVD behavior (TV = 2.00 at all times). In smooth regions the second-order LW slope is retained, while near discontinuities the sensor automatically detects the sharp gradient and applies numerical dissipation by reducing the slope toward zero.

---

## 4. Code Structure

```
Part_I/
├── linear_advection.f90      Tasks 1–2: Three schemes + TV + solution output
├── schemes.inc               Shared subroutines (advance, slopes, TV, errors)
├── convergence_study.f90     Task 3: Grid refinement for order of accuracy
├── stability_study.f90       Task 4: CFL sweep for numerical stability
├── adaptive_lw.f90           Task 5: Adaptive Lax-Wendroff implementation
├── plot_results.py           Tasks 1–2 plotting
├── plot_convergence.py       Task 3 plotting
├── plot_stability.py         Task 4 plotting
└── plot_adaptive.py          Task 5 plotting
```

All programs compile with `gfortran`:
```bash
gfortran -O2 linear_advection.f90  -o linear_advection.exe
gfortran -O2 convergence_study.f90 -o convergence_study.exe
gfortran -O2 stability_study.f90   -o stability_study.exe
gfortran -O2 adaptive_lw.f90       -o adaptive_lw.exe
```

---

## 5. Key Conclusions

1. **Lax-Wendroff** provides second-order accuracy on smooth solutions but produces non-physical oscillations near discontinuities due to dispersion error. The TV grows unboundedly.

2. **van Leer** and **SUPERBEE** limiters achieve TVD behavior, eliminating oscillations at the cost of locally reduced accuracy at extrema (from second to first order). SUPERBEE gives the sharpest discontinuities, while van Leer offers a balanced compromise.

3. All three schemes share the same linear stability bound $\nu \leq 1$, confirmed both analytically (von Neumann / TVD theory) and numerically.

4. The **Adaptive Lax-Wendroff** scheme, using a simple shock sensor to blend between LW and upwind slopes, successfully removes LW oscillations while preserving second-order behavior in smooth regions. It achieves strict TVD behavior (TV = 2.0 invariant) without requiring a nonlinear limiter function.
