program linear_advection_project
    implicit none
    
    ! =================================================================
    ! 命令行动态参数接收配置
    ! =================================================================
    character(len=32) :: arg_N, arg_scheme
    integer :: N                                ! 网格点数 (由外部动态传入)
    integer :: scheme_type                      ! 格式类型 (由外部动态传入: 1=LW, 2=vL, 3=SB)
    
    double precision, parameter :: L = 2.0d0    ! 物理域总长度 [-1, 1]
    double precision, parameter :: a = 1.0d0    ! 平流速度
    double precision, parameter :: cfl = 0.5d0  ! 设定的 CFL 数
    
    ! =================================================================
    ! 动态可分配数组声明 (完美解决 N 变化带来的数组大小问题)
    ! =================================================================
    double precision, allocatable, dimension(:) :: x, sigma
    double precision, allocatable, dimension(:) :: u, u_new
    
    ! 其他控制变量
    double precision :: dx, dt, t, tv_val, l2_err, l1_err
    double precision :: t_snapshot_1, t_snapshot_2
    integer :: i, step, total_steps, num_args
    logical :: saved_t2
    character(len=40) :: filename_t2, filename_t8, filename_tv
    
    ! 检查命令行参数个数 (去掉了会引起编译报错的英文半角叹号)
    num_args = command_argument_count()
    if (num_args < 2) then
        print *, "Error: Please provide arguments. Usage: ./cfd_solver <N> <scheme_type>"
        print *, "Example: ./cfd_solver 160 3"
        stop
    end if
    
    ! 从命令行动态读取自变量
    call get_command_argument(1, arg_N)
    call get_command_argument(2, arg_scheme)
    read(arg_N, *) N
    read(arg_scheme, *) scheme_type
    
    ! 根据传入参数动态分配流场数组内存
    allocate(u(0:N+1), u_new(0:N+1))
    allocate(x(1:N))
    allocate(sigma(0:N+1))  ! 【核心修复】将 sigma 同样扩展至包含幽灵单元 0 和 N+1
    
    ! 根据选择的格式以及网格数动态构建文件名
    select case(scheme_type)
    case(1)
        write(filename_t2, '(A,I0,A)') 'lw_result_t2_N', N, '.txt'
        write(filename_t8, '(A,I0,A)') 'lw_result_t8_N', N, '.txt'
        write(filename_tv, '(A,I0,A)') 'lw_tv_history_N', N, '.txt'
    case(2)
        write(filename_t2, '(A,I0,A)') 'vanleer_result_t2_N', N, '.txt'
        write(filename_t8, '(A,I0,A)') 'vanleer_result_t8_N', N, '.txt'
        write(filename_tv, '(A,I0,A)') 'vanleer_tv_history_N', N, '.txt'
    case(3)
        write(filename_t2, '(A,I0,A)') 'superbee_result_t2_N', N, '.txt'
        write(filename_t8, '(A,I0,A)') 'superbee_result_t8_N', N, '.txt'
        write(filename_tv, '(A,I0,A)') 'superbee_tv_history_N', N, '.txt'
    case default
        print *, "Error: Unknown scheme_type!"
        stop
    end select
    
    ! 计算网格步长和时间步长
    dx = L / dble(N)
    dt = cfl * dx / a
    
    ! 设置目标时间与中途抓拍点
    t_snapshot_1 = 2.0d0
    t_snapshot_2 = 8.0d0
    total_steps = nint(t_snapshot_2 / dt)
    
    ! =================================================================
    ! 核心推进核心：一气呵成从 t = 0 到 t = 8.0
    ! =================================================================
    call initialize_field(x, u, N, dx)
    t = 0.0d0
    saved_t2 = .false.
    
    ! 打开历史记录文件
    open(12, file=trim(filename_tv), status='replace')
    write(12, '(A20, A20, A20, A20)') "Time", "Total_Variation", "L2_Error", "L1_Error"
    
    ! 先记录下 t = 0 初始时刻的状态
    tv_val = calc_tv(u, N)
    l2_err = calc_l2_error(x, u, N, t)
    l1_err = calc_l1_error(x, u, N, t)
    write(12, '(4F20.8)') t, tv_val, l2_err, l1_err
    
    do step = 1, total_steps
        ! 1. 同步流场的周期性边界条件
        u(0)   = u(N)
        u(N+1) = u(1)
        
        ! 2. 计算细胞斜率 sigma (内部会自动同步 sigma 的幽灵单元)
        call compute_slopes(u, sigma, N, dx, scheme_type)
        
        ! 3. 有限体积主格式核心推进 (此时 i=1 时读取 sigma(0) 已经是合法的周期性边界值)
        do i = 1, N
            u_new(i) = u(i) - (a * dt / dx) * (u(i) - u(i-1)) &
                       - (a * dt / (2.0d0 * dx)) * (dx - a * dt) * (sigma(i) - sigma(i-1))
        end do
        
        u(1:N) = u_new(1:N)
        t = t + dt
        
        ! 4. 全程实时计算当前步的 TV 值与误差并写入历史文件
        tv_val = calc_tv(u, N)
        l2_err = calc_l2_error(x, u, N, t)
        l1_err = calc_l1_error(x, u, N, t)
        write(12, '(4F20.8)') t, tv_val, l2_err, l1_err
        
        ! 5. 【中途智能截获】当推进到约 t = 2.0 时，保存第一组画图快照
        if (.not. saved_t2 .and. (t >= t_snapshot_1 - 1.0d-7)) then
            open(10, file=trim(filename_t2), status='replace')
            write(10, '(A20, A20, A20)') "x", "u_numerical", "u_analytical"
            do i = 1, N
                write(10, '(3F20.8)') x(i), u(i), analytical_sol(x(i), t)
            end do
            close(10)
            saved_t2 = .true.
            
            ! 打印供 Python 全自动抓取收集的标志
            print *, "RESULTS_T2:", scheme_type, N, l1_err, l2_err
        end if
    end do
    close(12)
    
    ! 6. 运行到终点，导出 t = 8.0 的数值解与解析解对比数据
    open(11, file=trim(filename_t8), status='replace')
    write(11, '(A20, A20, A20)') "x", "u_numerical", "u_analytical"
    do i = 1, N
        write(11, '(3F20.8)') x(i), u(i), analytical_sol(x(i), t)
    end do
    close(11)
    
    ! 释放动态分配的内存空间
    deallocate(u, u_new, x, sigma)

contains

    ! --- 子程序：初始化流场 ---
    subroutine initialize_field(x, u, N, dx)
        integer, intent(in) :: N
        double precision, intent(in) :: dx
        double precision, dimension(1:N), intent(out) :: x
        double precision, dimension(0:N+1), intent(out) :: u
        integer :: i
        
        do i = 1, N
            x(i) = -1.0d0 + (dble(i) - 0.5d0) * dx
            if (x(i) > -0.5d0 .and. x(i) < 0.5d0) then
                u(i) = 1.0d0
            else
                u(i) = 0.0d0
            end if
        end do
    end subroutine initialize_field

    ! --- 子程序：斜率重构计算核心 ---
    subroutine compute_slopes(u, sigma, N, dx, stype)
        integer, intent(in) :: N, stype
        double precision, intent(in) :: dx
        double precision, dimension(0:N+1), intent(in) :: u
        double precision, dimension(0:N+1), intent(out) :: sigma ! 【核心修复】扩展为 0:N+1
        
        integer :: j
        double precision :: s1, s2, sig_L, sig_R
        
        ! 1. 计算内部单元网格的物理斜率
        do j = 1, N
            s1 = (u(j+1) - u(j)) / dx
            s2 = (u(j) - u(j-1)) / dx
            
            select case(stype)
            case(1) 
                sigma(j) = s1
            case(2) 
                if (abs(s1) + abs(s2) > 1.0d-14) then
                    sigma(j) = (sign(1.0d0, s1) + sign(1.0d0, s2)) * (abs(s1) * abs(s2)) / (abs(s1) + abs(s2))
                else
                    sigma(j) = 0.0d0
                end if
            case(3) 
                sig_L = minmod(2.0d0 * s2, s1)
                sig_R = minmod(s2, 2.0d0 * s1)
                sigma(j) = maxmod(sig_L, sig_R)
            end select
        end do

        ! 2. 【核心修复】在这里强行同步斜率数组的周期性边界条件！
        sigma(0)   = sigma(N)
        sigma(N+1) = sigma(1)
        
    end subroutine compute_slopes

    ! --- 函数：minmod 算子 ---
    double precision function minmod(a, b)
        double precision, intent(in) :: a, b
        if (a * b > 0.0d0) then
            if (abs(a) < abs(b)) then
                minmod = a
            else
                minmod = b
            end if
        else
            minmod = 0.0d0
        end if
    end function minmod

    ! --- 函数：maxmod 算子 ---
    double precision function maxmod(a, b)
        double precision, intent(in) :: a, b
        if (a * b > 0.0d0) then
            if (abs(a) > abs(b)) then
                maxmod = a
            else
                maxmod = b
            end if
        else
            maxmod = 0.0d0
        end if
    end function maxmod

    ! --- 函数：计算理论解析解 ---
    double precision function analytical_sol(x_val, t_val)
        double precision, intent(in) :: x_val, t_val
        double precision :: shifted_x
        
        shifted_x = x_val - a * t_val
        do while (shifted_x < -1.0d0)
            shifted_x = shifted_x + 2.0d0
        end do
        do while (shifted_x > 1.0d0)
            shifted_x = shifted_x - 2.0d0
        end do
        
        if (shifted_x > -0.5d0 .and. shifted_x < 0.5d0) then
            analytical_sol = 1.0d0
        else
            analytical_sol = 0.0d0
        end if
    end function analytical_sol

    ! --- 函数：计算当前流场的全变差 ---
    double precision function calc_tv(u_arr, N)
        integer, intent(in) :: N
        double precision, dimension(0:N+1), intent(in) :: u_arr
        integer :: i
        
        calc_tv = 0.0d0
        do i = 1, N-1
            calc_tv = calc_tv + abs(u_arr(i+1) - u_arr(i))
        end do
        calc_tv = calc_tv + abs(u_arr(1) - u_arr(N))
    end function calc_tv

    ! --- 函数：计算当前流场的 L2 空间数值误差 ---
    double precision function calc_l2_error(x_arr, u_arr, N, t_val)
        integer, intent(in) :: N
        double precision, intent(in) :: t_val
        double precision, dimension(1:N), intent(in) :: x_arr
        double precision, dimension(0:N+1), intent(in) :: u_arr
        integer :: i
        double precision :: sum_sq
        
        sum_sq = 0.0d0
        do i = 1, N
            sum_sq = sum_sq + (u_arr(i) - analytical_sol(x_arr(i), t_val))**2
        end do
        calc_l2_error = sqrt(sum_sq / dble(N))
    end function calc_l2_error

    ! --- 函数：计算当前流场的 L1 空间数值误差 ---
    double precision function calc_l1_error(x_arr, u_arr, N, t_val)
        integer, intent(in) :: N
        double precision, intent(in) :: t_val
        double precision, dimension(1:N), intent(in) :: x_arr
        double precision, dimension(0:N+1), intent(in) :: u_arr
        integer :: i
        double precision :: sum_abs
        
        sum_abs = 0.0d0
        do i = 1, N
            sum_abs = sum_abs + abs(u_arr(i) - analytical_sol(x_arr(i), t_val))
        end do
        calc_l1_error = sum_abs / dble(N)
    end function calc_l1_error

end program linear_advection_project