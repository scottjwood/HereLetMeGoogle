#BEGIN GPL LICENSE BLOCK

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software Foundation,
#Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

#END GPL LICENCE BLOCK

bl_info = {
    'name': "HereLetMeGoogle",
    'author': "scottwood",
    'version': (0, 6, ),
    'blender': (2, 9),
    'location': "View3D > Tools",
    'description': "Quick site specific google searches",
    'warning': "Still tinkering around, suggestions/bugs appreciate",
    'wiki_url': "",
    'tracker_url': "",
    'category': "Development"
    }


import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty

### Define Classes to register ###
classes = [
    HereLetMeProperties,
    HereLetMePanel,
    OBJECT_OT_hereletme
    ]


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.WindowManager.hereletme = bpy.props.PointerProperty(type=HereLetMeProperties)


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.WindowManager.hereletme

if __name__ == "__main__":
    register()