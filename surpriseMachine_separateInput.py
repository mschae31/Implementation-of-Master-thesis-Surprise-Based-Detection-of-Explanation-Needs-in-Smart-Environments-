import numpy as np
from scipy.stats import dirichlet
from scipy.special import gamma
from scipy import special
import time
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import pandas as pd
from matplotlib.patches import Patch

with open("input_output.txt", "r") as file:
    lines = file.read().splitlines()
    event_list = []
    timestamp_list = []
    input_list = []
    output_list = []
    
    for line in lines:
        parts = line.split(';')

        logs = parts[0].strip()
        timestamp = parts[1].strip()

        event_list.append(logs)
        timestamp_list.append(timestamp)

    input_list = [s.split('_')[0][1:] for s in event_list]
    output_list = [s.split('_')[1][:-1] for s in event_list]

start = time.time()

# Function for compution the Kullback-Leibler divergence
def KL_dirichlet(alpha1, alpha2, index, sum_alpha):
    term1 = np.log(1/(sum_alpha-1))
    term2 = (np.log(alpha2[index]-1)
        -1*(special.digamma(alpha1[index]) - special.digamma(sum_alpha-1))
        )  
    return term1 + term2


inputs_seen = []
outputs_seen = []
alpha = {}
plot = []
plot2 = []
plot3 = []
threshold = 0.51

for i in range(len(input_list)):

    if input_list[i] not in inputs_seen:
        inputs_seen.append(input_list[i])
        alpha[input_list[i]] = {}
        alpha[input_list[i]]["a"] = np.ones(20, dtype="int64")
        alpha[input_list[i]]["b"] = np.ones(20, dtype="int64")
        #for j in range(len(alpha[input_list[i]]["a"])-10,len(alpha[input_list[i]]["a"])):
        #    alpha[input_list[i]]["a"][j]=1
        #    alpha[input_list[i]]["b"][j]=1
        alpha[input_list[i]]["sum_alpha"]= sum(alpha[input_list[i]]["a"])
    
    if output_list[i] not in outputs_seen:
        outputs_seen.append(output_list[i])

    index = outputs_seen.index(output_list[i])     
    a = alpha[input_list[i]]["a"]
    b = alpha[input_list[i]]["b"]
    sum_alpha = alpha[input_list[i]]["sum_alpha"]


    if(b[index]==0):
        b[index] += 2
        sum_alpha += 2
        a[index] += 1
    else:
        b[index] += 1   # Posterior
        sum_alpha += 1     # Sum of alpha of b (posterior)

 
    # Check if it was surprising, but only if not already seen 15 times
    if b[index] < 15:  #does not rly shorten the runtime
        if(KL_dirichlet(a,b,index,sum_alpha)> threshold/a[index]):
            print("This was surprising! At time "+ str(timestamp_list[i]) + 
                ", we have event " + str(event_list[i]) + " with KL " +
                str(round(KL_dirichlet(a,b,index,sum_alpha)*a[index],3)))
        plot2.append(event_list[i])
        if KL_dirichlet(a,b,index,sum_alpha)>(threshold/a[index]+0.05):
                plot3.append("very surprising")
        elif KL_dirichlet(a,b,index,sum_alpha)>(threshold/a[index]+0.02):
                plot3.append("surprising")
        elif KL_dirichlet(a,b,index,sum_alpha)>threshold/a[index]:
                plot3.append("slightly surprising")
        else:
             plot3.append("not surprising")


    """if i<30:
        print("This was surprising! At time "+ str(timestamp_list[i]) + 
                ", we have event " + str(event_list[i]) + " with KL " +
                str(round(KL_dirichlet(a,b,index,sum_alpha)*a[index],10))) """
     
    result = round(KL_dirichlet(a,b,index,sum_alpha)*a[index],3)

    plot.append(result)

    
    #Print when coffeemachine fail occurs to check if it was detected as surprising 
    """if(data[i]==("Waiting,Stopping")):
        print("Fail! At time "+ str(i+1) + ", we have event " + 
              str(data[i]) + " with KL " + str(round(KL_dirichlet(a,b,index,sum_alpha)*a[index],3))

        # When choosing alternatives as distance measures the probability will be important:
        print("Probability of event is " + str(b[index]/sum_alpha)) """  

    # Posterior is the prior in the next iteration
    a[index] += 1 

    alpha[input_list[i]]["a"] = a
    alpha[input_list[i]]["b"] = b
    alpha[input_list[i]]["sum_alpha"] = sum_alpha
    

#print(alpha["Switching power on,Pressing the button to start Coffeemachine"]["a"][:15])
#print(alpha)
indices = [index for index, value in enumerate(plot2) if value == "(._Mixer makes a sound)"]

plt.plot(plot, label='Amount of Surprise')
plt.axhline(y=threshold, color='r', linestyle='--', label='threshold')
plt.xlabel('Iteration')
plt.ylabel('KL divergence')
plt.title('Amount of Surprise for all events')
plt.legend()
plt.show()


df = pd.DataFrame({'plot2': plot2, 'plot3': plot3})
categories_counts = Counter(plot2)

stacked_data = pd.DataFrame()
for cat in categories_counts:
    temp_df = df[df['plot2'] == cat]['plot3'].value_counts().reset_index()
    temp_df.columns = ['plot3', 'count']
    temp_df['plot2'] = cat
    stacked_data = pd.concat([stacked_data, temp_df])

stacked_data.sort_values(by=['plot2', 'plot3'], inplace=True)

sns.set(style="whitegrid")
plt.figure(figsize=(12, 8))

unique_plot3_values = df['plot3'].unique()
colors = sns.color_palette('Set2', n_colors=len(unique_plot3_values))

bottoms = {}
legend_elements = []

for j, att in enumerate(unique_plot3_values):
    for i, cat in enumerate(categories_counts):
        subset = stacked_data[(stacked_data['plot2'] == cat) & (stacked_data['plot3'] == att)]
        values = subset['count'].tolist()
        if values:
            plt.barh(cat, values[0], left=bottoms.get(cat, 0), color=colors[j])
            bottoms[cat] = bottoms.get(cat, 0) + values[0]

    legend_elements.append(Patch(color=colors[j % len(colors)], label=att))

plt.legend(handles=legend_elements, title='Surprise categories')
plt.xlabel('Count')
plt.ylabel('Events')
plt.title('How surprising was each event in each of its first 13 occurrences')

plt.tight_layout()
plt.show()

end = time.time()
time = end - start

#print(f'The execution time is {time}s')