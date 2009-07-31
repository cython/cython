
      subroutine complex_default(r1,r2,r3)
          implicit none
          complex, intent(in) :: r1
          complex, intent(inout) :: r2
          complex, intent(out) :: r3
          r3 = r3 + r1 - r1
          r2 = r2 + r3 - r3
      end subroutine
      ! subroutine complex_x_len(r10,r11,r12,r13,r14,r15)
          ! implicit none
          ! complex*4, intent(in) :: r10
          ! complex*4, intent(inout) :: r11
          ! complex*4, intent(out) :: r12
          ! complex*8, intent(in) :: r13
          ! complex*8, intent(inout) :: r14
          ! complex*8, intent(out) :: r15
      ! end subroutine
      subroutine complex_kind_x(r7,r8,r9,r10,r11,r12)
          implicit none
          complex(kind=4), intent(in) :: r7
          complex(kind=4), intent(inout) :: r8
          complex(kind=4), intent(out) :: r9
          complex(kind=8), intent(in) :: r10
          complex(kind=8), intent(inout) :: r11
          complex(kind=8), intent(out) :: r12
      end subroutine
      subroutine complex_kind_call(r1,r2,r3,r4,r5,r6)
          implicit none
          complex(kind=kind((0.0,0.0))), intent(in) :: r1
          complex(kind=kind((0.0,0.0))), intent(inout) :: r2
          complex(kind=kind((0.0,0.0))), intent(out) :: r3
          complex(kind=kind((0.0D0,0.0D0))), intent(in) :: r4
          complex(kind=kind((0.0D0,0.0D0))), intent(inout) :: r5
          complex(kind=kind((0.0D0,0.0D0))), intent(out) :: r6
      end subroutine
      subroutine complex_srk_call(r1,r2,r3,r4,r5,r6,r7,r8,r9)
          implicit none
          complex(kind=selected_real_kind(1)), intent(in) :: r1
          complex(kind=selected_real_kind(1)), intent(inout) :: r2
          complex(kind=selected_real_kind(1)), intent(out) :: r3
          complex(kind=selected_real_kind(7)), intent(in) :: r4
          complex(kind=selected_real_kind(7)), intent(inout) :: r5
          complex(kind=selected_real_kind(7)), intent(out) :: r6
          complex(kind=selected_real_kind(14)), intent(in) :: r7
          complex(kind=selected_real_kind(14)), intent(inout) :: r8
          complex(kind=selected_real_kind(14)), intent(out) :: r9
      end subroutine
