program float_binary
    implicit none
    real :: x
    integer :: i
    integer, dimension(32) :: bits
    
    ! 读取输入
    print *, 'Enter a real number:'
    read *, x
    
    ! 将实数的内存表示转换为整数
    ! 使用 transfer 函数和等价语句
    block
        integer :: ix
        ix = transfer(x, 1)
        
        ! 提取每一位
        do i = 1, 32
            bits(i) = ibits(ix, 32-i, 1)
        end do
    end block
    
    ! 输出二进制表示
    print '(A)', 'Binary representation (32 bits):'
    write(*, '(32I1)') (bits(i), i=1,32)
    
    ! 按 IEEE 754 格式分组输出：符号位 | 指数位 | 尾数位
    print '(A)', 'Format: sign | exponent | mantissa'
    write(*, '(I1, A, 8I1, A, 23I1)') bits(1), ' | ', (bits(i), i=2,9), ' | ', (bits(i), i=10,32)
    
end program float_binary