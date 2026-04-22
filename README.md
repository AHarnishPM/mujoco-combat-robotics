Members: Riddhi Lamba, Aaron Harnish

Project for CS 4756, modeling Huey, a 3lb autonomous battlebot, in MuJoCo.

## Arena Scene (NHRL 8ft x 8ft)

The MuJoCo arena floor scene is in:

- `models/nhrl_arena.xml`

It creates an 8ft x 8ft floor (`2.4384m x 2.4384m`) with boundary walls and cameras so you can open it directly in MuJoCo desktop.

## Open In MuJoCo Desktop

1. Launch MuJoCo desktop app.
2. Open `models/nhrl_arena.xml`.
3. Use camera `iso` or `top_down` in the UI camera selector.
4. Open the Controls/Actuators panel and move:
   - `left_drive_motor`
   - `right_drive_motor`
   - `weapon_motor`

### Quick drive values in MuJoCo desktop

- Forward: left `+20`, right `+20`
- Reverse: left `-20`, right `-20`
- Turn left: left `-12`, right `+12`
- Turn right: left `+12`, right `-12`
- Spin weapon: `weapon_motor` around `80` to `160`

## Add Your Robot CAD + Wheels + Weapon

Use `models/robot_template.xml` as the base template:

1. Export robot CAD parts to STL or OBJ:
   - chassis
   - wheel (single mesh, reused for left/right)
   - weapon (bar, drum, etc.)
2. Put mesh files under `models/meshes/`.
3. In `models/robot_template.xml`, uncomment mesh assets and set file names/scales.
   - Typical CAD mm -> m scale is `0.001 0.001 0.001`.
4. Keep collision geoms simple (box/cylinder/capsule), and use mesh mostly for visuals.
5. Tune joint axes:
   - wheel hinge axes should align with wheel axle
   - weapon hinge axis should align with spinner shaft
6. Copy your robot body/actuator definitions from `models/robot_template.xml` into `models/nhrl_arena.xml` (or maintain a combined scene file) before loading in MuJoCo desktop.

## Controls/Actuators

`robot_template.xml` includes 3 motors:

- `left_drive_motor`
- `right_drive_motor`
- `weapon_motor`

In MuJoCo desktop, use the Actuator controls panel to send inputs and verify wheel/weapon behavior.

## Keyboard Teleop (Arrow Keys + F)

You can drive the arena robot with keyboard input using:

- `scripts/keyboard_teleop.py`

### Install Python deps

- `pip install mujoco`

### Run

- `python3 scripts/keyboard_teleop.py`

macOS note:

- Use `python3`, not `mjpython`, for `scripts/keyboard_teleop.py`.
- `mjpython` can crash with `NSWindow should only be instantiated on the main thread` when creating GLFW windows.

Optional args:

- `--model models/nhrl_arena.xml`
- `--drive 22`
- `--turn 14`
- `--weapon 120`
- `--weapon-key F`

### Key mapping

- `Up` / `Down`: forward / reverse
- `Left` / `Right`: left / right turn
- `F`: weapon spin (while held)

Drive mixing is differential:

- `left = throttle*drive - turn*turn_gain`
- `right = throttle*drive + turn*turn_gain`