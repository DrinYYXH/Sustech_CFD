Program main 
implicit none
! on wall implementation, center difference
! Euler time integration
!integer,parameter     :: N=90, Ntime=1024
!real*8,parameter      ::  dt = 0.002d0
!integer,parameter     :: N=40, Ntime=256
!real*8,parameter      ::  dt = 0.008d0
integer,parameter      :: N=20, Ntime=64
real*8,parameter       ::  dt = 0.032d0

real*8,parameter       :: u0=1.0d0, aL=1.0d0, anu=0.1
! u0 maximum velocity,aL channel half width,anu kinematic viscosity
! body force is then  g = 2*nu*u0/al^2
!real*8, dimension(1:N+1) :: uold, u, uana  [uana is not used, can be removed.]
real*8, dimension(1:N+1) :: uold, u
real*8                   ::theta0, theta1, theory1,ss,ycc,CFL
integer                  :: j,it,nsteps,k
real*8                   :: dy,pi,t,Tend

   pi = 4.0d0*atan(1.0d0)
   dy = 2.d0*aL/real(N)
! initial condition
   u = 0.0d0
   uold = u
   CFL = dt*anu/dy/dy

   write(*,*) 'anu, dt, aL, dy, CFL=', anu, dt, aL, dy, CFL
   t = 0.d0
   Tend = 3.0d0*aL*aL/anu
   nsteps = Tend / dt
   write(*,*) 'Tend, dt, Ntime, nsteps=', Tend, dt, Ntime, nsteps

   do it=1, nsteps
  
      do j=2,N
         u(j) = uold(j) + CFL*(uold(j-1)-2.d0*uold(j)+uold(j+1)) &
                + dt*2.d0*u0*anu/aL**2.d0
      end do

      do j=2,N
         uold(j) = u(j)
      enddo

      t = t +dt
! print out solutions
      if(mod(it,NTime).eq.0) then
! analytical solution with the same N
! assume N is even
         do j = 1,N+1
            ycc = real(j-1)*dy - 1.0d0
            theory1 = (1.d0- ycc**2.d0)
! I used 100 terms
            do k =0,100
            ss = (0.5d0+real(k))*pi
            theta0 = 4.0d0*(-1.0)**k/(pi*(real(k)+0.5d0))**3.d0
            theta1 =theta0 *exp(-ss*ss*anu*t)*cos(ss*ycc)
            theory1 = theory1 - theta1
            end do

         write(55,100)ycc,theory1,u(j)/u0,abs(u(j)-theory1)/theory1
         end do
!!!!!!!!!!
      end if

100     format(2x, 4f16.12)
   
   enddo
end program
