!==============================================================================
! MAE5005 / MAE403 Computational Fluid Dynamics, Spring 2026
! Part I: 1D Linear Advection Equation with Discontinuous Initial Condition
!
! Three schemes implemented in a unified MUSCL framework:
!   u_j^{n+1} = u_j^n - nu*(u_j - u_{j-1}) - 0.5*nu*(1-nu)*(delta_j - delta_{j-1})
!   where nu = a*dt/dx, delta_j = sigma_j * dx
!
! Scheme 1: Lax-Wendroff      -> delta_j = u_{j+1} - u_j   (downwind slope)
! Scheme 2: van Leer limiter  -> delta_j = phi_VL(r_j) * (u_{j+1} - u_j)
! Scheme 3: SUPERBEE limiter  -> delta_j = phi_SB(r_j) * (u_{j+1} - u_j)
!==============================================================================

program linear_advection
  implicit none

  ! --- Grid parameters ---
  integer, parameter :: N = 160
  real(8), parameter :: a = 1.0d0
  real(8), parameter :: xmin = -1.0d0, xmax = 1.0d0
  real(8), parameter :: Lx = xmax - xmin
  real(8), parameter :: dx = Lx / N

  ! --- Time parameters ---
  real(8), parameter :: cfl = 0.8d0
  real(8), parameter :: dt = cfl * dx / a
  real(8), parameter :: t_out1 = 2.0d0
  real(8), parameter :: t_out2 = 8.0d0

  ! --- Arrays ---
  real(8) :: x(N), u0(N), u(N), u_new(N)
  real(8) :: delta(N)
  real(8) :: t, nu
  integer :: i, step, nsteps1, nsteps2, tv_skip
  real(8) :: tv

  ! --- Output files ---
  integer, parameter :: f_lw = 10, f_vl = 11, f_sb = 12

  ! Derived parameters
  nu = cfl
  nsteps1 = nint(t_out1 / dt)
  nsteps2 = nint(t_out2 / dt)

  ! Initialize grid
  do i = 1, N
    x(i) = xmin + (i - 0.5d0) * dx
  end do

  ! Initial condition: square wave
  u0 = 0.0d0
  do i = 1, N
    if (x(i) > -0.5d0 .and. x(i) < 0.5d0) then
      u0(i) = 1.0d0
    end if
  end do

  ! Open TV output file (will be merged from temp files)
  tv_skip = max(1, nsteps2 / 500)

  !=========================================================================
  ! Run all three schemes with inline TV tracking
  !=========================================================================

  ! ---- Scheme 1: Lax-Wendroff ----
  u = u0
  t = 0.0d0
  open(20, file='tv_lw_temp.dat', status='replace')
  call total_variation(N, u, tv)
  write(20, '(f12.6,f16.10)') 0.0d0, tv

  do step = 1, nsteps2
    call compute_delta_lw(N, u, delta)
    call advance(N, nu, u, delta, u_new)
    u = u_new
    t = t + dt

    if (mod(step, tv_skip) == 0) then
      call total_variation(N, u, tv)
      write(20, '(f12.6,f16.10)') t, tv
    end if

    if (step == nsteps1) then
      call write_solution(f_lw, 'lax_wendroff_t2.dat', N, x, u, u0, t)
    end if
  end do
  call write_solution(f_lw, 'lax_wendroff_t8.dat', N, x, u, u0, t)
  close(20)

  ! ---- Scheme 2: van Leer ----
  u = u0
  t = 0.0d0
  open(21, file='tv_vl_temp.dat', status='replace')
  call total_variation(N, u, tv)
  write(21, '(f12.6,f16.10)') 0.0d0, tv

  do step = 1, nsteps2
    call compute_delta_vl(N, u, delta)
    call advance(N, nu, u, delta, u_new)
    u = u_new
    t = t + dt

    if (mod(step, tv_skip) == 0) then
      call total_variation(N, u, tv)
      write(21, '(f12.6,f16.10)') t, tv
    end if

    if (step == nsteps1) then
      call write_solution(f_vl, 'van_leer_t2.dat', N, x, u, u0, t)
    end if
  end do
  call write_solution(f_vl, 'van_leer_t8.dat', N, x, u, u0, t)
  close(21)

  ! ---- Scheme 3: SUPERBEE ----
  u = u0
  t = 0.0d0
  open(22, file='tv_sb_temp.dat', status='replace')
  call total_variation(N, u, tv)
  write(22, '(f12.6,f16.10)') 0.0d0, tv

  do step = 1, nsteps2
    call compute_delta_sb(N, u, delta)
    call advance(N, nu, u, delta, u_new)
    u = u_new
    t = t + dt

    if (mod(step, tv_skip) == 0) then
      call total_variation(N, u, tv)
      write(22, '(f12.6,f16.10)') t, tv
    end if

    if (step == nsteps1) then
      call write_solution(f_sb, 'superbee_t2.dat', N, x, u, u0, t)
    end if
  end do
  call write_solution(f_sb, 'superbee_t8.dat', N, x, u, u0, t)
  close(22)

  !=========================================================================
  ! Merge TV temp files into total_variation.dat
  !=========================================================================
  call merge_tv_files()

  print *, 'Done. Output files:'
  print *, '  lax_wendroff_t2.dat, lax_wendroff_t8.dat'
  print *, '  van_leer_t2.dat, van_leer_t8.dat'
  print *, '  superbee_t2.dat, superbee_t8.dat'
  print *, '  total_variation.dat'

contains

  !===========================================================================
  ! Advance one time step using the unified MUSCL scheme
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
  ! Slope for Lax-Wendroff (downwind slope, no limiter)
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
  ! Slope for van Leer limiter
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
  ! Slope for SUPERBEE limiter
  !   phi_SB(r) = max(0, min(2r, 1), min(r, 2))
  !   r_j = (u_j - u_{j-1}) / (u_{j+1} - u_j)
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
  ! Write solution to file
  !===========================================================================
  subroutine write_solution(unit, filename, N, x, u, u_ana, t)
    integer, intent(in) :: unit, N
    character(len=*), intent(in) :: filename
    real(8), intent(in) :: x(N), u(N), u_ana(N), t
    integer :: i

    open(unit, file=filename, status='replace')
    write(unit, '(a,f8.3)') '# t = ', t
    write(unit, '(a)') '# x  u_numerical  u_analytical'
    do i = 1, N
      write(unit, '(3f16.10)') x(i), u(i), u_ana(i)
    end do
    close(unit)
  end subroutine write_solution

  !===========================================================================
  ! Compute total variation
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
    tv = tv + abs(u(1) - u(N))   ! wrap-around term
  end subroutine total_variation

  !===========================================================================
  ! Merge three temporary TV files into one
  !===========================================================================
  subroutine merge_tv_files()
    real(8) :: t_lw, tv_lw, t_vl, tv_vl, t_sb, tv_sb
    integer :: ios

    open(20, file='tv_lw_temp.dat', status='old')
    open(21, file='tv_vl_temp.dat', status='old')
    open(22, file='tv_sb_temp.dat', status='old')
    open(23, file='total_variation.dat', status='replace')
    write(23, '(a)') '# time  TV_LW  TV_VL  TV_SB'

    do
      read(20, *, iostat=ios) t_lw, tv_lw
      if (ios /= 0) exit
      read(21, *, iostat=ios) t_vl, tv_vl
      if (ios /= 0) exit
      read(22, *, iostat=ios) t_sb, tv_sb
      if (ios /= 0) exit
      write(23, '(4f16.10)') t_lw, tv_lw, tv_vl, tv_sb
    end do

    close(20, status='delete')
    close(21, status='delete')
    close(22, status='delete')
    close(23)
  end subroutine merge_tv_files

end program linear_advection
