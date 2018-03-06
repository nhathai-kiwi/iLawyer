# ilawyer machine learning algorithm
# in-house development
import numpy as np


# sigmoid function
def sigmoid(z):
    return 1/(1 + np.exp(-z))


def sigmoid_gradient(z):
    return sigmoid(z)*(1 - sigmoid(z))


# generate input in good format
def gen_inp():

    return 0


# generate TS in good format
def gen_ts():

    return 0


# initialize parameters by randomization
def gen_rand_init_weights(L_in, L_out):
    eps = 0.12
    # eps = 6**.5/(L_in + L_out)**.5
    return np.random.uniform(0, 1, (L_out, 1 + L_in))*2*eps - eps


# prediction
# get the label
def prediction(params, X):
    return 0


# cost function
def cost_func(nn_params, *args):
    layers_size, X, y, nn_lambda = args
    J = 0
    input_layer_size = layers_size[0]
    hidden_layer_size = layers_size[1]
    output_layer_size = layers_size[2]

    Theta1 = np.reshape(nn_params[0:(hidden_layer_size * (input_layer_size + 1))],
                        (hidden_layer_size, input_layer_size + 1))
    Theta2 = np.reshape(nn_params[hidden_layer_size * (input_layer_size + 1):np.size(nn_params)],
                        (output_layer_size, hidden_layer_size + 1))


    m = np.size(X, 0)
    return J


# cost function
def costFunc(nn_params, input_layer_size, hidden_layer_size, num_labels, X, y, nn_lambda):
    Theta1 = np.reshape(nn_params[0:(hidden_layer_size*(input_layer_size + 1))], (hidden_layer_size, input_layer_size + 1))
    Theta2 = np.reshape(nn_params[hidden_layer_size*(input_layer_size + 1):np.size(nn_params)])
    m = np.size(X,0)
    J = 0
    Theta1_grad = np.zeros((np.size(Theta1, 0), np.size(Theta1, 1)))
    Theta2_grad = np.zeros((np.size(Theta2, 0), np.size(Theta2, 1)))
    # feed forward
    a1_all = np.concatenate((np.ones((m, 1)), X), axis=1)
    z2_all = np.dot(Theta1, a1_all.transpose()).transpose()
    a2_all = np.concatenate((np.ones((m, 1)), sigmoid(z2_all)), axis=1)
    z3_all = np.dot(Theta2, a2_all.transpose()).transpose()
    a3_all = sigmoid(z3_all)

    all_labels = np.eye(num_labels)

    # calculate 1st term corresponding to non regularized cost
    s = 0
    for cnt in range(0, m):
        for cnt1 in range(1, num_labels + 1):
            temp = -all_labels[y(cnt), cnt1]*np.log(a3_all[cnt, cnt1]) - (1 - all_labels[y(cnt), cnt1])*np.log(1 - a3_all[cnt, cnt1])
            s = s + temp
    J_nr = 1/m*s
    # calculate 2nd tern corresponding to regularized part
    # remember that we do not regularize bias intercepter
    Theta1[:, 1] = 0
    Theta2[:, 1] = 0
    J_rg = nn_lambda / 2 / m * (np.sum(Theta1 ** 2) + np.sum(Theta2 ** 2))
    J = J_nr + J_rg


    # calculate gradient
    delta3 = np.zeors((m, num_labels))
    delta2 = np.zeors((m, hidden_layer_size))
    D1 = np.zeros((np.size(Theta1, 0), np.size(Theta1, 1)))
    D2 = np.zeros((np.size(Theta2, 0), np.size(Theta2, 1)))
    for cnt in range(0, m):
        delta3[cnt, :] = a3_all[cnt, :] - all_labels[y(cnt), :]
        delta2[cnt, :] = np.dot(delta3[cnt, :], Theta2[:, 1:(hidden_layer_size + 1)]) * sigmoid_gradient(z2_all[cnt, :])
        D1 = D1 + np.dot(delta2[cnt, :].transpose(), a1_all[cnt, :])
        D2 = D2 + np.dot(delta3[cnt, :].transpose(), a2_all[cnt, :])
    Theta1_grad = 1/m*D1
    Theta2_grad = 1/m*D2
    Theta1_grad[:, 1:(input_layer_size + 1)] = Theta1_grad[:, 1:(input_layer_size + 1)] + nn_lambda/m*Theta1[:, 1:(input_layer_size + 1)]
    Theta2_grad[:, 1:(input_layer_size + 1)] = Theta2_grad[:, 1:(input_layer_size + 1)] + nn_lambda/m*Theta2[:, 1:(input_layer_size + 1)]
    grad = np.concatenate((np.ravel(Theta1_grad), np.ravel(Theta2_grad)))

    return J, grad



