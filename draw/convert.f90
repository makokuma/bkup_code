        program convert

        use iso_c_binding
        implicit none

        integer ::ix,jy,nx,ny,iix,jjy
        real(4), allocatable :: data(:,:),new_data(:,:)
        character(100) :: filepath_1,filepath_2
        character(40) :: filename_1,filename_2
        character(2) :: MM,DD,HH
        character(4) :: YYYY
        character(10) :: yyyymmdd
        integer :: ios
        integer :: cnt0, cnt999
        real(4),parameter :: eps = 1.0e-8
        real(4) :: min_val
        
        nx=2560
        ny=3360

        allocate(data(nx,ny), new_data(nx,ny))

        !read YYYY MM DD
        
        if (command_argument_count() /= 4) then
                print *, 'Usage: ./convert YYYY MM DD HH'
                stop
        endif

        call get_command_argument(1, YYYY)
        call get_command_argument(2, MM)
        call get_command_argument(3, DD)
        call get_command_argument(4, HH)


        filename_1 = YYYY//MM//DD//'_'//HH//'.bin'
!        write(6,*) filename_1

        filepath_1 = '/uhome/a01854/db_an.nus/dat/RA_data/'//YYYY//'/'&
                 &//MM//'/'//DD//'/'//filename_1

        filename_2 = 'RA01_nusdas_'//YYYY//MM//DD//HH//'00.dat'

        filepath_2 = '/uhome/a01854/db_an.nus/dat/convert/'//YYYY//'/'&
                 &//MM//'/'//DD//'/'//filename_2

        !open previous file
        open(unit=20,file=filepath_1,access='direct',form='unformatted'&
             &,recl=nx*ny*4, convert='little_endian', iostat=ios)

        if (ios /= 0) stop 'failed open ifile!'
        write(6,*) filename_1

        read(20,rec=1) data
        close(20)

        !imputation of missing values -999.0
        do jy = 1,ny
          do ix = 1,nx
          if (abs(data(ix,jy)) < eps)  then
                  data(ix,jy) = -999.0
          endif
          enddo
        enddo

        !upside down
        new_data(:,:) = data(:, ny:1:-1)

        ! check -999.0
        min_val = minval(new_data)
        write(*,*) 'min after conversion:', min_val

        !convert little_endian --> big_endian and save as new file
        open(unit=30,file=filepath_2,access='direct',form='unformatted'&
             &,recl=nx*ny*4, convert='big_endian', iostat=ios)

        if (ios /= 0) stop 'failed open ofile!'
        write(6,*) filename_2
        write(30,rec=1) new_data
        close(30) 

        end program convert
