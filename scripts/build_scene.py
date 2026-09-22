"""Editable Blender 5.2 scene for Jaswanth's animated GitHub identity.

Run in Higgsfield 3D Jutsu. The artifacts registry is provided by the host.
"""
import bpy
import math
from mathutils import Vector

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.eevee.taa_render_samples = 16
scene.render.resolution_x = 640
scene.render.resolution_y = 640
scene.render.resolution_percentage = 100
scene.render.fps = 12
scene.frame_start = 1
scene.frame_end = 49  # Include the matching endpoint in the portable GLB loop.
scene.render.film_transparent = False
scene.world = bpy.data.worlds.new('Midnight ambient')
scene.world.use_nodes = True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value = (.035,.055,.09,1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value = .4
scene.view_settings.view_transform = 'Khronos PBR Neutral'

def material(name, color, metallic=0, roughness=.35, emission=0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color,1)
    m.use_nodes = True
    p = m.node_tree.nodes.get('Principled BSDF')
    p.inputs['Base Color'].default_value = (*color,1)
    p.inputs['Metallic'].default_value = metallic
    p.inputs['Roughness'].default_value = roughness
    p.inputs['Emission Color'].default_value = (*color,1)
    p.inputs['Emission Strength'].default_value = emission
    return m

navy = material('Graphite ceramic',(.027,.045,.072),.55,.28)
base = material('Midnight stage',(.010,.017,.029),.22,.42)
cyan = material('Ice cyan luminous trim',(.2,.78,1),.45,.22,.7)
violet = material('Lavender anodized metal',(.54,.32,.95),.6,.25,.25)
white = material('Porcelain typography',(.88,.95,1),.1,.32,.1)
muted = material('Blue grey typography',(.33,.47,.65),.2,.4)
lime = material('Lime signal',(.58,.9,.3),.2,.3,.5)

def empty(name, location=(0,0,0)):
    o=bpy.data.objects.new(name,None)
    scene.collection.objects.link(o)
    o.location=location
    return o

def cube(name, location, dimensions, mat, bevel=.06, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=location)
    o=bpy.context.object
    o.name=name
    o.dimensions=dimensions
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    o.data.materials.append(mat)
    mod=o.modifiers.new('Machined soft edges','BEVEL')
    mod.width=bevel
    mod.segments=4
    o.modifiers.new('Weighted surface normals','WEIGHTED_NORMAL')
    if parent:o.parent=parent
    return o

def ring(name,location,radius,thickness,mat,rotation=(0,0,0),parent=None):
    bpy.ops.mesh.primitive_torus_add(major_radius=radius,minor_radius=thickness,major_segments=96,minor_segments=12,location=location,rotation=rotation)
    o=bpy.context.object
    o.name=name
    o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
    if parent:o.parent=parent
    return o

def text(name,body,location,size,mat,rotation=(math.pi/2,0,0),parent=None):
    c=bpy.data.curves.new(name,'FONT')
    c.body=body
    c.align_x='CENTER'
    c.align_y='CENTER'
    c.size=size
    c.extrude=.003
    c.bevel_depth=.001
    o=bpy.data.objects.new(name,c)
    scene.collection.objects.link(o)
    o.location=location
    o.rotation_euler=rotation
    o.data.materials.append(mat)
    if parent:o.parent=parent
    return o

def animate_float(obj, amplitude, phase=0):
    z=obj.location.z
    for f in (1,13,25,37,49):
        obj.location.z=z+amplitude*math.sin(2*math.pi*(f-1)/48+phase)
        obj.keyframe_insert(data_path='location',index=2,frame=f)

cube('Infinite dark studio floor',(0,0,-.18),(200,200,.2),base,.02)
bpy.ops.mesh.primitive_cylinder_add(vertices=96,radius=1.76,depth=.2,location=(0,0,.02))
plinth=bpy.context.object
plinth.name='Floating core circular pedestal'
plinth.data.materials.append(navy)
bevel=plinth.modifiers.new('Pedestal bevel','BEVEL');bevel.width=.055;bevel.segments=4
plinth.modifiers.new('Pedestal smooth normals','WEIGHTED_NORMAL')
ring('Cyan pedestal rim',(0,0,.095),1.67,.012,cyan)
ring('Fine outer etching',(0,0,.123),1.50,.006,muted)

core=empty('SVJ floating identity assembly',(0,0,1.64))
cube('Core chamfered ceramic body',(0,0,0),(1.38,1.38,1.38),navy,.15,core)
cube('Front cyan reveal',(0,-.687,0),(1.12,.016,1.12),cyan,.09,core)
cube('Front recessed display',(0,-.704,0),(1.05,.03,1.05),base,.075,core)
text('SVJ engraved monogram','SVJ',(0,-.728,.095),.40,white,parent=core)
text('Core signature','BUILD / CONNECT',(0,-.73,-.21),.079,cyan,parent=core)
for i in range(3):
    cube('Signal bar '+str(i),(-.2+i*.2,-.73,-.36),(.115,.015,.018),cyan if i<2 else violet,.005,core)
animate_float(core,.09)
for f,angle in ((1,-8),(13,0),(25,8),(37,0),(49,-8)):
    core.rotation_euler.z=math.radians(angle)
    core.keyframe_insert(data_path='rotation_euler',index=2,frame=f)

orbit=empty('Orbital gimbal',(0,0,1.64))
ring('Cyan gimbal',(0,0,0),1.28,.016,cyan,(math.radians(64),math.radians(10),0),orbit)
ring('Lavender gimbal',(0,0,0),1.39,.014,violet,(math.radians(-57),math.radians(25),0),orbit)
for i,(angle,mat) in enumerate(((.3,cyan),(3.1,violet),(4.7,lime))):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,radius=.062,location=(1.4*math.cos(angle),1.4*math.sin(angle),.18))
    o=bpy.context.object;o.name='Orbit data node '+str(i);o.parent=orbit;o.data.materials.append(mat)
    for p in o.data.polygons:p.use_smooth=True
for f,angle in ((1,0),(49,2*math.pi)):
    orbit.rotation_euler.z=angle
    orbit.keyframe_insert(data_path='rotation_euler',index=2,frame=f)

# Floating modules are separate semantic components in the editable scene.
for index,(label,pos,mat) in enumerate((
    ('API',(-1.52,.0,2.25),cyan),
    ('AI',(1.25,.6,2.50),violet),
    ('UI',(1.35,-.60,.83),lime),
)):
    card=empty(label+' module',pos)
    cube(label+' module shell',(0,0,0),(.64,.14,.45),navy,.075,card)
    cube(label+' module accent',(-.25,-.079,0),(.025,.012,.23),mat,.01,card)
    text(label+' label',label,(.035,-.087,.012),.21,white,parent=card)
    animate_float(card,.065,index*math.pi*2/3)

def light(name,location,color,energy,size):
    data=bpy.data.lights.new(name,'POINT')
    data.energy=energy;data.color=color;data.shadow_soft_size=size
    o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=location
light('Key softbox',(1,-4,6),(0.77,.9,1),1600,3)
light('Lavender rim',(-3,2,4),(.55,.32,1),1300,2)
light('Cyan fill',(4,1,2),(.25,.75,1),950,2)
camera_data=bpy.data.cameras.new('Profile delivery camera')
camera=bpy.data.objects.new('Profile delivery camera',camera_data)
scene.collection.objects.link(camera)
camera.location=(3.6,-7.5,4.0)
camera.rotation_euler=(Vector((0,0,1.35))-camera.location).to_track_quat('-Z','Y').to_euler()
camera_data.type='ORTHO';camera_data.ortho_scale=4.7;camera_data.lens=50
scene.camera=camera

# Blender 5 layered actions: explicitly linear orbit rotation, eased floating.
for o in (core,orbit)+tuple(x for x in scene.objects if x.name.endswith(' module')):
    if not o.animation_data or not o.animation_data.action:continue
    action=o.animation_data.action
    for layer in action.layers:
        for strip in layer.strips:
            bag=strip.channelbag(o.animation_data.action_slot)
            if not bag:continue
            for fc in bag.fcurves:
                for k in fc.keyframe_points:
                    k.interpolation='LINEAR' if o==orbit else 'BEZIER'

scene.frame_set(1)
scene.render.image_settings.media_type='IMAGE'
scene.render.image_settings.file_format='PNG'
target=artifacts.file(name='jaswanth-3d-preview.png',media_type='image/png')
scene.render.filepath=target.path
bpy.ops.render.render(write_still=True)
target.publish()
result={'objects':len(scene.objects),'fps':12,'frames':[1,48],'loop_match_frame':49,'resolution':[640,640],'camera':camera.name}
