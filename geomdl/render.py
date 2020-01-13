"""
.. module:: render
    :platform: Unix, Windows
    :synopsis: Provides basic rendering capability

.. moduleauthor:: Onur R. Bingol <contact@onurbingol.net>

"""

from .base import GeomdlDict
from . import tessellate
from . import voxelize

RENDER_OPTIONS = GeomdlDict(
    cpcolor='blue',
    evalcolor='black',
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


def render(spg, **kwargs):
    op = RENDER_OPTIONS
    op.update(kwargs)

    # Evaluate the geometry
    spg.evaluate()

    # Clear the visualization component
    spg.vis.clear()

    # Add control points as points
    if spg.vis.mconf['ctrlpts'] == 'points':
        spg.vis.add(
            ptsarr=spg.ctrlpts.data,
            name="control points",
            color=op['cpcolor'],
            plot_type='ctrlpts'
        )

    # Add control points as quads
    if spg.vis.mconf['ctrlpts'] == 'quads':
        qtsl = op['config_tsl_quad'] if op['config_tsl_quad'] else tessellate.QuadTessellate()
        qtsl.tessellate(spg.ctrlpts.data, size_u=spg.ctrlpts_size.u, size_v=spg.ctrlpts_size.v)
        spg.vis.add(
            ptsarr=[qtsl.vertices, qtsl.faces],
            name="control points",
            color=op['cpcolor'],
            plot_type='ctrlpts'
        )

    # Add evaluated points as points
    if spg.vis.mconf['evalpts'] == 'points':
        spg.vis.add(
            ptsarr=spg.evalpts,
            name=spg.name,
            color=op['evalcolor'],
            plot_type='evalpts'
        )

    # Add evaluated points as quads
    if spg.vis.mconf['evalpts'] == 'quads':
        qtsl = op['config_tsl_quad'] if op['config_tsl_quad'] else tessellate.QuadTessellate()
        qtsl.tessellate(spg.evalpts, size_u=spg.sample_size.u, size_v=spg.sample_size.v)
        spg.vis.add(
            ptsarr=[qtsl.vertices, qtsl.faces],
            name=spg.name,
            color=op['evalcolor'],
            plot_type='evalpts'
        )

    # Add evaluated points as vertices and triangles
    if spg.vis.mconf['evalpts'] == 'triangles':
        tsl = op['config_tsl_tri'] if op['config_tsl_tri'] else tessellate.TrimTessellate()
        spg.vis.add(
            ptsarr=[tsl.vertices, tsl.faces],
            name=spg.name,
            color=op['evalcolor'],
            plot_type='evalpts'
        )

    # Add evaluated points as voxels
    if spg.vis.mconf['evalpts'] == 'voxels':
        grid, filled = voxelize.voxelize(spg, **kwargs)
        faces = voxelize.convert_bb_to_faces(grid)
        spg.vis.add(
            ptsarr=[grid, faces, filled],
            name=spg.name,
            color=op['evalcolor'],
            plot_type='evalpts'
        )

    # Add trim curves
    if spg.trims:
        for idx, trim in enumerate(spg.trims):
            spg.vis.add(
                ptsarr=spg.evaluate_list(trim.evalpts),
                name="Trim Curve " + str(idx + 1),
                color=op['trimcolor'],
                plot_type='trimcurve'
            )

    # Add bounding box
    spg.vis.add(
        ptsarr=spg.bbox,
        name="Bounding Box",
        color=op['bboxcolor'],
        plot_type='bbox'
    )

    # Add user plots
    for ep in op['extras']:
        spg.vis.add(
            ptsarr=ep['points'],
            name=ep['name'],
            color=(ep['color'], ep['size']),
            plot_type='extras'
        )

    # Process data requested by the visualization module
    if spg.vis.mconf['others']:
        for vo in spg.vis.mconf['others'].split(","):
            vo_clean = vo.strip()
            # Send center point of the parametric space to the visualization module
            if vo_clean == "midpt":
                spg.vis.add(
                    ptsarr=[spg.evaluate_single(*[r / 2.0 for r in spg.range()])],
                    plot_type=vo_clean
                )

    # Display the figure
    if op['animate']:
        return spg.vis.animate(fig_save_as=op['filename'], display_plot=op['plot'], colormap=op['colormap'])
    return spg.vis.render(fig_save_as=op['filename'], display_plot=op['plot'], colormap=op['colormap'])
