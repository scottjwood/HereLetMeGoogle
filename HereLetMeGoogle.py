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

class HereLetMeProperties(bpy.types.PropertyGroup):
    engines = [
        ('google.com', 'Google', "0"),
        ('blenderartists.org', 'BlenderArtists', "1"),
        ('blender.org/documentation/blender_python_api_2_69_1', 'Blender.org API', "2"),
        ('blendercookie.com', 'BlenderCookie', "3"),
        ('blenderguru.com', 'BlenderGuru', "4"),
        ('graphicall.com', 'GraphicAll', "5"),
        ('pasteall.org', 'PasteAll', "6"),
        ('stackoverflow.com', 'StackOverflow', "7"),
        ('svn.blender.org/svnroot/bf-extensions', 'SVN extensions', '8'),
        ('sourceforge.net/projects/blenderpython', 'Sourceforge blender', '9'),
        ('blender.stackexchange.com/', 'Blender Stackexchange', '10'),
        ('customURL', 'Custom', "11")
        ]

    engine = bpy.props.EnumProperty(name="Search Site", description="What site to search", default="blenderartists.org", items=engines)
    settings = bpy.props.BoolProperty(name="Settings", description="Boolean", default=False)
    custom = bpy.props.BoolProperty(name="custom", description="Boolean", default=False)
    search_string = bpy.props.StringProperty(name="Search String", description="Type your search")
    custom_string = bpy.props.StringProperty(name="Custom Web Search", description="Type your custom website")
    term_python = bpy.props.BoolProperty(name="Python", description="Add Python to search", default=False)
    term_26 = bpy.props.BoolProperty(name="2.6", description="Add 2.6 to search", default=False)
    term_game = bpy.props.BoolProperty(name="Game Engine", description="Add Game Engine to search", default=False)
    term_modeling = bpy.props.BoolProperty(name="Modeling", description="Add Modeling to search", default=False)
    term_script = bpy.props.BoolProperty(name="Script", description="Add Script to search", default=False)
    term_cycles = bpy.props.BoolProperty(name="Cycles", description="Add Cycles to search", default=False)
    term_rigging = bpy.props.BoolProperty(name="Rigging", description="Add Rigging to search", default=False)
    term_rendering = bpy.props.BoolProperty(name="Rendering", description="Add Rendering to search", default=False)
    term_osl = bpy.props.BoolProperty(name="OSL", description="Add OSL to search", default=False)


class HereLetMePanel(bpy.types.Panel):
    bl_label = "Here Let Me Google"
    bl_idname = "OBJECT_PT_hereletme"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        search_props = bpy.context.window_manager.hereletme
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(search_props, "search_string", text="")
        row = col.row()
        row = col.row()
        row.prop(search_props, "settings")
        row.operator("wm.hereletme", text='Search', icon='VIEWZOOM')
        if search_props.settings:
            if search_props.engine == 'customURL':
                mysearch = search_props.custom_string
            else:
                current = search_props.engine
                for i in search_props.engines:
                    if i[0] == current:
                        mycontainer = i
                        mysearch = i[0]  # find the second element, aka 1

            col = layout.column()
            col.label("Search Site")
            col.prop(search_props, "engine", text="")
            if search_props.engine == 'customURL':
                col.label("Enter Custom URL")
                col.prop(search_props, "custom_string", text="")
            row = layout.row(align=True)
            row.label(text="Additional Search Terms")
            row = layout.row(align=True)
            row.prop(search_props, "term_python")
            row.prop(search_props, "term_26")
            row = layout.row(align=True)
            row.prop(search_props, "term_game")
            row.prop(search_props, "term_modeling")
            row = layout.row(align=True)
            row.prop(search_props, "term_script")
            row.prop(search_props, "term_rigging")
            row = layout.row(align=True)
            row.prop(search_props, "term_cycles")
            row.prop(search_props, "term_rendering")
            row = layout.row(align=True)
            row.prop(search_props, "term_osl")


################## ################## ################## ############
## Search Helper Operator
## searches website via google
################## ################## ################## ############

class OBJECT_OT_hereletme(bpy.types.Operator):
    bl_idname = "wm.hereletme"
    bl_label = "HereLetMeGoogle"
    bl_description = "Search a website using a StringProperty"

    def invoke(self, context, event):
        search_props = bpy.context.window_manager.hereletme  # Get duplicate check setting
        # Search Terms
        myterms = ""
        if search_props.term_python:
            myterms += "Python+"
        if search_props.term_26:
            myterms += "2.6+"
        if search_props.term_game:
            myterms += "Game+Engine+"
        if search_props.term_modeling:
            myterms += "Modeling+"
        if search_props.term_script:
            myterms += "Script+"
        if search_props.term_rigging:
            myterms += "Rigging+"
        if search_props.term_cycles:
            myterms += "cycles+"
        if search_props.term_rendering:
            myterms += "Rendering+"
        if search_props.term_osl:
            myterms += "OSL+"

        # Search engines
        searchengine = 'https://www.google.com/search?&q=site%3A'
        searchsite = search_props.engine
        terms = myterms.replace(" ", "+")
        search = search_props.search_string.replace(" ", "+")
        if search_props.engine == 'google.com':
            searchurl = 'https://www.google.com/search?&q=' + "+" + myterms + search
        else:
            searchurl = 'https://www.google.com/search?&q=site%3A' + searchsite + "+" + myterms + search

        bpy.ops.wm.url_open(url=searchurl)
        return{"FINISHED"}

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
