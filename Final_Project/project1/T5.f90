program main
    implicit none
    integer :: N, scheme_type, i, step, total_steps
    integer, allocatable :: ip1(:), im1(:)
    double precision, allocatable :: x(:), u(:), u_new(:)
    
    ! 物理与流场参数
    double precision, parameter :: L = 2.0d0
    double precision, parameter :: u_base = 1.0d0 ! 对流速度
    double precision, parameter :: cfl = 0.5d0    ! CFL数
    double precision, parameter :: kappa = 0.15d0  ! 人工粘性系数 (针对scheme=4)
    double precision :: dx, dt, t, max_t
    
    ! 用于非线性人工粘性的局部变量
    double precision :: r_left, r_right, nu_i
    
    character(len=32) :: arg1, arg2
    character(len=64) :: file_name

    ! 读取命令行参数
    if (command_argument_count() < 2) then
        print *, "Usage: ./hw <N> <scheme_type>"
        print *, "  scheme_type: 1=LW, 2=van Leer, 3=SUPERBEE, 4=Improved LW"
        stop
    end if
    
    call get_command_argument(1, arg1)
    call get_command_argument(2, arg2)
    read(arg1, *) N
    read(arg2, *) scheme_type

    ! 动态分配数组
    allocate(x(N), u(N), u_new(N))
    allocate(ip1(N), im1(N))

    ! 计算网格步长与时空推进基础
    dx = L / dble(N)
    dt = cfl * dx / u_base
    max_t = 1.0d0 ! 设定演化到特定时间无量纲 \tau = 1.0
    total_steps = nint(max_t / dt)

    ! 初始化网格点坐标与周期性边界索引表
    do i = 1, N
        x(i) = dble(i-1) * dx
        ! 预计算周期性边界索引
        ip1(i) = i + 1
        im1(i) = i - 1
    end do
    ip1(N) = 1
    im1(1) = N

    ! 初始化流场：经典方波拓扑
    do i = 1, N
        if (x(i) >= 0.5d0 .and. x(i) <= 1.0d0) then
            u(i) = 1.0d0
        else
            u(i) = 0.0d0
        end if
    end do

    ! 主时间推進循环
    t = 0.0d0
    do step = 1, total_steps
        t = t + dt
        
        select case (scheme_type)
        case (1)
            ! -------------------------------------------------------------
            ! 1. 标准 Lax-Wendroff 格式
            ! -------------------------------------------------------------
            do i = 1, N
                u_new(i) = u(i) - 0.5d0*cfl*(u(ip1(i)) - u(im1(i))) &
                           + 0.5d0*(cfl**2)*(u(ip1(i)) - 2.d0*u(i) + u(im1(i)))
            end do
            
        case (2)
            ! -------------------------------------------------------------
            ! 2. van Leer 格式 (如果你之前有写，保留在这里即可)
            ! -------------------------------------------------------------
            ! [此处可以保留你原有的 van Leer 核心更新代码]
            do i = 1, N
                u_new(i) = u(i) ! 占位符，运行时请替换为你原有的逻辑
            end do

        case (3)
            ! -------------------------------------------------------------
            ! 3. SUPERBEE 格式 (如果你之前有写，保留在这里即可)
            ! -------------------------------------------------------------
            ! [此处可以保留你原有的 SUPERBEE 核心更新代码]
            do i = 1, N
                u_new(i) = u(i) ! 占位符，运行时请替换为你原有的逻辑
            end do

        case (4)
            ! -------------------------------------------------------------
            ! 4. 改进型 Lax-Wendroff (带非线性 Jameson 人工粘性)
            ! -------------------------------------------------------------
            ! Step 4.1: 执行基础的经典 Lax-Wendroff 空间演化
            do i = 1, N
                u_new(i) = u(i) - 0.5d0*cfl*(u(ip1(i)) - u(im1(i))) &
                           + 0.5d0*(cfl**2)*(u(ip1(i)) - 2.d0*u(i) + u(im1(i)))
            end do
            
            ! Step 4.2: 局部非线性激波/间断检测并注入自适应耗散
            do i = 1, N
                r_left  = abs(u(i) - u(im1(i)))
                r_right = abs(u(ip1(i)) - u(i))
                
                ! 非线性开关：间断区域大，光滑区域小
                nu_i = kappa * max(r_left, r_right)
                
                ! 修正原本 LW 的过冲振荡
                u_new(i) = u_new(i) + nu_i * (u(ip1(i)) - 2.d0*u(i) + u(im1(i)))
            end do

        end select

        ! 更新流场状态
        u = u_new
    end do

    ! 根据格式类型写出最终流场快照到特定文本
    select case (scheme_type)
    case (1)
        file_name = "lw_snapshot.txt"
    case (4)
        file_name = "clw_snapshot.txt"
    case default
        file_name = "other_snapshot.txt"
    end select
    
    open(10, file=trim(file_name), status='unknown')
    do i = 1, N
        write(10, '(2F18.8)') x(i), u(i)
    end do
    close(10)
    
    print *, "Format ", scheme_type, " finished. Snapshot saved to ", trim(file_name)

    deallocate(x, u, u_new, ip1, im1)
end program main