      module mod1
      implicit none
      integer, parameter :: GP = 6
      end module mod1

      module mod2
      implicit none
      integer, parameter :: SP = 5
      end module mod2

      module mod3
      use mod1
      implicit none
      integer, parameter :: DP = 0
      end module mod3

      module mod4
      use mod2
      implicit none
      end module mod4

      module mod5
      use mod3, lGP => GP
      use mod4
      implicit none
      end module mod5

      program driver
      use mod5
      implicit none

      print *, DP
      print *, SP
      print *, lGP

      end program driver
