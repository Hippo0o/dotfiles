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

async def on_focus(c, e):
    focused_window = await grab_focused(c)
    if focused_window is None:
        return

    parent = focused_window.parent
    prev_window = parent.nodes[-1]

    if (parent.layout != "tabbed" and parent.layout != "stacked"):
        if parent.rect.height < parent.rect.width:
            await c.command("split horizontal")

async def on_new(c, e):
    focused_window = await grab_focused(c)
    if focused_window is None:
        return

    parent = focused_window.parent
    prev_window = parent.nodes[-1]

    if (parent.layout != "tabbed" and parent.layout != "stacked"):
        if parent.rect.height > parent.rect.width and len(parent.nodes) == 2:
            await c.command("[con_id=%s] layout splitv" % prev_window.id)



"""
To have the right split after moving when not changing focus.
Need a timeout or else windows get unable to be moved outside their parent container in certain cases.
"""
timeout = 0
async def on_move(c, e):
    global timeout
    timeout += 1
    await asyncio.sleep(0.5)
    timeout -= 1
    if timeout > 0:
        return
    await on_focus(c, e)


async def main():
    # with auto_reconnect script would survive i3 exit aswell
    c = await Connection(auto_reconnect=False).connect()
    c.on(Event.WINDOW_FOCUS, on_focus)
    c.on(Event.WINDOW_NEW, on_new)
    c.on(Event.WINDOW_MOVE, on_move)
    await c.main()

asyncio.get_event_loop().run_until_complete(main())
