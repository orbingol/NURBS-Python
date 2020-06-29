"""
.. module:: render
    :platform: Unix, Windows
    :synopsis: Provides visualization options for NURBS-Python (geomdl)

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from ..base import GeomdlError
from ..tessellate import triangular, quadrilateral
from ..voxelate import voxelize
from .visutils import color_generator


def render(bsplg, vism, **kwargs):
    """ Renders B-spline geometries

    :param bsplg: B-spline geometry
    :type bsplg: abstract.SplineGeometry
    :param vism: visualization module
    :type vism: visabstract.VisAbstract
    :raises GeomdlError: invalid user input
    """
    # Get number of geometries
    ssz = len(bsplg)

    # Update configuration
    op = dict(
        cpcolor=['blue'] if ssz == 1 else color_generator(num=ssz),
        evalcolor=['green'] if ssz == 1 else color_generator(num=ssz),
        bboxcolor=['darkorange'] if ssz == 1 else color_generator(num=ssz),
        trimcolor=['black'],
        colormap=list(),
        filename=None,
        display=True,
        extras=list(),
        animate=False,
    )
    op.update(kwargs)

    # Validate user input
    if len(op['cpcolor']) != ssz:
        raise GeomdlError("Number of color values for the control points must be " + str(ssz))
    if len(op['evalcolor']) != ssz:
        raise GeomdlError("Number of color values for the evaluated points must be " + str(ssz))
    if len(op['bboxcolor']) != ssz:
        raise GeomdlError("Number of color values for the boundary box must be " + str(ssz))

    # Clear the visualization component
    vism.clear()

    # Start geometry loop
    for si, s in enumerate(bsplg):
        # Add control points as points
        if vism.mconf['ctrlpts'] == 'points' and vism.vconf.display_ctrlpts:
            vism.add(
                ptsarr=s.ctrlpts.points,
                name="control points" if ssz == 1 else  "control points {}".format(si + 1),
                color=op['cpcolor'][si],
                plot_type='ctrlpts'
            )

        # Add control points as quads
        if vism.mconf['ctrlpts'] == 'quads' and vism.vconf.display_ctrlpts:
            v, f = quadrilateral.make_quad_mesh(s.ctrlpts.points, size_u=s.ctrlpts_size[0], size_v=s.ctrlpts_size[1])
            vism.add(
                ptsarr=[v, f],
                name="control points" if ssz == 1 else "control points {}".format(si + 1),
                color=op['cpcolor'][si],
                plot_type='ctrlpts'
            )

        # Add evaluated points as points
        if vism.mconf['evalpts'] == 'points' and vism.vconf.display_evalpts:
            vism.add(
                ptsarr=s.evalpts,
                name=s.name if ssz == 1 else "geometry {}".format(si + 1),
                color=op['evalcolor'][si],
                plot_type='evalpts'
            )

        # Add evaluated points as quads
        if vism.mconf['evalpts'] == 'quads' and vism.vconf.display_evalpts:
            v, f = quadrilateral.make_quad_mesh(s.evalpts, size_u=s.sample_size[0], size_v=s.sample_size[1])
            vism.add(
                ptsarr=[v, f],
                name=s.name if ssz == 1 else "geometry {}".format(si + 1),
                color=op['evalcolor'][si],
                plot_type='evalpts'
            )

        # Add evaluated points as vertices and triangles
        if vism.mconf['evalpts'] == 'triangles' and vism.vconf.display_evalpts:
            v, f = triangular.make_triangle_mesh(s.evalpts, size_u=s.sample_size[0], size_v=s.sample_size[1])
            vism.add(
                ptsarr=[v, f],
                name=s.name if ssz == 1 else "geometry {}".format(si + 1),
                color=op['evalcolor'][si],
                plot_type='evalpts'
            )

        # Add evaluated points as voxels
        if vism.mconf['evalpts'] == 'voxels' and vism.vconf.display_evalpts:
            grid, filled = voxelize.voxelize(s, **kwargs)
            faces = voxelize.convert_bb_to_faces(grid)
            vism.add(
                ptsarr=[grid, faces, filled],
                name=s.name if ssz == 1 else "geometry {}".format(si + 1),
                color=op['evalcolor'][si],
                plot_type='evalpts'
            )

        # Add trim curves
        if s.trims and vism.vconf.display_trims:
            for idx, trim in enumerate(s.trims):
                vism.add(
                    ptsarr=s.evaluate_list(trim.evalpts),
                    name="trim {}".format(idx + 1) if ssz == 1 else "trim {} for geometry {}".format(idx + 1, si + 1),
                    color=op['trimcolor'][si],
                    plot_type='trimcurve'
                )

        # Add bounding box
        if vism.vconf.display_bbox:
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
        return vism.animate(fig_save_as=op['filename'], display_plot=op['display'], colormap=op['colormap'])
    return vism.render(fig_save_as=op['filename'], display_plot=op['display'], colormap=op['colormap'])
