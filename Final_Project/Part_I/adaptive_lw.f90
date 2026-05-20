!==============================================================================
! Task 5: Adaptive Lax-Wendroff with Shock Sensor
! Runs ALW with discontinuous IC (square wave), compares with LW/VL/SB
!==============================================================================

program adaptive_lw
  implicit none

  integer, parameter :: N = 160
  real(8), parameter :: a = 1.0d0
  real(8), parameter :: xmin = -1.0d0, xmax = 1.0d0
  real(8), parameter :: Lx = xmax - xmin
  real(8), parameter :: dx = Lx / N
  real(8), parameter :: cfl = 0.8d0
  real(8), parameter :: dt = cfl * dx / a
  real(8), parameter :: t_out1 = 2.0d0, t_out2 = 8.0d0
  real(8), parameter :: nu = cfl

  real(8) :: x(N), u0(N), u(N), u_new(N), delta(N)
  real(8) :: t
  integer :: i, step, nsteps1, nsteps2

  do i = 1, N
    x(i) = xmin + (i - 0.5d0) * dx
  end do

  u0 = 0.0d0
  do i = 1, N
    if (x(i) > -0.5d0 .and. x(i) < 0.5d0) u0(i) = 1.0d0
  end do

  nsteps1 = nint(t_out1 / dt)
  nsteps2 = nint(t_out2 / dt)

  write(*, '(a,f10.6,a,f10.6)') 'dx=', dx, '  dt=', dt

  ! ---- Adaptive Lax-Wendroff ----
  u = u0
  t = 0.0d0
  do step = 1, nsteps2
    call compute_delta_alw(N, u, delta)
    call advance(N, nu, u, delta, u_new)
    u = u_new
    t = t + dt

    if (step == nsteps1) then
      call write_solution('adaptive_lw_t2.dat', N, x, u, u0, t)
    end if
  end do
  call write_solution('adaptive_lw_t8.dat', N, x, u, u0, t)

  ! ---- TV history for ALW ----
  call write_tv(N, nu, u0, dt, nsteps2)

  print *, 'Output: adaptive_lw_t2.dat, adaptive_lw_t8.dat, adaptive_tv.dat'

contains
  include 'schemes.inc'

  subroutine write_solution(filename, N, x, u, u_ana, t)
    character(len=*), intent(in) :: filename
    integer, intent(in) :: N
    real(8), intent(in) :: x(N), u(N), u_ana(N), t
    integer :: i

    open(20, file=filename, status='replace')
    write(20, '(a,f8.3)') '# t = ', t
    write(20, '(a)') '# x  u_numerical  u_analytical'
    do i = 1, N
      write(20, '(3f16.10)') x(i), u(i), u_ana(i)
    end do
    close(20)
  end subroutine write_solution

  subroutine write_tv(N, nu, u0, dt, nsteps)
    integer, intent(in) :: N, nsteps
    real(8), intent(in) :: nu, u0(N), dt
    real(8) :: u(N), delta(N), u_new(N), t, tv
    integer :: step, tv_skip

    tv_skip = max(1, nsteps / 500)
    u = u0
    t = 0.0d0

    open(21, file='adaptive_tv.dat', status='replace')
    write(21, '(a)') '# time  TV_ALW'
    call total_variation(N, u, tv)
    write(21, '(2f16.10)') 0.0d0, tv

    do step = 1, nsteps
      call compute_delta_alw(N, u, delta)
      call advance(N, nu, u, delta, u_new)
      u = u_new
      t = t + dt
      if (mod(step, tv_skip) == 0) then
        call total_variation(N, u, tv)
        write(21, '(2f16.10)') t, tv
      end if
    end do
    close(21)
  end subroutine write_tv

end program adaptive_lw
