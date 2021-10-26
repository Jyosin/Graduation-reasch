import os
import h5py
import numpy as np
import tensorflow as tf

from trainer import Trainer

class Plotter:
    def __init__(self, plotter_args, model):
        self.step = plotter_args['step']
        self.num_evaluate = plotter_args['num_evaluate']
        self.fuse_models = plotter_args['fuse_models']
        self.model = model

    def get_weights(self):
        return self.model.trainable_weights
    
    def fuse_direction(self,normalized_directions,init_fuse= False):
        random_directions= []
        for d in normalized_directions:
            fuse_random_direction =[]
            for i in range(self.fuse_models):
                if init_fuse == True:
                    fuse_random_direction.append(d)
                else:
                    fuse_random_direction.append(d*(i+1))
            random_directions.append(tf.stack(fuse_random_direction))
        return random_directions

    def set_weights(self,directions=None, step=None):
        #l(alpha * theta + (1- alpha)* theta')=> L(theta + alpha *(theta-theta'))
        #l(theta + alpha * theta_1 + beta * theta_2)
        #Each direction have same shape with trainable weights
        #)
        if directions == None:
            print("None of directions")
        else:
            if len(directions) == 2:
                dx = directions[0]
                dy = directions[1]
                changes = [step[0]*d0 +step[1]*d1 for (d0, d1)in zip(dx, dy)]
            else:
                changes = [d*step for d in directions[0]]

        weights = self.get_weights()
        for(weight,change) in zip(weights, changes):
            weight.assign_add(change)

    def get_random_weights(self,weights):
        if self.fuse_directionfuse_models == None:
            return [tf.random.normal(w.shape)for w in weights]
        else:
            single_random_direction = []
            for w in weights:
                dims = list(w.shape)
                single_random_direction.append(
                    tf.random.normal(shape=dims[1:]))
            return single_random_direction

    def get_diff_weights(self, weights_1, weights_2):
        return [w2 - w1 for (w1, w2) in zip(weights_1, weights_2)]

    def normalize_direction(self,direction,weights,norm='filter'):
        # filter normalize : d = direction / norm(direction) * weight
        if norm == 'filter':

            normalized_direction = []
            for d, w in zip(direction, weights):
                normalized_direction.append(
                d = d / (tf.norm(d) + 1e-10) * tf.norm(w))
        elif norm == 'layer':
            normalized_direction = direction * tf.norm(weights)/tf.norm(direction)
        elif norm == 'weight':
            normalized_direction = direction * weights
        elif norm == 'd_filter':
            normalized_direction = []
            for d in direction :
                normalized_direction.append(d/ (tf.norm(d)+1e-10))
        elif norm == 'd_layer':
            normalized_direction = direction/tf.norm(direction)
        return normalized_direction

    def normalize_directions_for_weights(self,direction,weights, norm="filter", ignore="bias_bn"):
        normalized_direction = []
        for d,w in zip(direction,weights):
            if len(d.shape) <= 1:
                if ignore == "bias_bn":
                    d = tf.zeros(d.shape)
                else:
                    d=w
                normalized_direction.append(d)
            else:
                normalized_direction.append(
                    self.normalize_direction(d ,w, norm))
        if self.fuse_models != None:
            fused_normalized_direction = self.fuse_direction(
                normalized_direction
            )
        return fused_normalized_direction, normalized_direction

    def create_target_direction(self):
        pass

    def creat_random_direction(self, ignore='bias_bn', norm='filter'):
        weights = self.get_weights()
        direction = self.get_random_weights(weights)
        direction = self.normalize_directions_for_weights(
            direction,weights, norm ,ignore
        )
        return direction
        

    def setup_direction(self):
        pass

    def name_direction_file(self):
        pass

    def load_directions(self):
        pass

