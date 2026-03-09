program main
    implicit none
    integer, parameter :: N = 600
    integer :: M
    real(kind=8) :: P, P0
    character(len=20) :: filename

    filename = 'prob_N600.dat'
    open(unit=10, file=filename, status='replace')

    ! 计算 P(0) = 1 / 2^N
    P0 = 1.0d0 / (2.0d0 ** N)

    P = P0
    if (P >= 1.0d-6) then
        write(10, *) 0, P
    end if

    do M = 1, N
        P = P * (N - M + 1.0d0) / (M * 1.0d0)
        if (P >= 1.0d-6) then
            write(10, *) M, P
        end if
    end do

    close(10)
    print *, 'Output written to ', filename
end program main