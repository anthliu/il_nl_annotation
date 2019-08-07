# Advice Labeler

## Trajectory Format

Pickle file of the format
```
{
    'seed': SEED,
    'trajectory': [(s0, a0), ..., (sn, an)]
}
```

## Making Annotations

```
./annotate.py TRAJECTORY_FILE ENV
```

Saves to `TRAJECTORY_FILE + .annotated`

Example:
```
./annotate.py alien/Alien-v0_trajectory_1.pkl Alien-v0
```

Controls:
* Pause: space
* Skip forward/backward: left/right
* Mark beginning/end of annotation: enter
* Finish: escape

## Viewing Annotations
```
./annotate.py TRAJECTORY_FILE ENV
```

Example:
```
./replay_annotation.py alien/Alien-v0_trajectory_0.pkl.annotated Alien-v0
```

