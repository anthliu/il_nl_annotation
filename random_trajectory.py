#!/usr/bin/env python

import os
import pickle
import argparse
import gym
from random import randint, choice

def main(args):
    env = gym.make(args.environment)
    for trajectory in range(args.trajectories):
        seed = randint(0, 5000)
        env.seed(seed)
        observation = env.reset()
        d = {'seed': seed, 'trajectory': []}
        for _ in range(args.frames):
            env.render()
            action = env.action_space.sample()
            d['trajectory'].append((observation, action))
            observation, reward, done, info = env.step(action)
            if done:
                break

        with open(os.path.join(args.out_directory, '{}_trajectory_{}.pkl'.format(args.environment, trajectory)), 'wb') as f:
            pickle.dump(d, f)
        env.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Randomly Sample Trajectories')
    parser.add_argument('out_directory', type=str)
    parser.add_argument('-e', '--environment', type=str, default='CartPole-v0')
    parser.add_argument('-t', '--trajectories', type=int, default=5)
    parser.add_argument('-f', '--frames', type=int, default=5000)

    args = parser.parse_args()
    main(args)
