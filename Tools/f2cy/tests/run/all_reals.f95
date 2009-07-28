
      subroutine real_default(r1,r2,r3)
          implicit none
          real, intent(in) :: r1
          real, intent(inout) :: r2
          real, intent(out) :: r3
          r3 = r3 + r1 - r1
          r2 = r2 + r3 - r3
      end subroutine
      subroutine real_x_len(r10,r11,r12,r13,r14,r15)
          implicit none
          real*4, intent(in) :: r10
          real*4, intent(inout) :: r11
          real*4, intent(out) :: r12
          real*8, intent(in) :: r13
          real*8, intent(inout) :: r14
          real*8, intent(out) :: r15
      end subroutine
      subroutine real_kind_x(r7,r8,r9,r10,r11,r12)
          implicit none
          real(kind=4), intent(in) :: r7
          real(kind=4), intent(inout) :: r8
          real(kind=4), intent(out) :: r9
          real(kind=8), intent(in) :: r10
          real(kind=8), intent(inout) :: r11
          real(kind=8), intent(out) :: r12
      end subroutine
      subroutine real_kind_call(r1,r2,r3,r4,r5,r6)
          implicit none
          real(kind=kind(0.0)), intent(in) :: r1
          real(kind=kind(0.0)), intent(inout) :: r2
          real(kind=kind(0.0)), intent(out) :: r3
          real(kind=kind(0.0D0)), intent(in) :: r4
          real(kind=kind(0.0D0)), intent(inout) :: r5
          real(kind=kind(0.0D0)), intent(out) :: r6
      end subroutine
      subroutine real_srk_call(r1,r2,r3,r4,r5,r6,r7,r8,r9)
          implicit none
          real(kind=selected_real_kind(1)), intent(in) :: r1
          real(kind=selected_real_kind(1)), intent(inout) :: r2
          real(kind=selected_real_kind(1)), intent(out) :: r3
          real(kind=selected_real_kind(7)), intent(in) :: r4
          real(kind=selected_real_kind(7)), intent(inout) :: r5
          real(kind=selected_real_kind(7)), intent(out) :: r6
          real(kind=selected_real_kind(14)), intent(in) :: r7
          real(kind=selected_real_kind(14)), intent(inout) :: r8
          real(kind=selected_real_kind(14)), intent(out) :: r9
      end subroutine
