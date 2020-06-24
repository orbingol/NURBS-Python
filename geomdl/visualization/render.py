"""
.. module:: render
    :platform: Unix, Windows
    :synopsis: Provides visualization options for NURBS-Python (geomdl)

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from ..tessellate import triangular, quadrilateral
from ..voxelate import voxelize

RENDER_OPTIONS = dict(
    cpcolor=['blue'],
    evalcolor=['green'],
    bboxcolor=['darkorange'],
    trimcolor=['black'],
    colormap=list(),
    filename=None,
    plot=True,
    extras=list(),
    animate=False,
)


def render(bsplg, vism, **kwargs):
    """ Renders B-spline geometries

    :param bsplg: B-spline geometry
    :param vism: visualization module
    """
    op = RENDER_OPTIONS
    op.update(kwargs)

    # Evaluate the geometry
    bsplg.evaluate()

    # Clear the visualization component
    vism.clear()

    ssz = len(bsplg)
    for si, s in enumerate(bsplg):
        # Add control points as points
        if vism.mconf['ctrlpts'] == 'points':
            vism.add(
                ptsarr=s.ctrlpts.points,
                name="control points" if ssz == 1 else  "control points {}".format(si + 1),
                color=op['cpcolor'][si],
                plot_type='ctrlpts'
            )

        # Add control points as quads
        if vism.mconf['ctrlpts'] == 'quads':
            v, f = quadrilateral.make_quad_mesh(s.ctrlpts.points, size_u=s.ctrlpts_size[0], size_v=s.ctrlpts_size[1])
            vism.add(
                ptsarr=[v, f],
                name="control points" if ssz == 1 else "control points {}".format(si + 1),
                color=op['cpcolor'][si],
                plot_type='ctrlpts'
            )

        # Add evaluated points as points
        if vism.mconf['evalpts'] == 'points':
            vism.add(
                ptsarr=s.evalpts,
                name=s.name if ssz == 1 else "geometry {}".format(si + 1),
                color=op['evalcolor'][si],
                plot_type='evalpts'
            )

        # Add evaluated points as quads
        if vism.mconf['evalpts'] == 'quads':
            v, f = quadrilateral.make_quad_mesh(s.evalpts, size_u=s.sample_size[0], size_v=s.sample_size[1])
            vism.add(
                ptsarr=[v, f],
                name=s.name if ssz == 1 else "geometry {}".format(si + 1),
                color=op['evalcolor'][si],
                plot_type='evalpts'
            )

        # Add evaluated points as vertices and triangles
        if vism.mconf['evalpts'] == 'triangles':
            v, f = triangular.make_triangle_mesh(s.evalpts, size_u=s.sample_size[0], size_v=s.sample_size[1])
            vism.add(
                ptsarr=[v, f],
                name=s.name if ssz == 1 else "geometry {}".format(si + 1),
                color=op['evalcolor'][si],
                plot_type='evalpts'
            )

        # Add evaluated points as voxels
        if vism.mconf['evalpts'] == 'voxels':
            grid, filled = voxelize.voxelize(s, **kwargs)
            faces = voxelize.convert_bb_to_faces(grid)
            vism.add(
                ptsarr=[grid, faces, filled],
                name=s.name if ssz == 1 else "geometry {}".format(si + 1),
                color=op['evalcolor'][si],
                plot_type='evalpts'
            )

        # Add trim curves
        if bsplg.trims:
            for idx, trim in enumerate(bsplg.trims):
                vism.add(
                    ptsarr=s.evaluate_list(trim.evalpts),
                    name="trim {}".format(idx + 1) if ssz == 1 else "trim {} for geometry {}".format(idx + 1, si + 1),
                    color=op['trimcolor'][si],
                    plot_type='trimcurve'
                )

        # Add bounding box
        vism.add(
            ptsarr=s.bbox,
            name="bounding box" if ssz == 1 else "bounding box {}".format(si + 1),
            color=op['bboxcolor'][si],
            plot_type='bbox'
        )

        # Add user plots
        for ep in op['extras']:
            vism.add(
                ptsarr=ep['points'],
                name=ep['name'],
                color=(ep['color'], ep['size']),
                plot_type='extras'
            )

        # Process data requested by the visualization module
        if vism.mconf['others']:
            for vo in vism.mconf['others'].split(","):
                vo_clean = vo.strip()
                # Send center point of the parametric space to the visualization module
                if vo_clean == "midpt":
                    vism.add(
                        ptsarr=[s.evaluate_single(*[r / 2.0 for r in s.range()])],
                        plot_type=vo_clean
                    )

    # Display the figure
    if op['animate']:
        return vism.animate(fig_save_as=op['filename'], display_plot=op['plot'], colormap=op['colormap'])
    return vism.render(fig_save_as=op['filename'], display_plot=op['plot'], colormap=op['colormap'])
