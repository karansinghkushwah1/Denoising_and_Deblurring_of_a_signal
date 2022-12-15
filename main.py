#First we import required libraries such as numpy , cmath , csv and matplotlib
import numpy as np                                                          #used for somevalues like pi
import cmath                                                                #already in pyhton , used for some math work
import csv                                                                  #used for importing given data in csv formet
import matplotlib.pyplot as plt                                             #used for plotting purpose

with open('data.csv') as csv_doc:                                           #code to read given csv file
    file=csv.reader(csv_doc)
    x_n=[]
    y_n=[]
    for l in file:
        if(l[0][0]=='x'):                                                   #given that first column of data is for x_n values
            pass
        else:
            x_n.append(float(l[0]))
        if(l[1][0]=='y'):                                                   #given that second column of data is for y_n values
            pass
        else:
            y_n.append(float(l[1]))
#now we plot our intial data as x_n and y_n for better understanding
#use some properties of matplot to style the plot
plt.plot(x_n, '-k', label="X[n]")
plt.plot(y_n, '-r', label="Y[n]")
plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)

plt.title("Initial figure of True and distorted value")                     #provide title for graph
plt.xlabel("Time")                                                          #label x-axis
plt.ylabel("Temperature")                                                   #label y-axis
plt.show()

#Now, we make a DFT function to find discrete Fourier transform of given distorted signal y[n] and also for h[n] , in some point also used for filtered signal
def DFT(a):
    N = len(a)
    X=[]
    for i in range(N):
        add = 0
        for n in range(N):
            add += a[n] * cmath.exp(complex(0, -1 * i * 2 * np.pi * n / N))  #we simply try to apply discrete fourier transform formula
        X.append(add)

    print(X)
    return X


#Now , make a Filter function for filtering y[n] signal and in second approach used for filtering idft_dft_y. basically it help in denoising the signal
def filter(y):
    fy = np.zeros(193)                          #Return a new array of given number, filled with zeros.

    for i in range(2, len(y) - 2):              #make a loop for taking average of 5 values
        fy[i] = (y[i-2] + y[i-1] + y[i] + y[i+1] + y[i+2])/5

#define averaging algoritm for bounding conditions

    fy[0] = (y[0] + y[0] + y[0] + y[1] + y[2])/5                    #for Oth element there is no term for -2,-1 position so take it as 0th term
    fy[1] = (y[0] + y[0] + y[1] + y[2] + y[3]) / 5                  #for 1st element there is no term for -2 position so take it as 0th term
    fy[-1] = (y[-1] + y[-2] + y[-3]) / 3                            #for last term we tak the average of 3 terms because there is no term in right side or we can also similiar way that we use for zero and 1st element
    fy[-2] = (y[-4] + y[-3] + y[-2] + y[-1]) / 4                    #for second last term we tak the average of 4 terms because there is no term in right side or we can also similiar way that we use for zero and 1st element

    return fy


#Make a function for calculating IDFT for division values and also use in second approach for finding idft of dft(y).
def idft(a):
    N = len(a)

    x = []
    for n in range(N):
        add = 0
        for k in range(N):
            add += a[k] * cmath.exp(complex(0, 2 * np.pi * k * n / N))          #we simply try to apply inverse discrete fourier transform formula
        x.append(add.real / N)
    return x




filtered_signal=filter(y_n)                                         #calling function filter for signal y[n]
plt.plot(filtered_signal)                                           #plotting filterred signal
plt.title('FILTERED SIGNAL Y')                                      #title of graph
plt.show()

Y=DFT(filtered_signal)                                              #calling function DFT for filtered_signal

h=np.array([1/16,4/16,6/16,4/16,1/16])                              #given impulse response

H_DFT=DFT(h)                                                        #calling DFT function for given impulse response
#plt.plot(H_DFT) #plotting h_DFT
#plt.title('DFT SINGAL OF H')


#Now, we divide DFT of filterd y[n] by DFT of h[n] and collect them in a list 'division_values'
division_values=[]
for i in range(len(Y)):
    if i<5 and abs(H_DFT[i])>0.65:  #we use this condition because when we got close to 0 then it give error like dividing by 0
        division_values.append(Y[i]/H_DFT[i])
    else:
        division_values.append(Y[i]/1.015)   #there we divide it by 1.015 , we can also choose any other no. also

#print and plotting division_values
print(division_values)                                              #print the division_values
plt.plot(division_values)                                           #ploting the graph
plt.title('DIVISION OF DFT OF Y AND H')                             #set title for graph
plt.show()

#Now , we come to our first result that the singal is 'first denoise and then deblur'
plt.plot(x_n, '-k', label='X[n]')                                   #plotting original signal
plt.plot(idft(division_values), '-r', label='X1[n]')                #plotting idft(division_values) which is basically our desired signal X1[n]
plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)   #this commond make a box for for labels of x_n and x1n

plt.title('DENOISE THEN DEBLUR SIGNAL COMPARISON')                  #set title
plt.xlabel("Time")                                                  #label x-axis
plt.ylabel("Temperature")                                           #label y-axis
plt.show()

#Now , we come to our second result that the singal is first deblur and then denoise

y_DFT1=DFT(y_n)                                                     #calling fucntion DFT for signal y[n]
idft_DFT_y=idft(y_DFT1)                                             #calling function idft for y_DFT1
final_signal2=filter(idft_DFT_y)                                    #calling function filter for idft_DFT_y


plt.plot(x_n, '-k', label='X[n]')                                   #plotting orignial signal
plt.plot(final_signal2, '-c', label='X2[n]')                        #plotting idft of filtered signal , so this is our second case result X2[n]
plt.legend(fancybox=True, framealpha=1, shadow=True, borderpad=1)

plt.title('DEBLUR THEN DENOISE SIGNAL COMPARISON')
plt.xlabel("Time")
plt.ylabel("Temperature")
plt.show()


#Final comparison of x1[n] and x2[n] by using MSE
MSE_yn = np.square(np.subtract(x_n, y_n)).mean()                    #MSE of distorted signal y[n] w.r.t x[n]
MSE_x1 = np.square(np.subtract(x_n, idft(division_values))).mean()  #MSE of x1[n] w.r.t x[n]
MSE_x2 = np.square(np.subtract(x_n, final_signal2)).mean()          #MSE of x2[n] w.r.t x[n]

print('MSE of y :-', MSE_yn)                                        #printing the MSE for y
print('MSE of x1 :-', MSE_x1)                                       #printing the MSE for x1
print('MSE of x2 :-', MSE_x2)                                       #printing the MSE for x2