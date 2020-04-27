def twiss_product(n, A, B0, twiss_array):
    for pos in range(n):
        m = A[pos]
        twiss_array[0,pos] = m[0,0] * m[0,0] * B0[0] - 2. * m[0,0] * m[0,1] * B0[2] + m[0,1] * m[0,1] * B0[4]
        twiss_array[2,pos] = -m[0,0] * m[1,0] * B0[0] + (m[0,0] * m[1,1] + m[0,1] * m[1,0]) * B0[2] - m[1,1] * \
                              m[0,1] * B0[4]
        twiss_array[4,pos] = m[1,0] * m[1,0] * B0[0] - 2. * m[1,1] * m[1,0] * B0[2] + m[1,1] * m[1,1] * B0[4]

        twiss_array[1,pos] = m[2,2] * m[2,2] * B0[1] - 2. * m[2,2] * m[2,3] * B0[3] + m[2,3] * m[2,3] * B0[5]
        twiss_array[3,pos] = -m[2,2] * m[3,2] * B0[1] + (m[2,2] * m[3,3] + m[2,3] * m[3,2]) * B0[3] - m[3,3] * \
                              m[2,3] * B0[5]
        twiss_array[5,pos] = m[3,2] * m[3,2] * B0[1] - 2. * m[3,3] * m[3,2] * B0[3] + m[3,3] * m[3,3] * B0[5]
#        twiss_array[6,pos] = m[0,0] * B0[6] + m[0,1] * B0[7] + m[0,4]
#        twiss_array[7,pos] = m[1,0] * B0[6] + m[1,1] * B0[7] + m[1,4]
