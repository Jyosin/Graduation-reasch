from utils import *
import argparse
from trainer.uniform_trainer import UniformTrainer
from trainer.cifa10_trainer import Cifar10Trainer
from plotter import Plotter
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Plot lossland around ture minima.')
    parser.add_argument('--config', default='scripts/configs/2d_uniform_dnn.yaml')
    args = parser.parse_args()
    config = get_yml_content(args.config)

    trainer_args = config['Trainer']
    plotter_args = config['Plotter']

    if trainer_args['dataset']['name'] == 'uniform':
        trainer = UniformTrainer(trainer_args)
    elif trainer_args['dataset']['name'] == 'cifar10':
        trainer = Cifar10Trainer(trainer_args)
    plotter = Plotter(plotter_args, trainer)

    plotter.run()
