Program main
implicit none
real*4 y
integer i,m,n

! setting up the variables
y = 1.0
n = 459
m = 1000

! reduce n to the smaller of n and m-n
if (n > m - n) n = m - n

! different formula for even and odd n
if (mod(n,2) == 0) then
    y = 1.0
else
    y = y * (m - n + 1)/REAL(n)/2.
    n = n - 1
end if

! loop to calculate the probability
do i=1,n/2
    y=y*(m + 1 - i)/4./(n  + 1 - i)
    y=y*(m - n + i)/REAL(i)/4.
    write(1,*) i, y, log10(y)
enddo

! final calculation of the probability
y = y*(2.**-(m - 2*n))
write (*,*) y

end program main