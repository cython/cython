subroutine wrapsubr_int_args_subr(a,b,c,d) bind(c,name="int_args_subr")
      use iso_c_binding
      implicit none
      integer(kind=c_signed_char), intent(in) :: a
      integer(kind=c_short), intent(in) :: b
      integer(kind=c_int), intent(in) :: c
      integer(kind=c_long), intent(out) :: d

      interface
        subroutine int_args_subr(a,b,c,d)
          integer(kind=1), intent(in) :: a
          integer(kind=2), intent(in) :: b
          integer(kind=4), intent(in) :: c
          integer(kind=8), intent(out) :: d
        end subroutine int_args_subr
      end interface

      call int_args_subr(a,b,c,d)
end subroutine wrapsubr_int_args_subr

function wrapfunc_int_args_func(a,b,c,d) bind(c,name="int_args_func")
      use iso_c_binding
      implicit none
      integer(kind=c_long) :: wrapfunc_int_args_func
      integer(kind=c_signed_char), intent(in) :: a
      integer(kind=c_short), intent(in) :: b
      integer(kind=c_int), intent(in) :: c
      integer(kind=c_long), intent(out) :: d

      interface
        function int_args_func(a,b,c,d)
          integer(kind=8) :: int_args_func
          integer(kind=1), intent(in) :: a
          integer(kind=2), intent(in) :: b
          integer(kind=4), intent(in) :: c
          integer(kind=8), intent(out) :: d
        end function int_args_func
      end interface

      wrapfunc_int_args_func = int_args_func(a,b,c,d)
end function wrapfunc_int_args_func

! module dummy
  ! use iso_c_binding
  ! use kind_type_params
  ! integer, parameter :: fortran_int_1 = c_signed_char

  ! contains

    ! subroutine int_args_subr_wrap(a,b,c,d) bind(c,name="int_args_subr")
    ! implicit none
    ! integer(kind=fortran_int_1), intent(in) :: a
    ! integer(kind=c_short), intent(in) :: b
    ! integer(kind=c_int), intent(in) :: c
    ! integer(kind=c_int64_t), intent(out) :: d
    ! ! integer(kind=c_long), intent(in) :: a
    ! ! integer(kind=c_long), intent(in) :: b
    ! ! integer(kind=c_long), intent(in) :: c
    ! ! integer(kind=c_long), intent(out) :: d

    ! ! integer(kind=1) :: convert_a
    ! ! integer(kind=2) :: convert_b
    ! ! integer(kind=4) :: convert_c
    ! ! integer(kind=8) :: convert_d

    ! interface
    ! subroutine int_args_subr(a,b,c,d)
    ! use kind_type_params
      ! integer(kind=1), intent(in) :: a
      ! integer(kind=2), intent(in) :: b
      ! integer(kind=4), intent(in) :: c
      ! integer(kind=sik10), intent(out) :: d
    ! end subroutine int_args_subr
    ! end interface

    ! print *, "before call in wrapper in fortran"
    ! print *, a,b,c,d

    ! ! convert_a = a
    ! ! convert_b = b
    ! ! convert_c = c
    ! ! convert_d = d

    ! print *, "before call in wrapper in fortran, converted vals."
    ! print *, convert_a, convert_b, convert_c, convert_d

    ! ! call int_args_subr(convert_a,convert_b,convert_c,convert_d)
    ! call int_args_subr(a,b,c,d)

    ! ! d = convert_d

    ! ! print *, "after call in wrapper in fortran, converted vals."
    ! ! print *, convert_a, convert_b, convert_c, convert_d

! end subroutine int_args_subr_wrap
! end module dummy
