#!/usr/bin/env python
import time
from copy import deepcopy
import pickle
import argparse
import gym


def main(args):
    with open(args.trajectory_file, 'rb') as f:
        d = pickle.load(f)
    seed = d['seed']
    trajectory = d['trajectory']
    # save checkpoints
    env = gym.make(args.environment)
    env.render()
    env.seed(seed)
    env.reset()
    for frame, buf in enumerate(trajectory):
        env.render()
        time.sleep(args.frame_rate)
        if len(buf) > 2:
            _, a, (indicator, n) = buf
        else:
            indicator = 'c'
            _, a = buf
        if indicator == 's':
            print('start: ', n)
        elif indicator == 'e':
            print('end: ', n)
        _, _, done, _ = env.step(a)
        if done:
            break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Annotate trajectory')
    parser.add_argument('trajectory_file', type=str)
    parser.add_argument('environment', type=str)
    parser.add_argument('-f', '--frame_rate', type=float, default=0.05)

    args = parser.parse_args()
    main(args)
