#!/usr/bin/env python3

from i3ipc.aio import Connection
from i3ipc import Event
from optparse import OptionParser

import asyncio


def get_comma_separated_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(","))


parser = OptionParser()
parser.add_option("-e", "--exclude-workspaces", dest="excludes", type="string", action="callback", callback=get_comma_separated_args,
                  metavar="ws1,ws2,.. ", help="List of workspaces that should be ignored.")
parser.add_option("-o", "--outputs", dest="outputs", type="string", action="callback", callback=get_comma_separated_args,
                  metavar="HDMI-0,DP-0,.. ", help="List of outputs that should be used instead of all.")
(options, args) = parser.parse_args()


skip_window_id = 0


async def grab_focused(c):
    tree = await c.get_tree()
    focused_window = tree.find_focused()

    if(options.excludes and focused_window.workspace().name in options.excludes):
        return None

    if(options.outputs and focused_window.ipc_data["output"] not in options.outputs):
        return None

    return focused_window


async def set_split(c, e):
    global skip_window_id
    focused_window = await grab_focused(c)
    if focused_window is None:
        return

    parent = focused_window.parent
    prev_window = parent.nodes[-1]

    if len(parent.nodes) == 1:
        skip_window_id = focused_window.id
    else:
        skip_window_id = 0

    if (parent.layout != "tabbed" and parent.layout != "stacked"):
        if (focused_window.rect.height > focused_window.rect.width):  
            await c.command("split vertical")
        
        if (focused_window.rect.height < focused_window.rect.width and len(parent.nodes)==1):  
            await c.command("split horizontal")
        # if prev_window.rect.height > prev_window.rect.width:
        #     await c.command("split vertical")
        # else:
        #     await c.command("split horizontal")


# To have the right split after moving when not changing focus.
# Workaround needed or windows get unable to be moved outside their parent container in certain cases.
async def move_workaround(c, e):
    global skip_window_id
    focused_window = await grab_focused(c)

    if focused_window is None:
        return

    if focused_window.id == skip_window_id:
        skip_window_id = 0
        return

    await set_split(c, e)

    focused_window = await grab_focused(c)
    if len(focused_window.parent.nodes) == 1:
        skip_window_id = focused_window.id
    else:
        skip_window_id = 0


async def main():
    # with auto_reconnect script would survive i3 exit aswell
    c = await Connection(auto_reconnect=False).connect()
    c.on(Event.WINDOW_FOCUS, set_split)
    c.on(Event.WINDOW_MOVE, move_workaround)
    await c.main()

asyncio.get_event_loop().run_until_complete(main())
