! consult https://en.wikipedia.org/wiki/Single-precision_floating-point_format
!
program main_range
real*4 input
integer::binput
20 read(*,*)input
write(*,*)'output = ',input
binput = transfer(input,binput)
write(*,fmt="(b32.32)")binput
go to 20
end program main_range
