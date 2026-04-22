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
6. Include robot in arena by uncommenting this line in `models/nhrl_arena.xml`:
   - `<include file="robot_template.xml"/>`

## Controls/Actuators

`robot_template.xml` includes 3 motors:

- `left_drive_motor`
- `right_drive_motor`
- `weapon_motor`

In MuJoCo desktop, use the Actuator controls panel to send inputs and verify wheel/weapon behavior.