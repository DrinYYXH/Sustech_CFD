Program main 
implicit none 
real*4 y
integer i
y=1.0
do i=1,500
y=y*(1001-i)/4.0/(501-i)
write(10,*) i, y, alog10(y)
enddo

write (*,*) y

end program

