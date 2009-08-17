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

      subroutine pass_array(arr0, arr1, arr2)
      implicit none
      integer, dimension(:,:), intent(in) :: arr0
      integer, dimension(:,:), intent(inout) :: arr1
      integer, dimension(:,:), intent(out) :: arr2

      print *, arr0
      print *, arr1

      arr2 = arr1 + arr0

      end subroutine pass_array

      subroutine pass_5D(arr0, arr1, arr2)
      implicit none
      integer :: i,j,k,l,m
      integer, dimension(:,:,:,:,:), intent(in) :: arr0
      integer, dimension(:,:,:,:,:), intent(inout) :: arr1
      integer, dimension(:,:,:,:,:), intent(out) :: arr2

      print *, shape(arr0)
      print *, shape(arr1)
      print *, shape(arr2)
      ! print *, arr0
      ! print *, arr1

      do i = 1, size(arr0,1)
          do j = 1, size(arr0,2)
              do k = 1, size(arr0,3)
                  do l = 1, size(arr0,4)
                      do m = 1, size(arr0,5)
                          print *, arr0(m,l,k,j,i)
                      enddo
                  enddo
              enddo
          enddo
      enddo

      arr2 = arr1 + arr0

      end subroutine pass_5D

      subroutine pass_3D(arr0, arr1, arr2)
      implicit none
      integer :: i,j,k,l,m
      integer, dimension(:,:,:), intent(in) :: arr0
      integer, dimension(:,:,:), intent(inout) :: arr1
      integer, dimension(:,:,:), intent(out) :: arr2

      print *, shape(arr0)
      print *, shape(arr1)
      print *, shape(arr2)
      ! print *, arr0
      ! print *, arr1

      do k = 1, size(arr0,1)
          do l = 1, size(arr0,2)
              do m = 1, size(arr0,3)
                  print *, arr0(m,l,k)
              enddo
          enddo
      enddo

      arr2 = arr1 + arr0

      end subroutine pass_3D

      subroutine pass_2D(arr0, arr1, arr2)
      implicit none
      integer :: i,j,k,l,m
      integer, dimension(:,:,:), intent(in) :: arr0
      integer, dimension(:,:,:), intent(inout) :: arr1
      integer, dimension(:,:,:), intent(out) :: arr2

      print *, shape(arr0)
      print *, shape(arr1)
      print *, shape(arr2)
      ! print *, arr0
      ! print *, arr1

      do l = 1, size(arr0,1)
          do m = 1, size(arr0,2)
              print *, arr0(m,l)
          enddo
      enddo

      arr2 = arr1 + arr0

      end subroutine pass_2D
