"""
.. module:: render
    :platform: Unix, Windows
    :synopsis: Provides visualization options for NURBS-Python (geomdl)

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from . import tessellate
from . import voxelize

RENDER_OPTIONS = dict(
    cpcolor='blue',
    evalcolor='green',
    bboxcolor='darkorange',
    trimcolor='black',
    colormap=None,
    filename=None,
    plot=True,
    extras=list(),
    animate=False,
    config_tsl_tri=None,
    config_tsl_quad=None
)


def render(spg, vism, **kwargs):
    op = RENDER_OPTIONS
    op.update(kwargs)

    # Evaluate the geometry
    spg.evaluate()

    # Clear the visualization component
    vism.clear()

    # Add control points as points
    if vism.mconf['ctrlpts'] == 'points':
        vism.add(
            ptsarr=spg.ctrlpts.points,
            name="control points",
            color=op['cpcolor'],
            plot_type='ctrlpts'
        )

    # Add control points as quads
    if vism.mconf['ctrlpts'] == 'quads':
        qtsl = op['config_tsl_quad'] if op['config_tsl_quad'] is not None else tessellate.QuadTessellate()
        qtsl.tessellate(spg.ctrlpts.points, size_u=spg.ctrlpts_size.u, size_v=spg.ctrlpts_size.v)
        vism.add(
            ptsarr=[qtsl.vertices, qtsl.faces],
            name="control points",
            color=op['cpcolor'],
            plot_type='ctrlpts'
        )

    # Add evaluated points as points
    if vism.mconf['evalpts'] == 'points':
        vism.add(
            ptsarr=spg.evalpts,
            name=spg.name,
            color=op['evalcolor'],
            plot_type='evalpts'
        )

    # Add evaluated points as quads
    if vism.mconf['evalpts'] == 'quads':
        qtsl = op['config_tsl_quad'] if op['config_tsl_quad'] is not None else tessellate.QuadTessellate()
        qtsl.tessellate(spg.evalpts, size_u=spg.sample_size[0], size_v=spg.sample_size[1])
        vism.add(
            ptsarr=[qtsl.vertices, qtsl.faces],
            name=spg.name,
            color=op['evalcolor'],
            plot_type='evalpts'
        )

    # Add evaluated points as vertices and triangles
    if vism.mconf['evalpts'] == 'triangles':
        tsl = op['config_tsl_tri'] if op['config_tsl_tri'] is not None else tessellate.TrimTessellate()
        tsl.tessellate(spg.evalpts, size_u=spg.sample_size[0], size_v=spg.sample_size[1])
        vism.add(
            ptsarr=[tsl.vertices, tsl.faces],
            name=spg.name,
            color=op['evalcolor'],
            plot_type='evalpts'
        )

    # Add evaluated points as voxels
    if vism.mconf['evalpts'] == 'voxels':
        grid, filled = voxelize.voxelize(spg, **kwargs)
        faces = voxelize.convert_bb_to_faces(grid)
        vism.add(
            ptsarr=[grid, faces, filled],
            name=spg.name,
            color=op['evalcolor'],
            plot_type='evalpts'
        )

    # Add trim curves
    if spg.trims:
        for idx, trim in enumerate(spg.trims):
            vism.add(
                ptsarr=spg.evaluate_list(trim.evalpts),
                name="Trim Curve " + str(idx + 1),
                color=op['trimcolor'],
                plot_type='trimcurve'
            )

    # Add bounding box
    vism.add(
        ptsarr=spg.bbox,
        name="Bounding Box",
        color=op['bboxcolor'],
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
                    ptsarr=[spg.evaluate_single(*[r / 2.0 for r in spg.range()])],
                    plot_type=vo_clean
                )

    # Display the figure
    if op['animate']:
        return vism.animate(fig_save_as=op['filename'], display_plot=op['plot'], colormap=op['colormap'])
    return vism.render(fig_save_as=op['filename'], display_plot=op['plot'], colormap=op['colormap'])
