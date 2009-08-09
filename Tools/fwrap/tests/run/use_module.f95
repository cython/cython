      module other
      implicit none

      integer, parameter :: other_int = selected_real_kind(14)
      public :: other_int
      end module other

      module used
      use other, used_int => other_int
      implicit none

      integer, parameter :: r8 = selected_real_kind(10,10)
      integer, parameter :: foo = 4

      end module used

      module sub1
      use used
      implicit none
      end module sub1

      module sub2
      use used
      implicit none
      end module sub2

      module diamond
      use sub1
      use sub2
      implicit none
      end module diamond

      ! function user(arg0)
      ! use diamond, r4 => foo
      ! implicit none
      ! ! real(kind=r8), intent(in) :: arg0
      ! ! real(kind=r4), intent(in) :: arg0
      ! real(kind=used_int), intent(in) :: arg0
      ! real(kind=r8) user

      ! user = arg0

      ! end function user

      module conflict
      use sub2
      implicit none

      integer, parameter :: r8 = 4

      ! contains 

      ! subroutine user(arg0)
      ! use sub2
      ! implicit none
      ! real(kind=r8), intent(inout) :: arg0

      ! arg0 = 10

      ! end subroutine

      end module




      ! program prog
      ! use diamond

      ! implicit none

      ! interface
      ! function user(arg)
      ! use diamond
      ! implicit none
      ! real(kind=r8), intent(in) :: arg
      ! real(kind=r8) user
      ! end function
      ! end interface

      ! print *, user(10.0_r8)

      ! end program
