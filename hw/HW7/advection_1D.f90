program main
implicit none

! ======================
! 参数设置
! ======================
integer, parameter :: N = 160
real*8, parameter  :: a = 1.0d0
real*8, parameter  :: L = 2.0d0
real*8, parameter  :: C = 0.5d0

real*8 :: l1_up, l1_lw, l1_b
real*8 :: l2_up, l2_lw, l2_b

real*8 :: dx, dt, t, Tend
integer :: nsteps, it, j

! ======================
! 数组（带虚拟节点）
! ======================
real*8, dimension(-1:N+2) :: u_up, u_lw, u_b, u_exact
real*8, dimension(-1:N+2) :: uold_up, uold_lw, uold_b

real*8 :: x, pi

! ======================
! 初始化
! ======================
dx = L / real(N)
dt = C * dx / a

pi = 4.0d0 * atan(1.0d0)

Tend = 1.5d0
nsteps = int(Tend/dt) + 1

open(10, file='output13.dat', status='replace')
open(20, file='error13.dat', status='replace')

write(*,*) 'nsteps = ', nsteps

! ======================
! 初始条件
! ======================
do j = 1, N

    x = (j-1)*dx

    u_up(j) = sin(pi*x) + 0.6d0*sin(3.0d0*pi*x)

    u_lw(j) = u_up(j)
    u_b(j)  = u_up(j)

end do

t = 0.d0

! ======================
! 时间推进
! ======================
do it = 1, nsteps

    ! ======================
    ! 周期边界
    ! ======================

    ! Upwind
    u_up(0)   = u_up(N)
    u_up(-1)  = u_up(N-1)
    u_up(N+1) = u_up(1)
    u_up(N+2) = u_up(2)

    ! Lax-Wendroff
    u_lw(0)   = u_lw(N)
    u_lw(-1)  = u_lw(N-1)
    u_lw(N+1) = u_lw(1)
    u_lw(N+2) = u_lw(2)

    ! Scheme B
    u_b(0)   = u_b(N)
    u_b(-1)  = u_b(N-1)
    u_b(N+1) = u_b(1)
    u_b(N+2) = u_b(2)

    ! ======================
    ! 保存旧值
    ! ======================
    uold_up = u_up
    uold_lw = u_lw
    uold_b  = u_b

    ! ======================
    ! 三种格式
    ! ======================
    do j = 1, N

        ! --------------------------------
        ! Upwind
        ! --------------------------------
        u_up(j) = uold_up(j) &
                - C * (uold_up(j) - uold_up(j-1))

        ! --------------------------------
        ! Lax-Wendroff
        ! --------------------------------
        u_lw(j) = uold_lw(j) &
                - 0.5d0*C*(uold_lw(j+1) - uold_lw(j-1)) &
                + 0.5d0*C*C*(uold_lw(j+1) - 2.d0*uold_lw(j) + uold_lw(j-1))

        ! --------------------------------
        ! Scheme B
        ! --------------------------------
        u_b(j) = uold_b(j) &
               - C*(uold_b(j) - uold_b(j-1)) &
               - 0.5d0*C*(1.d0-C) &
               * (uold_b(j) - 2.d0*uold_b(j-1) + uold_b(j-2))

    end do

    t = t + dt

    ! ======================
    ! 精确解
    ! ======================
    do j = 1, N

        x = (j-1)*dx

        u_exact(j) = sin(pi*(x - t)) &
                   + 0.6d0*sin(3.0d0*pi*(x - t))

    end do

    ! ======================
    ! 初始化误差
    ! ======================
    l1_up = 0.d0
    l1_lw = 0.d0
    l1_b  = 0.d0

    l2_up = 0.d0
    l2_lw = 0.d0
    l2_b  = 0.d0

    ! ======================
    ! 计算误差
    ! ======================
    do j = 1, N

        l1_up = l1_up + abs(u_up(j) - u_exact(j))
        l1_lw = l1_lw + abs(u_lw(j) - u_exact(j))
        l1_b  = l1_b  + abs(u_b(j)  - u_exact(j))

        l2_up = l2_up + (u_up(j) - u_exact(j))**2
        l2_lw = l2_lw + (u_lw(j) - u_exact(j))**2
        l2_b  = l2_b  + (u_b(j)  - u_exact(j))**2

    end do

    ! ======================
    ! normalize
    ! ======================
    l1_up = l1_up / N
    l1_lw = l1_lw / N
    l1_b  = l1_b  / N

    l2_up = sqrt(l2_up / N)
    l2_lw = sqrt(l2_lw / N)
    l2_b  = sqrt(l2_b  / N)

    ! ======================
    ! 输出指定时间
    ! ======================
    if (abs(t - 0.5d0) < dt/2.d0 .or. &
        abs(t - 1.5d0) < dt/2.d0) then

        do j = 1, N

            x = (j-1)*dx

            write(10,*) t, x, &
                        u_up(j), &
                        u_lw(j), &
                        u_b(j), &
                        u_exact(j)

        end do

        write(10,*)

    end if

    ! ======================
    ! 输出误差随时间变化
    ! ======================
    write(20,*) t, &
                l1_up, l1_lw, l1_b, &
                l2_up, l2_lw, l2_b

end do

close(10)
close(20)

print*, "Simulation done."
print*, "Solution  : output13.dat"
print*, "Error data: error13.dat"

end program