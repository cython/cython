module foo
      implicit none
      integer*4 :: a
      real*4 :: b,c
      real*8 :: d
      integer*8 :: e
      double precision :: f
      character(kind=1,len=8) :: g
end module foo

subroutine bar(a,b,c,d,e,f,g)
    implicit none
    integer*4, intent(inout) :: a
    real*4, intent(inout) :: b,c
    real*8, intent(inout) :: d
    integer*8, intent(inout) :: e
    double precision, intent(inout) :: f
    character(kind=1,len=8), intent(inout) :: g

    ! print *, "kind(integer*4)", kind(a)
    ! print *, "kind(real*4)", kind(b)
    ! print *, "kind(real*4)", kind(c)
    ! print *, "kind(real*8)", kind(d)
    ! print *, "kind(integer*8)", kind(e)
    ! print *, "kind(double precision)", kind(f)
    ! print *, "kind(character(kind=1, len=8))", kind(g)

end subroutine bar

! program driver
    ! implicit none

    ! interface
    ! subroutine bar(a,b,c,d,e,f,g)
        ! implicit none
        ! integer*4, intent(inout) :: a
        ! real*4, intent(inout) :: b,c
        ! real*8, intent(inout) :: d
        ! integer*8, intent(inout) :: e
        ! double precision, intent(inout) :: f
        ! character(kind=1,len=8), intent(inout) :: g
    ! end subroutine bar
    ! end interface

        ! integer*4 :: a
        ! real*4 :: b,c
        ! real*8 :: d
        ! integer*8 :: e
        ! double precision :: f
        ! character(kind=1,len=8) :: g

        ! call bar(a,b,c,d,e,f,g)

! end program driver
