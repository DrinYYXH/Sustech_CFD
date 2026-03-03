Program main
implicit none
real*4 y
integer i,j,m,n

! setting up the variables
y = 1.0
!n = 499
m = 600

do j=1,300
    n = j
    y = 1.0
    ! reduce n to the smaller of n and m-n
    if (n > m - n) n = m - n

    ! different formula for even and odd n
    if (mod(n,2) == 0) then
        y = 1.1
    else
        y = y * (m - n + 1)/REAL(n)
        n = n - 1
    end if

 !   if (y < 1e-6) then 
 !       y = 0
!    else
        y = y*(2.**-(m - 2*n))
!    end if
    write (2,*) j,n,y,log10(y)


    ! loop to calculate the probability
    do i=1,n/2
        y=y*(m + 1 - i)/4./(n  + 1 - i)
        y=y*(m - n + i)/REAL(i)/4.
        !write(1,*) i, y, log10(y)
    enddo

    ! final calculation of the probability
    write (1,*) j,n,y,log10(y)

enddo

end program main