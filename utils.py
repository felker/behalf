import numpy as np
from time import time
from datetime import datetime, timedelta


def compute_energy(pos, vel, mass, G=6.67e-11):
    """
    Returns the total energy of the system defined by
    input positions (pos), velocities (vel), and masses,
    using units defined by choice of G.

    Total energy is the sum of potential and kinetic energy
    (see: compute_potential_energy and compute_kinetic_energy)

    Input:
       pos - positions (N x d)
       vel - velocities (N x d)
       mass - masses (N)
       G - Newton's Constant (optional. Default=6.67e-11)

    Output:
       E - total energy (float)
    """
    return compute_potential_energy(pos, mass, G=G) +\
        compute_kinetic_energy(vel, mass)


def compute_potential_energy(pos, mass, G=6.67e-11):
    """
    Returns the gravitational potential energy of the system defined by input
    positions (pos) and masses, using units defined by choice of G.
    
    Potential energy is defined as:
    U = - sum_i ( sum_[j > i] ( G * mass[i] * mass[j] / r_ij))
    r_ij = || pos[i] - pos[j] ||

    Input:
       pos - positions (N x d)
       mass - masses (N)
       G - Newton's Constant (optional. Default=6.67e-11)

    Output:
       U - Gravitational potential energy (float)
    """
    pos = np.array(pos).astype(float)
    mass = np.array(mass).astype(float)
    N_part = pos.shape[0]
    assert mass.shape == (N_part,), ("input masses must match length of "
                                     "input positions")
    U = 0.
    for i in range(N_part):
        for j in range(i+1, N_part):
            r = np.sqrt(np.sum((pos[i] - pos[j])**2))
            U -= G * mass[i] * mass[j] / r
    return U


def compute_kinetic_energy(vel, mass):
    """
    Returns the kinetic of the system defined by input
    velocities and mass.
    
    Kinetic energy is defined as:
    K = 1/2 sum_i (mass[i] * ||vel[i]||**2)

    Input:
       vel - velocities (N x 3)
       mass - masses (N)

    Output:
       K - kinetic energy (float)
    """
    vel = np.array(vel).astype(float)
    mass = np.array(mass).astype(float)
    N_part = vel.shape[0]
    assert mass.shape == (N_part,), ("input masses must match length of "
                                     "input velocities")
    return np.sum(vel.T**2. * mass) * 0.5


def save_results(out_file, pos, vel, t_start, iter_num, iter_total, num_cores):
    """
    Saves the current state of the simulation to "out_file". 
    
    Input:
       out_file - filename to save results to
       pos - array of particle positions (N x d)
       vel - array of particle velocities (N x d)
       t_start - start time (in seconds) of the simulation
       iter_num - current time step of the simulation
       iter_total - total number of iterations the simulation will run for
       num_cores - number of cores used for computation
    """
    header = ""
    header += 'Num Particles: {:d}\n'.format(len(pos))
    header += 'Num Cores: {:d}\n'.format(num_cores)
    E_total = compute_energy(pos, vel, np.ones(len(pos)))
    header += 'Total Energy: {:.6e}\n'.format(E_total)
    header += 'Iterations: {:d} of {:d}\n'.format(iter_num, iter_total)
    header += 'Current Time: {:s}\n'.format(str(datetime.now()))
    dt = time()-t_start
    header += 'Elapsed Time: {:s}\n'.format(str(timedelta(seconds=dt)))
    ave_dt = dt / iter_num
    header += 'Avg. Step Time: {:s}\n'.format(str(timedelta(seconds=ave_dt)))
    header += '\n'
    header += 'x\ty\tz\tvx\tvy\tvz\n'
    np.savetxt(out_file, np.append(pos, vel, axis=-1), header=header,
               fmt='%+8.4f', delimiter='\t')


def split_size(N_parts, N_chunks, i):
    """
    Returns number of particles (out of N_parts) distributed to
    chunk i of N_chunks

    Input:
       N_parts - number of particles (int)
       N_chunks - number of chunks to distribute to (int)
       i - which chunk to compute number of particles (int, 0-indexed)

    Example: splitting 1000 particles across 10 chunks
    >>> split_size(1000, 11, 0)
    91
    >>> split_size(1000, 11, 10)
    90
    """
    return (N_parts // N_chunks) + int((N_parts % N_chunks) > i)
