
def activateFunction(data: float) -> float:
    return max(0.0, data)


def functionLoss(data: list[float], result: list[float]):
    total_loss: float = 0.0
    for i in range(len(data)):
        total_loss += (data[i] - result[i])**2
    return total_loss / len(data)

def compute_gradients(inputs: list[float], weights: list[float], bias: float, target: float):
    prediction = neuron(inputs, weights, bias)
    error = prediction - target

    gradients = []
    for x in inputs:
        gradients.append(2 * error * x)

    bias_gradient = 2 * error

    return gradients, bias_gradient



def neuron(data: list[float], weight: list[float], bias: float = 0.0):
    if len(data) != len(weight):
        return []
    new_data: float = sum(weight[i] * data[i] for i in range(len(data)))
    return activateFunction(new_data + bias)


def layer(data: list[float], weight: list[list[float]], bias: list[float]):
    result: list[float] = []
    for i in range(len(weight)):
        result.append(neuron(data, weight[i], bias[i]))
    return result

learning_rate = 0.01
inputs = [2.0, -1.0, 3.0]
# weights = [[0.5, 1.5, -2.0], [0.2, 1.4, 2.4], [0.1, 2.4, -7.0]]
weights = [0.5, 1.5, -2.0]
# bias = [1.0, 2.0, 3.0]
bias = 3.0
target = 10.0

for _ in range(1000):
    prediction = neuron(inputs, weights, bias)
    print(prediction)
    loss = functionLoss([target], [prediction])
    gradients, bias_gradient = compute_gradients(inputs, weights, bias, target)
    for i in range(len(weights)):
        weights[i] -= learning_rate * gradients[i]
    bias -= learning_rate * bias_gradient
    print(prediction, loss, gradients, bias_gradient, bias)




