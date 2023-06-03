# Ml-Agents Eye Control
 Using the ml-agents Unity library, train a NN to conrol a pair of eyes to focus on a target.

 On start:
  - Eye rotation and target position on the black wall are randomized.

 Observations:
 - Twelve vector observations (Four for camera rotation angles, four for camera restriction angles, two pseudo boolean "target on screen" observations, and four taget viewport coordinates).

 Heuristics:
  - Use the arrow keys to control both eyes at the time.
  Up and down correspond to the y axis, and left and right to the x axis.

 Actions:
  - Four descrete branches (one for each axis of rotation per camera)

 Reward / Punishment conditions:
  - Punish agent slightly on every frame.
  - Reward agent on seeing the target partially.
  - Reward agent on fully seeing the target.
  - Reward the agent the closer it get's the target to the center of the cameras' viewports.
  - Reward the agent for holding the target in full view for a determined amount of seconds (end condition).

 Note: Rotation actions are either in the axis of rotation, against it, or no rotation.
