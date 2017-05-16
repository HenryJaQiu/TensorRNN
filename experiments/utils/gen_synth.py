import numpy as np
import cPickle as pickle


def gen_logistic_series(x0, num_steps, num_freq):
    alpha = 4.0
    x = np.ndarray((num_steps,1) )
    x[0]  = x0
    
    xx = np.ndarray((num_steps//num_freq,1))
    f = lambda  x ,t: alpha* x[t] * (1.0 - x[t]) 
    j = 0
    for t in range(num_steps-1):
        if t%num_freq ==0:
            xx[j]  = x[t]
            j += 1
        x[t+1] = f(x,t)
    logistic_series = xx
    return logistic_series


def lorenz(x, y, z, s=10, r=28, b=2.667):
    x_dot = s*(y - x)
    y_dot = r*x - y - x*z
    z_dot = x*y - b*z
    return x_dot, y_dot, z_dot

def gen_lorenz_series(x0, y0, z0, num_steps, num_freq):
    dt = 0.01
    stepCnt = num_steps

    # Need one more for the initial values
    xs = np.empty((stepCnt,))
    ys = np.empty((stepCnt,))
    zs = np.empty((stepCnt,))

    # Setting initial values
    #xs[0], ys[0], zs[0] = (0., 1., 1.05)
    xs[0] = x0
    ys[0] = y0
    zs[0] = z0

    xss = np.empty((stepCnt//num_freq,))
    yss = np.empty((stepCnt//num_freq,))
    zss = np.empty((stepCnt//num_freq,))
    # Stepping through "time".
    j = 0
    for i in range(stepCnt-1):
        # Derivatives of the X, Y, Z state
        if i%num_freq ==0:
            xss[j] = xs[i]
            yss[j] = ys[i]
            zss[j] = zs[i]
            j += 1
        x_dot, y_dot, z_dot = lorenz(xs[i], ys[i], zs[i])
        xs[i + 1] = xs[i] + (x_dot * dt)
        ys[i + 1] = ys[i] + (y_dot * dt)
        zs[i + 1] = zs[i] + (z_dot * dt)

    #save the sequence for training
    lorenz_series = np.transpose(np.vstack((xss,yss,zss)))
    return lorenz_series

def gen_lorenz_dataset2(file_name="lorenz.pkl"):
    #define initial range
    num_samples = int(1e4)
    num_freq = int(5)
    num_steps = int(1e2)*num_freq
    
    init_range = np.random.uniform(-20,20,(num_samples,3))
   
    lorenz_series_mat = np.ndarray((num_samples, num_steps//num_freq, 3))

    for i in range(num_samples):
        x0,y0,z0 = init_range[i,:]
        series = gen_lorenz_series(x0,y0,z0, num_steps, num_freq )
        lorenz_series_mat[i,:,:] = series
                
    pickle.dump(lorenz_series_mat, open(file_name,"wb")) 


def gen_logistic_dataset2(file_name = "logistic.pkl"):
    """generate set of chaotic time series with randomly selected initial"""
    num_samples = int(1e4)
    num_freq = int(5)
    num_steps = int(1e2)*num_freq
    
    init_range = np.random.uniform(0.0,1.0,(num_samples,1))
   
    logistic_series_mat = np.ndarray((num_samples, num_steps//num_freq, 1))

    for i in range(num_samples):
        x0 = init_range[i,:]
        series = gen_logistic_series(x0, num_steps, num_freq )
        logistic_series_mat[i,:,:] = series

    pickle.dump(logistic_series_mat,open(file_name,"wb"))

def gen_lorenz_dataset1(file_name="lorenz.pkl"):
    #define initial range 
    num_steps = int(1e6)
    num_freq = int(1)
    lorenz_series_mat = np.ndarray((num_steps, 3))

    x0,y0,z0 = (0.0,0.0,0.0)
    series = gen_lorenz_series(x0,y0,z0, num_steps, num_freq )
    lorenz_series_mat = series
                
    pickle.dump(lorenz_series_mat, open(file_name,"wb")) 


def gen_logistic_dataset1(file_name = "logistic.pkl"):
    """generate set of chaotic time series with randomly selected initial"""
    num_freq = int(1)
    num_steps = int(1e6)
   
    logistic_series_mat = np.ndarray((num_steps, 1))

    
    x0 = 0.0
    series = gen_logistic_series(x0, num_steps, num_freq )
    logistic_series_mat = series

    pickle.dump(logistic_series_mat,open(file_name,"wb"))

def gen_lorenz_dataset(file_name="lorenz.pkl"):
    #define initial range
    num_samples = int(1)
    num_freq = int(1)
    num_steps = int(1e4)*num_freq
    
    init_range = np.random.uniform(-20,20,(num_samples,3))
   
    lorenz_series_mat = np.ndarray((num_steps//num_freq, 3*num_samples))

    for i in range(num_samples):
        x0,y0,z0 = init_range[i,:]
        series = gen_lorenz_series(x0,y0,z0, num_steps, num_freq )
        lorenz_series_mat[:,i*3 : (i+1)*3] = series
    # print(lorenz_series_mat.shape)
                
    pickle.dump(lorenz_series_mat, open(file_name,"wb")) 


def gen_logistic_dataset(file_name = "logistic.pkl"):
    """generate set of chaotic time series with randomly selected initial"""

    num_samples = int(1)
    num_freq = int(1)
    num_steps = int(1e4)*num_freq
    
    init_range = np.random.uniform(0.0,1.0,(num_samples,1))
   
    logistic_series_mat = np.ndarray((num_steps//num_freq, 1*num_samples))

    for i in range(num_samples):
        x0 = init_range[i,:]
        series = gen_logistic_series(x0, num_steps, num_freq )
        logistic_series_mat[:,i:i+1] = series
    # print(logistic_series_mat.shape)

    pickle.dump(logistic_series_mat,open(file_name,"wb"))

def main():
    data_path = "/home/roseyu/data/tensorRNN/"
   # data_path = "/Users/roseyu/Documents/Python/"

    file_name = data_path+"logistic.pkl"
    gen_logistic_dataset(file_name)
    print("Finish generating logistic")

    file_name = data_path+"lorenz.pkl"
    gen_lorenz_dataset(file_name)

    print("Finish generating lorenz")
if __name__== "__main__":
    main()
