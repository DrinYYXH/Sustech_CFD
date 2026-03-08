Program main
implicit none
real*4 y
integer i,m,n

! setting up the variables
m = 600


do n=1,300
    y = - m * log(2.0)
    do i=1,n
        y = y + log(REAL(m - n + i)) - log(REAL(n + 1 - i))
    enddo
    if (y + 6 * log(10.0) < 0) then
        y = 0
    else
        y = exp(y)
    endif
    
    write(1,*) n,y,log(y)
enddo

end program main