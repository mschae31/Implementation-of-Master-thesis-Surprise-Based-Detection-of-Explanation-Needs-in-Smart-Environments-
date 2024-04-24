import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.patches import Patch, Rectangle
import math
from scipy import special


#Read event file
with open("input_output.txt", "r") as file:
    lines = file.read().splitlines()
    event_list = []
    timestamp_list = []
    time_passed_list = []
    input_list = []
    output_list = []
    
    for line in lines:
        parts = line.split(';')

        logs = parts[0].strip()   # event string
        timestamp = parts[1].strip()   
        time_passed = parts[2].strip() 

        event_list.append(logs)
        timestamp_list.append(timestamp)
        time_passed_list.append(time_passed)

    input_list = [s.split('_')[0][1:] for s in event_list]
    output_list = [s.split('_')[1][:-1] for s in event_list]

#Timekeeping
start = time.time()


# Function for computing the Surprise Value
def Macedo(p,index):
    term= math.log2(1+max(0,max(p)-p[index])) #first max avoids returning -0.0 in some cases
    return term

# Function for computing Gaussian surprise
def gaussian_surprise(parameter,x_i):
    [kappa1, mu1, nu1, s1, kappa2, mu2, nu2, s2] = parameter
    c=1   
    surprise_term1 = 0.5 * np.log(kappa1 / kappa2 )
    surprise_term2 = (kappa2/(4*kappa1)) * ((x_i-mu1)/(kappa2*s1))**2
    surprise_term3 = np.log(c)
    surprise_term4 = (-1/2)*(special.digamma(nu1/2)+np.log(2/(nu1*(s1)**2)))
    surprise_term5 = ((kappa1/kappa2)*(x_i-mu1)**2)/(2*(s1)**2)
    surprise = surprise_term1 + surprise_term2 + surprise_term3 + surprise_term4 + surprise_term5
    return surprise



inputs_seen = []
outputs_seen = []
alpha = {}

# Variables for Plots
plot = np.zeros(int(timestamp_list[-1])+1)
plot2 = []
plot3 = []
plot_time = []
events = []

time_surprise_indices = []

threshold = 0.9 #subject dependent
count = 0
paramaters_gaussian = {}
first_time = False

last_event = ""

for i in range(len(input_list)):

    if(last_event == '{},{}'.format(input_list[i], output_list[i]) and
       input_list[i].startswith("Waiting for")):
         continue
    last_event = '{},{}'.format(input_list[i], output_list[i])

    first_time = False

    if input_list[i] not in inputs_seen:
        inputs_seen.append(input_list[i])
        alpha[input_list[i]] = {}
        alpha[input_list[i]]["a"] = np.zeros(25, dtype="int64")
        alpha[input_list[i]]["b"] = np.zeros(25, dtype="int64")
        alpha[input_list[i]]["p"] = np.zeros(25)  #gets computed in each iteration
        alpha[input_list[i]]["sum_alpha"]= sum(alpha[input_list[i]]["a"])
        alpha[input_list[i]]["p"] = np.zeros(25)
        first_time = True
    
    if output_list[i] not in outputs_seen:
        outputs_seen.append(output_list[i])

    index = outputs_seen.index(output_list[i])    
    a = alpha[input_list[i]]["a"]
    b = alpha[input_list[i]]["b"]
    p = alpha[input_list[i]]["p"]
    sum_alpha = alpha[input_list[i]]["sum_alpha"]
    

    surprise = Macedo(p,index)
    
    b[index] += 1   # Posterior
    sum_alpha += 1     # Sum of alpha of b (posterior)

    #exponential smoothing:
    b = 0.8*b
    b[index] += 0.2*sum_alpha
    p = b/sum_alpha

                  
    #Exemplary Code for Gausiian surprise: Compute the amount of surprise because of the time
    if time_passed_list[i] != "x":
        x_i = int(time_passed_list[i])
        if '{},{}'.format(input_list[i], output_list[i]) in paramaters_gaussian:
            [kappa1, mu1, nu1, s1, kappa2, mu2, nu2, s2] = paramaters_gaussian['{},{}'.format(input_list[i], output_list[i])]
            kappa2 = kappa1 + 1
            mu2 = (kappa1/kappa2)*mu1+(1/kappa2)*x_i
            nu2 = nu1 + 1
            s2 = math.sqrt((nu1*(s1)**2+(kappa1/kappa2)*(x_i-mu1)**2)/nu2)
            time_surprise = gaussian_surprise([kappa1, mu1, nu1, s1, kappa2, mu2, nu2, s2],x_i)

            plot_time[events.index('{},{}'.format(input_list[i], output_list[i]))].append(int(time_passed_list[i])) 

        else:
             [kappa1, mu1, nu1, s1, kappa2, mu2, nu2, s2] = [2,x_i,2,2,2,x_i,2,2] #kappa,mu,nu,s
             time_surprise = 0

             plot_time.append([int(time_passed_list[i])])
             events.append('{},{}'.format(input_list[i], output_list[i]))
    
        if time_surprise>1: # 1 is a chosen threshold
            time_surprise_indices.append([events.index('{},{}'.format(input_list[i], output_list[i])),
                                          len(plot_time[events.index('{},{}'.format(input_list[i], output_list[i]))])-1])
            
            print("Time surprise! At time "+ str(timestamp_list[i]) + 
                ", we have event " + str(event_list[i]) + " with time surprise " +
                str(time_surprise)+ " and time " + time_passed_list[i] + " with usual time of " + str(mu1))
        
         
    
    # If it is the first time the user gives a certain input, it should be surprising
    if first_time:
         plot2.append(event_list[i])
         plot3.append("surprising")
    
    #Print Surprise event in console
    if(surprise> threshold):
        print("This was surprising! At time "+ str(timestamp_list[i]) + 
            ", we have event " + str(event_list[i]) + " with KL " +
            str(round(surprise,3)))
        count += 1
            
    #Save information for Plots:
    plot2.append(event_list[i])

    if surprise > (0.99):
            plot3.append("very surprising")
    elif surprise > (0.95):
            plot3.append("surprising")
    elif surprise > (0.9): 
            plot3.append("slightly surprising")
    else:
         plot3.append("not surprising")
     
    
    plot[int(timestamp_list[i])] = round(surprise,3)


    #Update parameters for next iteration

    # Posterior is the prior in the next iteration
    a = b 

    alpha[input_list[i]]["a"] = a
    alpha[input_list[i]]["b"] = b
    alpha[input_list[i]]["p"] = p
    alpha[input_list[i]]["sum_alpha"] = sum_alpha

    
    if time_passed_list[i] != "x":
        kappa1 = kappa2
        mu1 = mu2
        nu1 = nu2
        s1 = s2
        paramaters_gaussian['{},{}'.format(input_list[i], output_list[i])] = [kappa1, mu1, nu1, s1, kappa2, mu2, nu2, s2]
    
end = time.time()

#PLOTS:

plt.figure(figsize=(12, 8))
plt.plot(plot, label='Amount of Surprise',linewidth =0.5)
plt.axhline(y=threshold, color='r', linestyle='--', label='Threshold')
plt.xlabel('Iteration')
plt.ylabel('KL divergence')
plt.title('Surprise Value for all events')
plt.legend()
plt.show()

df = pd.DataFrame({'plot2': plot2, 'plot3': plot3})
df['Event_Index'] = df.groupby('plot2').cumcount() + 1 

# Only plot the first 20 occurrences
df_first_20 = df[df['Event_Index'] <= 20]

sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))

desired_order = ['very surprising', 'surprising', 'slightly surprising', 'not surprising']
unique_plot3_values = np.unique(desired_order)
colors = [
    "grey" if value == "not surprising" else sns.color_palette("YlOrRd", n_colors=len(unique_plot3_values))[i]
    for i, value in enumerate(unique_plot3_values)
]
legend_elements = []

for i, cat in enumerate(df_first_20['plot2'].unique()):
    subset = df_first_20[df_first_20['plot2'] == cat]

    for j in range(20):
        values = subset[subset['Event_Index'] == j + 1]['plot3'].value_counts()
        for k, att in enumerate(unique_plot3_values):
            count = values.get(att, 0)
            plt.bar(i, count, bottom=j, color=colors[np.where(unique_plot3_values == att)[0][0]])

for l in range(0, len(unique_plot3_values)):
    legend_elements.append(Patch(color=colors[l], label=unique_plot3_values[l]))
plt.legend(handles = legend_elements,title='Surprise categories', bbox_to_anchor=(1, 1), loc='upper left')

plt.xticks(np.arange(len(df_first_20['plot2'].unique())) + 0.2, df_first_20['plot2'].unique(), rotation='vertical', fontsize=8)
plt.xlabel('Events', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title('How surprising was each event in each of its first 20 occurrences', fontsize=14)

plt.tight_layout()
plt.show()

max_length = max(len(row) for row in plot_time)
#max_length = 30   # If too many events are considered
plot_time = [row[:max_length] for row in plot_time]
df = pd.DataFrame(plot_time, index=events, columns=list(range(1, max_length + 1))
)

plt.figure(figsize=(12, 8))
heatmap = sns.heatmap(df, cmap='Blues', annot=True, cbar_kws={'label': 'time between input and output'},
            linewidths=1, linecolor='white',
            vmin=0, vmax=7, xticklabels=False)

heatmap.tick_params(axis='y', labelsize=8)
ytick_labels = [label.get_text()[:50] + '...' if len(label.get_text()) > 50 else label.get_text() for label in heatmap.yaxis.get_ticklabels()]
heatmap.set_yticklabels(ytick_labels)

plt.subplots_adjust(left=0.3)
plt.subplots_adjust(right=1)


for row, col in time_surprise_indices:
    plt.gca().add_patch(Rectangle((col, row), 1, 1, fill=False, edgecolor='red', lw=2))

plt.subplots_adjust(right=1)
plt.title('Heatmap: Time between input and output')
plt.xlabel('Occurrence')
plt.ylabel('Event')
plt.show()


time = end - start
print(f'The execution time is {time}s')