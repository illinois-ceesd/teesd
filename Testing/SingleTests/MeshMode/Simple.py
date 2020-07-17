from __future__ import division

import numpy as np  # noqa

order = 4


def main():
    from meshmode.mesh.generation import (  # noqa
            make_curve_mesh, starfish)
    mesh1 = make_curve_mesh(starfish, np.linspace(0, 1, 20), 4)

    from meshmode.mesh.processing import affine_map, merge_disjoint_meshes
    mesh2 = affine_map(mesh1, b=np.array([2, 3]))

    mesh = merge_disjoint_meshes((mesh1, mesh2))

    from meshmode.mesh.visualization import draw_2d_mesh
    draw_2d_mesh(mesh, set_bounding_box=True)

    import os
    import teesd
    randfilekey = teesd.getrandkey(teesd.localrev)
    fname = os.getcwd() + '/meshmode_simple_' + randfilekey + '.png'

    import matplotlib.pyplot as pt
    # pt.show()
    pt.savefig(fname)

    import sys
    if os.path.exists(fname) is False:
        sys.exit(1)

    import abate
    abate.output_dart_measurement_file(fname)


if __name__ == "__main__":
    main()
