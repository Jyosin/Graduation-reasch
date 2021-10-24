import tensorflow as  tf
import os

from models import DNN 
from data_generator import read_data_from_csv
from plotter import Plotter

class Trainer:
    def __init__(self, args) :
        self.args = args 

        self.dataset = self._build_dataset(args['dataset'])
        self.loss = self._build_loss(self.args['loss'])
        self.metric = self._build_metric(self.args['metric'])
        self.optimizer = self._build_optimizer(self.args['optimizer'])
        self.model = self._build_model(self.args['model'])

    def _build_dataset(self, dataset_args) :
        if dataset_args['name'] == 'uniform':
            dataset = read_data_from_csv(filename='labeled.csv',
                                         filepath='./',
                                         batch_size=dataset_args['batch_size'],
                                         CSV_COLUMNS=['x','y'],
                                         num_epochs=dataset_args['epoch'])
        else:
            dataset = None

        return dataset

    def _build_model(self, model_args) :
        if model_args['name'] == 'DNN':
            model = DNN(units=model_args['units'],
                            activactions=model_args['activations'])
        else:
            model = None
        return model

    def _build_metric(self,metric_args):
        metric = tf.keras.metrics.get(metric_args['name'])
        return metric

    def _build_loss(self, loss_args) :
        loss = tf.keras.losses.get(loss_args['name'])
        return loss

    def _build_optimizer(self, optimizer_args) :
        if optimizer_args['name'] == 'SGD' :
            optimizer = tf.keras.optimizers.SGD(learning_rate=optimizer_args['learning_rate'])
        else:
            optimizer = None
        return optimizer

    def train_step(self,x):
        inputs = x['x']
        labels = x['y']
        with tf.GradientTape() as tape:
            prediction = self.model(inputs)
            loss = self.loss(prediction,labels)
            grad = tape.gradient(loss,self.model.trainable_variables)
        
        
        self.optimizer.apply_gradients(zip(grad,self.model.trainable_variables))
        self.metric.update_state(loss)

        return loss

    def valid_step(self,x):
        inputs = x['x']
        prediction = self.model(inputs)

    def just_build(self):
        iter_ds = iter(self.dataset)
        x = iter_ds.get_next()
        x['x'] = tf.reshape(x['x'],(-1,1))
        self.model(x['x'])

    def run(self):
        iter_ds = iter(self.dataset)

        while True : 
            x = iter_ds.get_next()
            x['x'] = tf.reshape(x['x'],(-1,1))

            self.train_step(x)
            print("loss:",self.metric.result().numpy())
            self.metric.reset_states()

    def save_model_weights(self,filepath='./saved_models',name = 'model.h5',save_format="h5"):
        num = len(os.listdir(filepath))
        save_path = os.path.join(filepath,str(num)+'/')
        if os.path.exists(save_path):
            self.model.save_weights(save_path+name, save_format=save_format)
        else:
            os.mkdir(save_path)
            self.model.save_weights(save_path+name, save_format=save_format)
        print("model saved in {}".format(save_path+name))

    def load_model_weights(self,filepath='./saved_models',num = -1,name='model.h5'):
        if num == -1:
            num = len(os.listdir(filepath))-1
        filepath = os.path.join(filepath,str(num)+'/')

        if os.path.exists(filepath):
            # import pdb
            # pdb.set_trace()
            self.just_build()
            self.model.load_weights(filepath+name)
            print("model load from {}".format(filepath+name))
        else:
            print("path dosen't exits.")

    def evaluate(self):
        iter_test = iter(self.dataset)
        self.metric.reset_states()

        while True:
            try:
                x = iter_test.get_next()
            except:
                print("run out of data. ")
                break
            x['x'] = tf.reshape(x['x'],(-1,1))
            prediction = self.model(x['x'])
            loss = self.loss(prediction,x['y'])
            self.metric.update_state(loss)
        
        avg_loss = self.metric.result().numpy()
        print("Avg loss", avg_loss)
        return avg_loss

if __name__ == "__main__":
    trainer_args = {'loss':{'name':'mse'},
                    'metric':{'name':'Mean'},
                    'optimizer':{'name':'SGD','learning_rate':0.001},
                    'dataset':{'name':'uniform','batch_size':12,'epoch':3},
                    'model':{'name':'DNN','units':[64,16,1],
                             'activations':['tanh','tanh','tanh']}, }
    
    trainer = Trainer(trainer_args)
    trainer.just_build()
    trainer.model.summar()

    avg_loss = trainer.self_eveluate()
    print(avg_loss)

    plotter = Plotter(trainer.model)
    normalized_random_direction = plotter.xreate_random_direction(norm = 'layer')
    plotter.set_weights([normalized_random_direction], step=0.5)

    # avg_loss = trainer.self_evaluate()
    # print(avg_loss)    