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

async def grab_focused(c):
    tree = await c.get_tree()
    focused_window = tree.find_focused()

    if(options.excludes and focused_window.workspace().name in options.excludes):
        return None

    if(options.outputs and focused_window.ipc_data["output"] not in options.outputs):
        return None
    
    return focused_window

last_window_id = 0
async def set_split(c, e):
    global last_window_id
    focused_window = await grab_focused(c)
    if focused_window is None:
        return

    #on WINDOW_MOVE windows would otherwise get unable to be moved outside their parent container in certain cases.
    if(last_window_id == focused_window.id):
        return
    last_window_id = focused_window.id

    parent = focused_window.parent
    prev_window = parent.nodes[-1]
    if (parent.layout != "tabbed" and parent.layout != "stacked"):
        if (focused_window.rect.height > focused_window.rect.width and
                parent.layout == "splith" and 
                parent.num is not None): #workspace container only
            await c.command("split vertical")
        # if prev_window.rect.height > prev_window.rect.width:
        #     await c.command("split vertical")
        # else:
        #     await c.command("split horizontal")

async def main():
    # with auto_reconnect script would survive i3 exit aswell
    c = await Connection(auto_reconnect=False).connect()
    c.on(Event.WINDOW_FOCUS, set_split)
    c.on(Event.WINDOW_MOVE, set_split)
    await c.main()

asyncio.get_event_loop().run_until_complete(main())
