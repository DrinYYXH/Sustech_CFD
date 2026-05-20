!==============================================================================
! Task 3: Order of Accuracy Study
! Grid refinement using smooth initial condition u(x,0) = sin(pi*x)
! N = 20, 40, 80, 160, 320  at CFL = 0.8, t_end = 1.0
!==============================================================================

program convergence_study
  implicit none

  integer, parameter :: num_N = 5
  integer, parameter :: N_vals(num_N) = (/ 20, 40, 80, 160, 320 /)
  real(8), parameter :: a = 1.0d0
  real(8), parameter :: xmin = -1.0d0, xmax = 1.0d0
  real(8), parameter :: Lx = xmax - xmin
  real(8), parameter :: cfl = 0.8d0
  real(8), parameter :: t_end = 1.0d0

  integer :: nidx, N, nsteps, step, i
  real(8) :: dx, dt, nu, t_actual, l1, linf
  real(8), allocatable :: x(:), u0(:), u(:), u_new(:), delta(:), u_exact(:)

  open(10, file='convergence.dat', status='replace')
  write(10, '(a)') '# N  dx  L1_LW  Linf_LW  L1_VL  Linf_VL  L1_SB  Linf_SB'

  do nidx = 1, num_N
    N = N_vals(nidx)
    dx = Lx / N
    dt = cfl * dx / a
    nu = cfl
    nsteps = nint(t_end / dt)

    allocate(x(N), u0(N), u(N), u_new(N), delta(N), u_exact(N))

    do i = 1, N
      x(i) = xmin + (i - 0.5d0) * dx
    end do

    u0 = sin(3.141592653589793d0 * x)
    t_actual = nsteps * dt

    write(*, '(a,i4,a,f8.4,a,i6,a,f10.6)') &
      'N=', N, '  dx=', dx, '  nsteps=', nsteps, '  t=', t_actual

    ! ---- LW ----
    u = u0
    do step = 1, nsteps
      call compute_delta_lw(N, u, delta)
      call advance(N, nu, u, delta, u_new)
      u = u_new
    end do
    call exact_solution(N, x, t_actual, a, u_exact)
    call compute_errors(N, u, u_exact, l1, linf)
    write(*, '(a,es12.4,a,es12.4)') '  LW:  L1=', l1, '  Linf=', linf
    write(10, '(i5,f12.8,2es16.8)', advance='no') N, dx, l1, linf

    ! ---- van Leer ----
    u = u0
    do step = 1, nsteps
      call compute_delta_vl(N, u, delta)
      call advance(N, nu, u, delta, u_new)
      u = u_new
    end do
    call exact_solution(N, x, t_actual, a, u_exact)
    call compute_errors(N, u, u_exact, l1, linf)
    write(*, '(a,es12.4,a,es12.4)') '  VL:  L1=', l1, '  Linf=', linf
    write(10, '(2es16.8)', advance='no') l1, linf

    ! ---- SUPERBEE ----
    u = u0
    do step = 1, nsteps
      call compute_delta_sb(N, u, delta)
      call advance(N, nu, u, delta, u_new)
      u = u_new
    end do
    call exact_solution(N, x, t_actual, a, u_exact)
    call compute_errors(N, u, u_exact, l1, linf)
    write(*, '(a,es12.4,a,es12.4)') '  SB:  L1=', l1, '  Linf=', linf
    write(10, '(2es16.8)') l1, linf

    deallocate(x, u0, u, u_new, delta, u_exact)
  end do

  close(10)
  print *, 'Convergence data written to convergence.dat'

contains
  include 'schemes.inc'
end program convergence_study
