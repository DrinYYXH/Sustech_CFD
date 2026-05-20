!==============================================================================
! Task 4: Numerical Stability Study
! Run with CFL = 0.5, 0.8, 1.0, 1.05, 1.1 on smooth IC sin(pi*x)
! Track max|u| vs time to detect instability
!==============================================================================

program stability_study
  implicit none

  integer, parameter :: N = 80
  integer, parameter :: num_cfl = 5
  real(8), parameter :: cfl_vals(num_cfl) = (/ 0.5d0, 0.8d0, 1.0d0, 1.05d0, 1.1d0 /)
  real(8), parameter :: a = 1.0d0
  real(8), parameter :: xmin = -1.0d0, xmax = 1.0d0
  real(8), parameter :: Lx = xmax - xmin
  real(8), parameter :: dx = Lx / N
  real(8), parameter :: t_end = 10.0d0
  real(8), parameter :: blowup = 1.0d10

  integer :: cidx, step, nsteps, output_every, i
  real(8) :: cfl, dt, nu, t, umax
  real(8) :: x(N), u0(N), u(N), u_new(N), delta(N)

  do i = 1, N
    x(i) = xmin + (i - 0.5d0) * dx
  end do
  u0 = sin(3.141592653589793d0 * x)

  open(10, file='stability_maxval.dat', status='replace')
  write(10, '(a)') '# CFL  scheme  time  max|u|'

  do cidx = 1, num_cfl
    cfl = cfl_vals(cidx)
    dt = cfl * dx / a
    nu = cfl
    nsteps = nint(t_end / dt)
    output_every = max(1, nsteps / 200)

    write(*, '(a,f5.2,a,f10.6,a,i8)') &
      'CFL=', cfl, '  dt=', dt, '  nsteps=', nsteps

    ! ---- LW ----
    u = u0; t = 0.0d0
    do step = 0, nsteps
      if (mod(step, output_every) == 0) then
        umax = maxval(abs(u))
        write(10, '(f5.2,3x,a3,f12.6,es16.6)') cfl, 'LW ', t, umax
        if (umax > blowup .or. umax /= umax) then
          write(*, '(a)') '  LW:  UNSTABLE at t=', t
          exit
        end if
      end if
      if (step == nsteps) exit
      call compute_delta_lw(N, u, delta)
      call advance(N, nu, u, delta, u_new)
      u = u_new; t = t + dt
    end do

    ! ---- van Leer ----
    u = u0; t = 0.0d0
    do step = 0, nsteps
      if (mod(step, output_every) == 0) then
        umax = maxval(abs(u))
        write(10, '(f5.2,3x,a3,f12.6,es16.6)') cfl, 'VL ', t, umax
        if (umax > blowup .or. umax /= umax) then
          write(*, '(a)') '  VL:  UNSTABLE at t=', t
          exit
        end if
      end if
      if (step == nsteps) exit
      call compute_delta_vl(N, u, delta)
      call advance(N, nu, u, delta, u_new)
      u = u_new; t = t + dt
    end do

    ! ---- SUPERBEE ----
    u = u0; t = 0.0d0
    do step = 0, nsteps
      if (mod(step, output_every) == 0) then
        umax = maxval(abs(u))
        write(10, '(f5.2,3x,a3,f12.6,es16.6)') cfl, 'SB ', t, umax
        if (umax > blowup .or. umax /= umax) then
          write(*, '(a)') '  SB:  UNSTABLE at t=', t
          exit
        end if
      end if
      if (step == nsteps) exit
      call compute_delta_sb(N, u, delta)
      call advance(N, nu, u, delta, u_new)
      u = u_new; t = t + dt
    end do

  end do

  close(10)
  print *, 'Stability data written to stability_maxval.dat'

contains
  include 'schemes.inc'
end program stability_study
