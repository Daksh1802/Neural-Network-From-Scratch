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

class Loss:
    def calculate(self,output,y):
        sample_losses=self.forward(output,y)
        data_loss=np.mean(sample_losses)
        return data_loss
class CategoricalCrossEntropy(Loss):
    def forward(self,y_pred,y_true):
        samples=len(y_pred)
        y_pred_clipped=np.clip(y_pred,1e-7,1-1e-7)
        if len(y_true.shape)==1:
            correct_confidences=y_pred_clipped[range(samples),y_true]
        elif len(y_true.shape)==2:
            correct_confidences=np.sum(y_pred_clipped*y_true,axis=1)
        negative_log_likelihoods=-np.log(correct_confidences)
        return negative_log_likelihoods


X,y=create_data(100,3)
layer1=Layer_Dense(2,3)
activation1=ReLU()

layer2=Layer_Dense(3,3)
activation2=Softmax()

layer1.forward(X)
activation1.forward(layer1.output)
layer2.forward(activation1.output)
activation2.forward(layer2.output)
loss_function=CategoricalCrossEntropy()
total_loss=loss_function.calculate(activation2.output,y)
print("Loss: ",total_loss)
predictions=np.argmax(activation2.output,axis=1)
accuracy=np.mean(predictions==y)
print("Accuracy: ",accuracy)
