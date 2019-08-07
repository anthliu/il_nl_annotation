#!/usr/bin/env python
import time
from copy import deepcopy
import pickle
import argparse
import gym

KEYS = {
    65363: 'right',
    65361: 'left',
    65293: 'enter',
    65307: 'esc',
    65288: 'back'
}

def translate(key):
    if key in KEYS:
        return KEYS[key]
    return chr(key)

def main(args):
    with open(args.trajectory_file, 'rb') as f:
        d = pickle.load(f)
    seed = d['seed']
    trajectory = d['trajectory']
    labeled_trajectory = deepcopy(trajectory)
    total_frames = len(trajectory)

    # state flags
    state = {
        'not_pause': True,# not pause for release trick
        'done': False,
        'skip_back': False,
        'skip_forw': False,
        'annotate': False,
        'undo_anno': False,
    }

    def key_press(key, mod):
        c = translate(key)
        if c == 'esc':
            state['done'] = True
        elif c == ' ':
            state['not_pause'] = not state['not_pause']
        elif c == 'left':
            state['skip_back'] = True
        elif c == 'right':
            state['skip_forw'] = True
        elif c == 'enter':
            state['annotate'] = True
        elif c == 'back':
            state['undo_anno'] = True

    def key_release(key, mod):
        pass


    env_cache = []
    # save checkpoints
    print('Caching states...')
    env = gym.make(args.environment)
    env.render()
    env.unwrapped.viewer.window.on_key_press = key_press
    env.unwrapped.viewer.window.on_key_release = key_release
    env.seed(seed)
    env.reset()
    for frame, (_, action) in enumerate(trajectory):
        env_cache.append(env.ale.cloneState())
        _, _, done, _ = env.step(action)
        if done:
            break

    # start
    print('Starting...')
    frame = 0

    anno_begin = None
    anno_end = None
    while not state['done']:
        env.ale.restoreState(env_cache[frame])
        env.render()
        while not any(state.values()):# pause release trick
            env.render()
            time.sleep(0.1)

        if state['skip_back']:
            frame = max(0, frame - args.skip_frames)
            print('Skipping to frame {}.'.format(frame))
            state['skip_back'] = False
        elif state['skip_forw']:
            frame = min(total_frames - 1, frame + args.skip_frames)
            print('Skipping to frame {}.'.format(frame))
            state['skip_forw'] = False
        elif state['annotate']:
            if anno_begin is None:
                anno_begin = frame
                print('Annotation mark at frame {}.'.format(anno_begin))
            elif anno_end is None:
                anno_end = frame
                annotation = input('frames {}-{} >> '.format(anno_begin, anno_end))
                for frame in range(anno_begin, anno_end + 1):
                    if frame == anno_begin:
                        indicator = 's'
                    elif frame == anno_end:
                        indicator = 'e'
                    else:
                        indicator = 'c'
                    s, a = trajectory[frame]
                    labeled_trajectory[frame] = (s, a, (indicator, annotation))
                anno_begin = None
                anno_end = None
            state['annotate'] = False
        elif state['undo_anno']:
            anno_begin = None
            anno_end = None
            print('Cleared Annotation Mark.')
            state['undo_anno'] = False
        else:
            frame = min(frame + 1, total_frames - 1)
            if frame >= total_frames - 1:
                print('Reached End of trajectory.')
                state['not_pause'] = False

        time.sleep(args.frame_rate)
        env.step(trajectory[frame][1])

    print('Saving to {}.'.format(args.trajectory_file + '.annotated'))
    d['trajectory'] = labeled_trajectory
    with open(args.trajectory_file + '.annotated', 'wb') as f:
        pickle.dump(d, f)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotate trajectory')
    parser.add_argument('trajectory_file', type=str)
    parser.add_argument('environment', type=str)
    parser.add_argument('-s', '--skip_frames', type=int, default=60)
    parser.add_argument('-r', '--frame_rate', type=float, default=1/30)

    args = parser.parse_args()
    main(args)
