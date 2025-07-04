import numpy as np
np.random.seed(0)

def create_data(points,classes):
    X=np.zeros((points*classes,2))
    y=np.zeros(points*classes,dtype='uint8')
    for class_number in range(classes):
        ix=range(points* class_number,points*(class_number+1))
        r=np.linspace(0.0,1,points)
        t=np.linspace(class_number*4,(class_number+1)*4,points) +np.random.randn(points)*0.2
        X[ix]=np.c_[r*np.sin(t*2.5),r*np.cos(t*2.5)]
        y[ix]=class_number
    return X,y


class Layer_Dense:
    def __init__(self,n_inputs,n_neurons):
        self.weights=0.10*np.random.randn(n_inputs,n_neurons)
        self.biases=np.zeros((1,n_neurons))
    def forward(self,inputs):
        self.output=np.dot(inputs,self.weights) + self.biases

class ReLU:
    def forward(self,inputs):
        self.output=np.maximum(0,inputs)

class Softmax:
    def forward(self,inputs):
        exp_values=np.exp(inputs-np.max(inputs,axis=1,keepdims=True))
        probabilities=exp_values/np.sum(exp_values,axis=1,keepdims=True)
        self.output=probabilities

X,y=create_data(100,3)
layer1=Layer_Dense(2,3)
activation1=ReLU()

layer2=Layer_Dense(3,3)
activation2=Softmax()

layer1.forward(X)
activation1.forward(layer1.output)
layer2.forward(activation1.output)
activation2.forward(layer2.output)

print(activation2.output[:5])
