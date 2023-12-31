# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess

from libqtile import bar, hook, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from qtilecolors import colors, wallpaper

config = os.path.expanduser("~/.config/qtile")


@hook.subscribe.startup_once
def start_once():
    autostart = os.path.join(config, "autostart.sh")
    subprocess.Popen([autostart])


@hook.subscribe.shutdown
def shutdown():
    subprocess.run(["killall", "Xorg"])


@lazy.function
def next_wallpaper(qtile):
    theme = os.path.join(config, "theme.sh")
    subprocess.run([theme, "-n"])
    qtile.reload_config()


mod = "mod4"
terminal = guess_terminal()

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key(
        [mod, "control"],
        "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink_main(),
        desc="Grow window to the left",
    ),
    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        lazy.layout.grow_main(),
        desc="Grow window to the right",
    ),
    Key(
        [mod, "control"],
        "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        desc="Grow window down",
    ),
    Key(
        [mod, "control"],
        "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        desc="Grow window up",
    ),
    Key([mod, "control"], "f", lazy.layout.flip(), desc="Flip panels"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    Key([mod], "m", lazy.window.toggle_minimize(), desc="Toggle minimize"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    # Toggle keyboard layout
    Key(
        ["mod1"],
        "Shift_L",
        lazy.widget["keyboardlayout"].next_keyboard(),
        desc="Next keyboard layout",
    ),
    # Pulse Audio controls
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"),
    ),
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"),
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"),
    ),
    # Next theme
    Key([mod, "control"], "n", next_wallpaper(), desc="Sets the next theme"),
    Key(
        [mod, "shift"],
        "s",
        lazy.spawn("maim -s | xclip -selection clipboard -t image/png", shell=True),
        desc="Screenshot of the screen area",
    ),
    Key(
        [],
        "Print",
        lazy.spawn("maim | xclip -selection clipboard -t image/png", shell=True),
        desc="Screenshot",
    ),
]

# groups = [Group(i) for i in "123456789"]
groups = [
    Group("1", label=""),
    Group("2", label="󰈹", spawn="firefox", matches=[Match(wm_class=["firefox"])]),
    Group("3", label="󰓓", spawn="steam", matches=[Match(wm_class=["steam"])]),
    Group("4", label=""),
    Group("5", label="󰙯", spawn="discord", matches=[Match(wm_class=["discord"])]),
    Group("6", label="", matches=[Match(wm_class=["mpv", "ffplay"])]),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {
    "margin": 10,
    "border_on_single": False,
    "border_width": 4,
    "border_normal": colors["Inactive"],
    "border_focus": colors["Active"],
}

layouts = [
    # layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(border_width=0, margin=10),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(
    #   **layout_theme
    # ),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(
    #   **layout_theme
    # ),
    # layout.RatioTil
    #   **layout_theme
    # ),
    # layout.Tile(
    #   **layout_theme
    # ),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font="Noto Nerd Font", fontsize=16, padding=10, foreground=colors["Foreground"]
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(
                    length=10,
                ),
                widget.CurrentLayoutIcon(
                    scale=0.5,
                    # foreground=colors["Blue"][0] #blue
                ),
                widget.CPU(format="  {freq_current}GHz {load_percent}%"),
                widget.Memory(
                    measure_mem="G",
                    format="  {MemUsed:.1f} GiB",
                    # foreground=colors["green"][0]
                ),
                widget.Net(
                    format="{down:.0f}{down_suffix:<2} ↓↑ {up:.0f}{up_suffix:<2}",
                    # foreground=colors["Green"][0]
                ),
                widget.Prompt(),
                widget.Spacer(),
                widget.GroupBox(
                    highlight_method="text",
                    this_current_screen_border=colors["Foreground"],
                    # block_highlight_text_color=colors["Background"] + "d0",
                    active=colors["Active"],
                    inactive=colors["Inactive"],
                    urgent_alert_method="text",
                    urgent_text=colors["Magenta"],
                    # hide_unused=True
                ),
                widget.Spacer(),
                # widget.Chord(
                #     chords_colors={
                #         "launch": ("#ff0000", "#ffffff"),
                #     },
                #     name_transform=lambda name: name.upper(),
                # ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.Mpris2(
                #     format="{xesam:title}",
                #     max_chars=50,
                #     no_metadata_text="-",
                #     playing_text="󰐊 {track}",
                #     paused_text="  {track}",
                #     poll_interval=1,
                # ),
                widget.Volume(
                    fmt="󰕾  {}",
                    volume_app="pactl",
                    get_volume_command="pactl get-sink-volume @DEFAULT_SINK@",
                    volume_down_command="pactl set-sink-volume @DEFAULT_SINK@ -1%",
                    volume_up_command="pactl set-sink-volume @DEFAULT_SINK@ +1%",
                    check_mute_command="pactl get-sink-mute @DEFAULT_SINK@",
                    check_mute_string="yes",
                    mute_command="pactl set-sink-mute @DEFAULT_SINK@ 'toggle'",
                ),
                widget.KeyboardLayout(
                    configured_keyboards=["us", "ru,us"],
                ),
                widget.Clock(
                    format="  %-d %B, %R",
                    mouse_callbacks={"Button1": lazy.spawn("kitty -e calcurse")},
                ),
                # widget.StatusNotifier(),
                widget.Systray(),
                widget.Spacer(
                    length=15,
                ),
            ],
            32,
            background=colors["Background"],
            opacity=0.8,
            margin=10,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
        # wallpaper="~/.config/wallpapers/Wallpaper.png",
        wallpaper=wallpaper,
        wallpaper_mode="fill",
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    **layout_theme,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
