#!/usr/bin/env python3
"""Stable keyboard teleop for MuJoCo 3.7.x using a custom GLFW loop.

Controls:
- Up/Down: forward/reverse throttle
- Left/Right: turn
- F: weapon spin while held
- Esc: close window
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import mujoco
from mujoco.glfw import glfw


KEY_UP = glfw.KEY_UP
KEY_DOWN = glfw.KEY_DOWN
KEY_LEFT = glfw.KEY_LEFT
KEY_RIGHT = glfw.KEY_RIGHT


def actuator_id(model: mujoco.MjModel, name: str) -> int:
    idx = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, name)
    if idx < 0:
        raise ValueError(f"Actuator '{name}' not found in model.")
    return idx


def main() -> None:
    exe_name = pathlib.Path(sys.executable).name.lower()
    if sys.platform == "darwin" and "mjpython" in exe_name:
        raise RuntimeError(
            "On macOS, run this script with python3 (not mjpython):\n"
            "  python3 scripts/keyboard_teleop.py\n"
            "mjpython runs user code off the main thread, and Cocoa/GLFW window creation crashes."
        )

    parser = argparse.ArgumentParser(description="Keyboard teleop for battle bot arena")
    parser.add_argument("--model", default="models/nhrl_arena.xml", help="Path to MJCF model")
    parser.add_argument("--drive", type=float, default=22.0, help="Drive command magnitude")
    parser.add_argument("--turn", type=float, default=14.0, help="Turn command magnitude")
    parser.add_argument("--weapon", type=float, default=120.0, help="Weapon command while held")
    parser.add_argument("--weapon-key", default="F", help="Single-character weapon key")
    args = parser.parse_args()

    weapon_key = args.weapon_key.upper()
    if len(weapon_key) != 1:
        raise ValueError("--weapon-key must be one character, e.g. F")
    weapon_keycode = glfw.get_key_scancode(ord(weapon_key))

    model = mujoco.MjModel.from_xml_path(args.model)
    data = mujoco.MjData(model)

    left_id = actuator_id(model, "left_drive_motor")
    right_id = actuator_id(model, "right_drive_motor")
    weapon_id = actuator_id(model, "weapon_motor")

    if not glfw.init():
        raise RuntimeError("Failed to initialize GLFW")

    window = glfw.create_window(1400, 900, "MuJoCo Teleop", None, None)
    if not window:
        glfw.terminate()
        raise RuntimeError("Failed to create GLFW window")

    glfw.make_context_current(window)
    glfw.swap_interval(1)

    cam = mujoco.MjvCamera()
    opt = mujoco.MjvOption()
    scene = mujoco.MjvScene(model, maxgeom=10000)
    context = mujoco.MjrContext(model, mujoco.mjtFontScale.mjFONTSCALE_150.value)

    # Start from an angled view of the arena.
    cam.type = mujoco.mjtCamera.mjCAMERA_FREE
    cam.azimuth = 135.0
    cam.elevation = -30.0
    cam.distance = 4.0
    cam.lookat[:] = [0.0, 0.0, 0.12]

    print(f"Teleop active: arrows drive/turn, {weapon_key} weapon.")
    while not glfw.window_should_close(window):
        throttle = 0.0
        turn = 0.0

        if glfw.get_key(window, KEY_UP) == glfw.PRESS:
            throttle += 1.0
        if glfw.get_key(window, KEY_DOWN) == glfw.PRESS:
            throttle -= 1.0
        if glfw.get_key(window, KEY_LEFT) == glfw.PRESS:
            turn += 1.0
        if glfw.get_key(window, KEY_RIGHT) == glfw.PRESS:
            turn -= 1.0

        weapon_pressed = glfw.get_key(window, ord(weapon_key)) == glfw.PRESS
        if weapon_keycode != -1:
            # Some keyboard layouts resolve key better by scancode path.
            weapon_pressed = weapon_pressed or (
                glfw.get_key_scancode(ord(weapon_key)) == weapon_keycode
                and glfw.get_key(window, ord(weapon_key)) == glfw.PRESS
            )

        data.ctrl[left_id] = throttle * args.drive - turn * args.turn
        data.ctrl[right_id] = throttle * args.drive + turn * args.turn
        data.ctrl[weapon_id] = args.weapon if weapon_pressed else 0.0

        mujoco.mj_step(model, data)

        width, height = glfw.get_framebuffer_size(window)
        viewport = mujoco.MjrRect(0, 0, width, height)
        mujoco.mjv_updateScene(
            model,
            data,
            opt,
            None,
            cam,
            mujoco.mjtCatBit.mjCAT_ALL.value,
            scene,
        )
        mujoco.mjr_render(viewport, scene, context)
        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
