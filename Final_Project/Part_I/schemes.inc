!==============================================================================
! Shared subroutines for Part I (included via 'include' inside contains block)
!==============================================================================

  !===========================================================================
  ! Advance one time step using the unified MUSCL scheme:
  !   u_j^{n+1} = u_j^n - nu*(u_j - u_{j-1}) - 0.5*nu*(1-nu)*(delta_j - delta_{j-1})
  !===========================================================================
  subroutine advance(N, nu, u, delta, u_new)
    integer, intent(in) :: N
    real(8), intent(in) :: nu
    real(8), intent(in) :: u(N), delta(N)
    real(8), intent(out) :: u_new(N)
    integer :: i, im1
    real(8) :: coeff

    coeff = 0.5d0 * nu * (1.0d0 - nu)

    do i = 1, N
      im1 = i - 1
      if (im1 < 1) im1 = N

      u_new(i) = u(i) - nu * (u(i) - u(im1)) &
                      - coeff * (delta(i) - delta(im1))
    end do
  end subroutine advance

  !===========================================================================
  ! Lax-Wendroff slope: delta_j = u_{j+1} - u_j  (downwind, no limiter)
  !===========================================================================
  subroutine compute_delta_lw(N, u, delta)
    integer, intent(in) :: N
    real(8), intent(in) :: u(N)
    real(8), intent(out) :: delta(N)
    integer :: i, ip1

    do i = 1, N
      ip1 = i + 1
      if (ip1 > N) ip1 = 1
      delta(i) = u(ip1) - u(i)
    end do
  end subroutine compute_delta_lw

  !===========================================================================
  ! van Leer limiter slope
  !   phi_VL(r) = (r + |r|) / (1 + |r|)
  !   r_j = (u_j - u_{j-1}) / (u_{j+1} - u_j)
  !===========================================================================
  subroutine compute_delta_vl(N, u, delta)
    integer, intent(in) :: N
    real(8), intent(in) :: u(N)
    real(8), intent(out) :: delta(N)
    integer :: i, im1, ip1
    real(8) :: du_back, du_forw, r, phi, eps

    eps = 1.0d-15

    do i = 1, N
      im1 = i - 1
      if (im1 < 1) im1 = N
      ip1 = i + 1
      if (ip1 > N) ip1 = 1

      du_back = u(i) - u(im1)
      du_forw = u(ip1) - u(i)

      if (abs(du_forw) < eps) then
        delta(i) = 0.0d0
      else
        r = du_back / du_forw
        phi = (r + abs(r)) / (1.0d0 + abs(r))
        delta(i) = phi * du_forw
      end if
    end do
  end subroutine compute_delta_vl

  !===========================================================================
  ! SUPERBEE limiter slope
  !   phi_SB(r) = max(0, min(2r, 1), min(r, 2))
  !===========================================================================
  subroutine compute_delta_sb(N, u, delta)
    integer, intent(in) :: N
    real(8), intent(in) :: u(N)
    real(8), intent(out) :: delta(N)
    integer :: i, im1, ip1
    real(8) :: du_back, du_forw, r, phi, eps

    eps = 1.0d-15

    do i = 1, N
      im1 = i - 1
      if (im1 < 1) im1 = N
      ip1 = i + 1
      if (ip1 > N) ip1 = 1

      du_back = u(i) - u(im1)
      du_forw = u(ip1) - u(i)

      if (abs(du_forw) < eps) then
        delta(i) = 0.0d0
      else
        r = du_back / du_forw
        phi = max(0.0d0, min(2.0d0 * r, 1.0d0), min(r, 2.0d0))
        delta(i) = phi * du_forw
      end if
    end do
  end subroutine compute_delta_sb

  !===========================================================================
  ! Adaptive Lax-Wendroff with shock sensor
  !   theta_j = |u_{j+1} - 2u_j + u_{j-1}| / (|u_{j+1} - u_j| + |u_j - u_{j-1}| + eps)
  !   delta_j = (1.0 - theta_j) * (u_{j+1} - u_j)
  !===========================================================================
  subroutine compute_delta_alw(N, u, delta)
    integer, intent(in) :: N
    real(8), intent(in) :: u(N)
    real(8), intent(out) :: delta(N)
    integer :: i, im1, ip1
    real(8) :: du_back, du_forw, d2, d1, theta, eps

    eps = 1.0d-12

    do i = 1, N
      im1 = i - 1
      if (im1 < 1) im1 = N
      ip1 = i + 1
      if (ip1 > N) ip1 = 1

      du_back = u(i) - u(im1)
      du_forw = u(ip1) - u(i)

      d2 = abs(du_forw - du_back)
      d1 = abs(du_forw) + abs(du_back) + eps

      theta = min(d2 / d1, 1.0d0)
      delta(i) = (1.0d0 - theta) * du_forw
    end do
  end subroutine compute_delta_alw

  !===========================================================================
  ! Compute total variation: TV = sum_i |u_{i+1} - u_i| (periodic)
  !===========================================================================
  subroutine total_variation(N, u, tv)
    integer, intent(in) :: N
    real(8), intent(in) :: u(N)
    real(8), intent(out) :: tv
    integer :: i

    tv = 0.0d0
    do i = 1, N - 1
      tv = tv + abs(u(i+1) - u(i))
    end do
    tv = tv + abs(u(1) - u(N))
  end subroutine total_variation

  !===========================================================================
  ! Exact solution for smooth IC: u(x,t) = sin(pi * (x - a*t))
  !===========================================================================
  subroutine exact_solution(N, x, t, a, u_exact)
    integer, intent(in) :: N
    real(8), intent(in) :: x(N), t, a
    real(8), intent(out) :: u_exact(N)
    real(8), parameter :: pi = 3.141592653589793d0

    u_exact = sin(pi * (x - a * t))
  end subroutine exact_solution

  !===========================================================================
  ! Compute L1 and Linf error norms
  !===========================================================================
  subroutine compute_errors(N, u, u_exact, l1, linf)
    integer, intent(in) :: N
    real(8), intent(in) :: u(N), u_exact(N)
    real(8), intent(out) :: l1, linf
    integer :: i

    l1 = 0.0d0
    linf = 0.0d0
    do i = 1, N
      l1 = l1 + abs(u(i) - u_exact(i))
      linf = max(linf, abs(u(i) - u_exact(i)))
    end do
    l1 = l1 / N
  end subroutine compute_errors
