      ! subroutine pass_array(arr0, arr1, arr2, arr3)
      ! implicit none
      ! integer, dimension(0:10), intent(inout) :: arr0
      ! integer, dimension(1:10+1-1), intent(inout) :: &
      ! arr1(-1+1:10-3, -100+100:-100+110)
      ! integer, dimension(:,:), intent(inout) :: arr2(-2:,-1:,0:)
      ! integer, dimension(size(arr0,1)) :: arr3

      ! arr0 = 5
      ! arr1 = 10

      ! end subroutine pass_array

      subroutine pass_array(arr0)
      implicit none
      integer, dimension(:,:), intent(inout) :: arr0

      arr0 = 5

      end subroutine pass_array
