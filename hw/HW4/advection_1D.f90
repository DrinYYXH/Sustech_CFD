program main
implicit none

! ======================
! 参数设置
! ======================
integer, parameter :: N = 160       ! 改成 160 做(c)(d)
real*8, parameter  :: a = 1.0d0
real*8, parameter  :: L = 2.0d0
real*8, parameter  :: C = 0.5d0

real*8 :: l1_up, l1_cen, l1_down
real*8 :: l2_up, l2_cen, l2_down

real*8 :: dx, dt, t, Tend
integer :: nsteps, it, j

! ======================
! 数组（带虚拟节点）
! ======================
real*8, dimension(0:N+1) :: u_up, u_down, u_cen, u_exact
real*8, dimension(0:N+1) :: uold_up, uold_down, uold_cen
real*8 :: x, pi

! ======================
! 初始化
! ======================
dx = L / real(N)
dt = C * dx / a

pi = 4.0d0*atan(1.0d0)

Tend = 1.5d0
nsteps = int(Tend/dt) + 1

open(10, file='output13.dat', status='replace')

write(*,*) 'nsteps=' ,nsteps

! 初始条件
do j = 1, N
    x = (j-1)*dx
    u_up(j)   = sin(pi*x) + 0.6d0*sin(3.0d0*pi*x)
    u_down(j) = u_up(j)
    u_cen(j)  = u_up(j)
end do

t = 0.d0

! ======================
! 时间推进
! ======================
do it = 1, nsteps

    ! 周期边界
    u_up(0)   = u_up(N)
    u_up(N+1) = u_up(1)

    u_down(0)   = u_down(N)
    u_down(N+1) = u_down(1)

    u_cen(0)   = u_cen(N)
    u_cen(N+1) = u_cen(1)

    ! 保存旧值
    uold_up   = u_up
    uold_down = u_down
    uold_cen  = u_cen

    ! ===== 三种格式 =====
    do j = 1, N

        ! Upwind
        u_up(j) = uold_up(j) - C*(uold_up(j) - uold_up(j-1))

        ! Downwind
        u_down(j) = uold_down(j) - C*(uold_down(j+1) - uold_down(j))

        ! Central
        u_cen(j) = uold_cen(j) - 0.5d0*C*(uold_cen(j+1) - uold_cen(j-1))

    end do

    t = t + dt

    l1_up = 0.d0
    l1_cen = 0.d0
    l1_down = 0.d0

    l2_up = 0.d0
    l2_cen = 0.d0
    l2_down = 0.d0

    do j = 1, N

        l1_up = l1_up + abs(u_up(j) - u_exact(j))
        l1_cen = l1_cen + abs(u_cen(j) - u_exact(j))
        l1_down = l1_down + abs(u_down(j) - u_exact(j))

        l2_up = l2_up + (u_up(j) - u_exact(j))**2
        l2_cen = l2_cen + (u_cen(j) - u_exact(j))**2
        l2_down = l2_down + (u_down(j) - u_exact(j))**2

    end do

    ! =========================
    ! normalize
    ! =========================
    l1_up = l1_up / N
    l1_cen = l1_cen / N
    l1_down = l1_down / N

    l2_up = sqrt(l2_up / N)
    l2_cen = sqrt(l2_cen / N)
    l2_down = sqrt(l2_down / N)

    ! ======================
    ! 输出（指定时间）
    ! ======================
    if (abs(t - 0.5d0) < dt/2.d0 .or. abs(t - 1.5d0) < dt/2.d0) then

        do j = 1, N
            x = (j-1)*dx

            ! 精确解
            u_exact(j) = sin(pi*(x - t)) + 0.6d0*sin(3.0d0*pi*(x - t))

            write(10,*) t, x, u_up(j), u_down(j), u_cen(j), u_exact(j)
            write(20,*) t, l1_up, l1_cen, l1_down, l2_up, l2_cen, l2_down
        end do

        write(10,*)   ! 空行分隔不同时间

    end if

end do

!100 format(6f16.8)

close(10)

print*, "Simulation done. Output in output13.dat"

end program