import tensorflow as tf
from tensorflow import keras 
from data_generator import read_data_from_csv

class Linear(keras.layers.Layer):
    def __init__(self, units=32, fuse_layers=None):
        super(Linear, self).__init__()
        self.units = units
        self.fuse_layers = fuse_layers

    def build(self,input_shape):    

        if self.fuse_layers == None :
            w_init = tf.random_normal_initializer(seed=100000)
            self.w = tf.Variable(
                initial_value=w_init(shape=(input_shape[-1], self.units), dtype="float32"),
                trainable=True, name="w"
            )
            b_init = tf.zeros_initializer()
            self.b = tf.Variable(
                initial_value=b_init(shape=(self.units,), dtype="float32"), trainable=True,
                name="b"
            )
        else:
            
            w_init = tf.random_normal_initializer(seed=10000)
            b_init = tf.zeros_initializer()

            self.fuse_w = tf.Variable(
                initial_value=w_init(
                    shape=(input_shape[-1], self.units), dtype="float32"),
                trainable=True, name="w"
                )
            self.b = tf.Variable(
                initial_value=b_init(shape=(self.fuse_layers, 1, self.units), dtype="float32"), trainable=True,
                name="b"
            )
            

    def call(self, inputs):
        if self.fuse_models == None:
            output = tf.matmul(inputs,self.w)+ self.b
        else:
            pass
        return output

class DNN(tf.keras.Model):
    def __init__(self,
                units=[64,32,16,1],
                activactions=['tanh','tanh','tanh','tanh'],
                fuse_models=None):
        super(DNN,self).__init__() 
        # 父类继承 

        self.units = units
        self.activations = activactions
        self.fuse_models = fuse_models
        self.fc_layers = self._build_fc()
        self.fc_act = self._build_act()

    def _build_fc(self):
        layers = []
        for units in self.units:
            layers.append(Linear(units=units))
        return layers

    def _build_act(self):
        acts = []
        for act in self.activations:
            acts.append(tf.keras.layers.Activation(act))
        return acts

    def call(self,inputs):
        x = inputs
        for layer,act in zip(self.fc_layers,self.fc_act):
            x = layer(x)
            x = act(x)
        return x
        
if __name__ == "__main__":
    dataset = read_data_from_csv()
    iter_ds = iter(dataset)
    x = iter_ds.get_next()
    # l1 = Linear()

    x['x'] = tf.reshape(x['x'],(-1,1))

    dnn = DNN()
    output = dnn(x['x'])
    print(output)
