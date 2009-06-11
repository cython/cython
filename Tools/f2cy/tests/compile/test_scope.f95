      module mod1
      implicit none
      integer, parameter :: GP = 6
      ! module_provides = {GP}
      ! use_provides = {}
      end module mod1

      module mod2
      implicit none
      integer, parameter :: SP = 5
      ! module_provides = {SP}
      ! use_provides = {}
      end module mod2

      module mod3
      use mod1
      implicit none
      integer, parameter :: DP = 0
      ! module_provides = {DP}
      ! use_provides = {GP}
      end module mod3

      module mod4
      use mod2
      implicit none
      ! module_provides = {}
      ! use_provides = {SP}
      end module mod4

      module mod5
      use mod3, lGP => GP
      use mod4
      implicit none

      integer, parameter :: FP = 1000
      integer(kind=kind(0)) :: dummy
      parameter (dummy = 20)

      ! module_provides = {FP, dummy}
      ! use_provides = {lGP, DP, SP}
      end module mod5

      program driver
      use mod5
      implicit none

      print *, DP
      print *, SP
      print *, lGP
      print *, FP

      end program driver
