
function int_args_func(a,b,c,d)
      integer(kind=8) :: int_args_func
      integer(kind=1), intent(in) :: a
      integer(kind=2), intent(in) :: b
      integer(kind=4), intent(in) :: c
      integer(kind=8), intent(out) :: d

      d = a + b + c
      int_args_func = 10

end function int_args_func

subroutine int_args_subr(a,b,c,d)
      integer(kind=1), intent(in) :: a
      integer(kind=2), intent(in) :: b
      integer(kind=4), intent(in) :: c
      integer(kind=8), intent(out) :: d

      d = a + b + c

end subroutine int_args_subr

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

! program blargh
! use dummy
      ! integer(kind=1) :: a
      ! integer(kind=2) :: b
      ! integer(kind=4) :: c
      ! integer(kind=8) :: d
      ! ! integer(kind=8) :: a
      ! ! integer(kind=8) :: b
      ! ! integer(kind=8) :: c
      ! ! integer(kind=8) :: d
      ! a = 1; b = 2; c = 3; d = 4
! call int_args_subr_wrap(a,b,c,d)
    ! print *, a,b,c,d
! end program blargh

 ! ====================
 ! integer types
 ! --------------------

 ! c_int                      4
 ! c_short                    2
 ! c_long                     8
 ! c_long_long                8
 ! c_signed_char              1
 ! c_size_t                   8
 ! c_int8_t                   1
 ! c_int16_t                  2
 ! c_int32_t                  4
 ! c_int64_t                  8
 ! c_int_least8_t             1
 ! c_int_least16_t            2
 ! c_int_least32_t            4
 ! c_int_least64_t            8
 ! c_int_fast8_t             -2
 ! c_int_fast16_t            -2
 ! c_int_fast32_t            -2
 ! c_int_fast64_t            -2
 ! c_intmax_t                 8
 ! c_intptr_t                 8

 ! ====================
 ! real types
 ! --------------------

 ! c_float                   4
 ! c_double                  8
 ! c_long_double            10

 ! ====================
 ! complex types
 ! --------------------

 ! c_float_complex                  4
 ! c_double_complex                 8
 ! c_long_double_complex           10

 ! ====================
 ! logical types
 ! --------------------

 ! c_bool              1

 ! ====================
 ! character types
 ! --------------------

 ! c_char              1

! module kind_type_params
! implicit none
! integer, parameter :: sik10 = selected_int_kind(10)

! end module kind_type_params
