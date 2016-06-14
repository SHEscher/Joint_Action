import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D
# Info: http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html

from SA_Evolution import *
from JA_Evolution import *

'''
TODO:
    - Behaviour compare with paper
    - analysis of strategy.
    - analysis William Beer 2015 (p.8)
    - Attractor space
    - Statistic for meaningful difference between sound off/on (run evolution n-times, for x-Generations)

GRAPHS:
1) GRAPH A:
 - Position Target and Tracker (y-axis), time (x-axis)
'''

# Setup Agent(s) to analyse:
condition = single_or_joint_request()
audicon = audio_condition_request()

load = load_request()

if load is False:
    filename = filename_request(condition)  # "joint" or "single"
    # filename = "Gen1001-2000.popsize55.mut0.02.sound_cond=False.JA.joint(Fitness6.1)"

    if condition == "single":
        sa = SA_Evolution(auditory_condition=audicon)
        if isinstance(filename, str):
           sa_performance = sa.reimplement_population(filename=filename, Plot=True)
           sa_performance = np.array(sa_performance, dtype=object)
           fitness = np.round(sa.pop_list[0, 1],2)
           np.save("./Analysis/single/sa_performance_cond{}_fitness{}".format(sa.condition, fitness), sa_performance)
           # sa_performance[0-3] are the different trials
           # sa_performance[0-3][0-5] = fitness[0], trajectories[1], keypress[2], sounds[3], neural_state[4], neural_input_L[5]

    if condition == "joint":
        ja = JA_Evolution(auditory_condition=audicon, pop_size=55)
        if isinstance(filename, str):
            ja_performance = ja.reimplement_population(filename=filename, Plot=True)
            ja_performance = np.array(ja_performance, dtype=object)
            fitness = np.round(ja.pop_list_L[0,1],2)
            np.save("./Analysis/joint/ja_performance_cond{}_fitness{}".format(ja.condition, fitness), ja_performance)
            # ja_performance[0-3] are the different trials
            # ja_performance[0-3][0-7] = fitness[0], trajectories[1], keypress[2], sounds[3], neural_state_L[4], neural_state_R[5], neural_input_R[6], neural_input_L[7]


# len(sa_performance)
# sa_performance[1][0] # Fitness for particular speed+direction trial
if load is True:
    if condition == "single":
        sa_performance = load_file(condition, audicon)
        print(">> File is loaded in sa_performance")
        fitness = np.round(np.mean([i[0] for i in sa_performance]),2) # Fitness over all trials
    if condition == "joint":
        ja_performance = load_file(condition, audicon)
        print(">> File is loaded in ja_performance")
        fitness = np.round(np.mean([i[0] for i in ja_performance]),2) # Fitness over all trials


## Split in different Trials:
sl = sa_performance[0] if condition == "single" else ja_performance[0] # speed: slow, initial target-direction: left
sr = sa_performance[1] if condition == "single" else ja_performance[1] # speed: slow, initial target-direction: right
fl = sa_performance[2] if condition == "single" else ja_performance[2] # speed: fast, initial target-direction: left
fr = sa_performance[3] if condition == "single" else ja_performance[3] # speed: fast, initial target-direction: right

trials = [sl, sr, fl, fr]
trial_names = ["slowleft", "slowright", "fastleft", "fastright"]
index = -1

folder = "./Analysis/graphs/{}_{}_{}".format(condition, audicon, fitness)
if not os.path.exists(folder):
    os.mkdir(folder)

## Colours:
# http://matplotlib.org/examples/color/colormaps_reference.html
# cmap = plt.get_cmap("Paired")

col = ["royalblue", "tomato", "palegreen", "fuchsia", "gold", "darkviolet", "darkslategray", "orange"] # colors.cnames

# for i in range(8):
#     plt.plot(2*i,1, marker="o", c=col[i])
#     plt.xlim(-1,15)


# trial = trials[0]

for trial in trials:

    index += 1
    trial_name = trial_names[index]

    # Create Folder
    current_folder = "{}/{}".format(folder, trial_name)
    if not os.path.exists(current_folder):
        os.mkdir(current_folder)

    ## GRAPH A:
    tracker = trial[1][:,0] # trajectories[1], tracker: tracs[:,0]
    target  = trial[1][:,1] # trajectories[1], target:  tracs[:,1]

    fig_a = plt.figure("GRAPH A, Trial {}".format(trial_name))
    plt.ylim(-20.5, 20.5)
    plt.plot(tracker,'r', markersize=12, alpha=0.5, label="Tracker")
    plt.plot(target, 'g', label="Target")
    plt.legend()
    # plt.title("Target and Tracker Positions")
    plt.xlabel("Timesteps")
    plt.ylabel("Position")

    plt.savefig("./{}/{} GRAPH A (POSITIONS) Trial {}".format(current_folder, condition, trial_name))
    plt.close(fig_a)

    ## GRAPH B:
    # Single: neural_state[4]
    # Single: neural_input_L[5]
    # trial[4].shape
    # trial[5].shape
    if condition == "single":
        neural_state = trial[4]  # knoblin.Y
        neural_input = trial[5]  # knoblin.I

    # Joint:  neural_state_L[4], neural_state_R[5]
    # Joint:  neural_input_L[6], neural_input_R[7]
    if condition == "joint":
        neural_state_L = trial[4]
        neural_state_R = trial[5]
        neural_input_L = trial[6]
        neural_input_R = trial[7]

    # Info: http://matplotlib.org/mpl_toolkits/mplot3d/tutorial.html
    fig_b = plt.figure("GRAPH B, Trial {}".format(trial_name))
    ax = fig_b.add_subplot(111, projection='3d')
    if condition == "single":
        for i in range(neural_state.shape[1]):
            ax.plot(xs = range(neural_state.shape[0]), zs = neural_state[:,i], ys=np.repeat(i+1,neural_state.shape[0]))
            ax.plot(xs = range(neural_input.shape[0]), zs = neural_input[:,i], ys=np.repeat(i+1,neural_state.shape[0]),
                    alpha=0.0)

    if condition == "joint":
        for i in range(neural_state_L.shape[1]):
            ax.plot(xs=range(len(neural_state_L)), zs=neural_state_L[:, i], ys=np.repeat(i + 1, len(neural_state_L)),
                    # ls="-.",
                    alpha = .5,
                    c=col[i]) # c=cmap(i**3))
            ax.plot(xs=range(len(neural_state_R)), zs=neural_state_R[:, i], ys=np.repeat(i + 1, len(neural_state_R)),
                    c=col[i]) # c=cmap(i**3))

            ax.plot(xs=range(len(neural_state_L)), zs=neural_input_L[:, i], ys=np.repeat(i + 1, len(neural_state_L)),
                    alpha=0.0)
            ax.plot(xs=range(len(neural_state_R)), zs=neural_input_R[:, i], ys=np.repeat(i + 1, len(neural_state_R)),
                    alpha=0.0)

    # ax.set_title("Neural activation through trial")
    ax.set_xlabel('Timesteps')
    ax.set_ylabel('Neurons')
    ax.set_zlabel('Activation')
    plt.savefig("./{}/{} GRAPH B (Neural Activity) Trial {}".format(current_folder, condition, trial_name))
    plt.close(fig_b)


    fig_b_b = plt.figure("GRAPH B_b, Trial {}".format(trial_name))
    ax = fig_b_b.add_subplot(111, projection='3d')

    if condition=="join":
        for i in range(neural_input_L.shape[1]):
            # ax.plot(xs = range(neural_state.shape[0]), zs = neural_state[:,i], ys=np.repeat(i+1,neural_state.shape[0]),
            #         alpha=0.1)
            ax.plot(xs = range(len(neural_input_L)), zs = neural_input_L[:,i], ys=np.repeat(i+1, len(neural_input_L)),
                    # ls="-.",
                    alpha=.5,
                    c=col[i])   # c=cmap(i**3))

            ax.plot(xs=range(len(neural_input_R)), zs=neural_input_R[:, i], ys=np.repeat(i + 1, len(neural_input_R)),
                    c=col[i])  # c=cmap(i**3))

    if condition=="single":
        for i in range(neural_input.shape[1]):
            # ax.plot(xs = range(neural_state.shape[0]), zs = neural_state[:,i], ys=np.repeat(i+1,neural_state.shape[0]),
            #         alpha=0.1)
            ax.plot(xs=range(len(neural_input)), zs=neural_input[:, i], ys=np.repeat(i + 1, len(neural_input)),
                    # ls="-.",
                    c=col[i])  # c=cmap(i**3))


    ax.set_title("Neural Input")
    ax.set_xlabel('Timesteps')
    ax.set_ylabel('Neurons')
    ax.set_zlabel('weighted Input')
    plt.savefig("./{}/{} GRAPH B_b (Neural Activity) Trial {}".format(current_folder, condition, trial_name))
    plt.close(fig_b_b)


    # TODO: Maybe Wireframe:
    # fig_b_c = plt.figure("GRAPH B, Trial {}".format(trial_name))
    # ax = fig_b_c.add_subplot(111, projection='3d')
    # for i in range(neural_state.shape[1]):
    #     ax.plot_wireframe(X = range(neural_state.shape[0]), Z = neural_state[:,i], Y=i+1)
    # # plt.plot(neural_input, alpha=0.3)
    # plt.savefig("./{}/{} GRAPH B_C (Neural Activity) WIRE Trial {}  [WiP]".format(current_folder, condition, trial_name))
    # plt.close(fig_b_c)


    # TODO: Contour plots
    # fig_b_d = plt.figure("GRAPH B_b, Trial {}".format(trial_name))
    # ax = fig_b_d.add_subplot(111, projection='3d')
    # for i in range(neural_state.shape[1]):
    #     ax.counter(X = range(neural_state.shape[0]), Z = neural_state[:,i], Y=i+1, alpha=0.3)
    #     ax.counter(X = range(neural_input.shape[0]), Z = neural_input[:,i], Y=i+1)
    # plt.savefig("./graphs/{} GRAPH B_b (Neural Activity) Trial {}  [WiP]".format(current_folder, condition, trial_name))
    # plt.close(fig_b_d)


    ## GRAPH C:
    # keypress[2], sounds[3]
    fig_c = plt.figure("GRAPH C, Trial {}".format(trial_name))
    plt.xlim(0, len(trial[2]))
    plt.ylim(2, -2)
    plt.xlabel("Timesteps")
    plt.ylabel("Keypress")
    plt.yticks([-1,1],["left", "right"])


    for i in range(len(trial[3])):
        if trial[3][i, 0] == 1:  # sound left
            plt.plot(i, trial[3][i, 0]-2, 'yo', markersize=16, alpha=0.05, lw=0)

        if trial[3][i, 1] == 1:  # sound right
            plt.plot(i, trial[3][i, 1], 'yo', markersize=16, alpha=0.05, lw=0)


    for i in range(len(trial[2])):
        if trial[2][i,0] == -1: # keypress left
            plt.plot(i, trial[2][i, 0], 'bs', markersize=8)

        if trial[2][i, 1] == 1:  # keypress right
            plt.plot(i, trial[2][i, 1], 'bs', markersize=8)

    plt.savefig("./{}/{} GRAPH C (Keypress and Sound) Trial {}".format(current_folder, condition, trial_name))
    plt.close(fig_c)


    ## GRAPH D:
    # keypress[2]
    # tracker = trial[1][:,0] # trajectories[1], tracker: tracs[:,0]
    # target  = trial[1][:,1] # trajectories[1], target:  tracs[:,1]

    # for negative change of target position (left movement)
    fig_d_neg = plt.figure("GRAPH D delta-, Trial {}".format(trial_name))

    # Define boarders
    plt.xlim(-20.5, 20.5)
    plt.ylim(-20.5, 20.5)

    # Label Axes, Title
    plt.title("$\delta- position \ of \ Target$")
    plt.xlabel("Position Target")
    plt.ylabel("Position Tracker")


    for row in range(len(trial[2])):
        if target[row] < target[row-1]: # check whether left movement
            if row%20 == 0:
                plt.plot(target[row], tracker[row], marker="o", alpha=.4, lw=0, c="blue", ms=.4)

            if trial[2][row, 0] == -1:     # left
                    plt.plot(target[row], tracker[row], marker=r"$ {} $".format("L"), markersize=10, markerfacecolor="blue")
            if trial[2][row, 1] == 1:      # right
                    plt.plot(target[row], tracker[row], marker=r"$ {} $".format("R"), ms=10, mfc="red")

    plt.savefig("./{}/{} GRAPH D delta- (Keypress and Trajectories) Trial {}".format(current_folder,
                                                                                     condition,
                                                                                     trial_name))

    # for positive change of target position (right movement)
    fig_d_pos = plt.figure("GRAPH D delta+, Trial {}".format(trial_name))

    # Define boarders
    plt.xlim(-20.5, 20.5)
    plt.ylim(-20.5, 20.5)

    # Label Axes, Title
    plt.title("$\delta+ position \ of \ Target$")
    plt.xlabel("Position Target")
    plt.ylabel("Position Tracker")

    for row in range(len(trial[2])):
        if target[row] > target[row - 1]:  # check whether right movement
            if row%20==0:
                plt.plot(target[row], tracker[row], marker="o", alpha=.4, lw=0, c="blue", ms=.4)

            if trial[2][row, 0] == -1:     # left
                    plt.plot(target[row], tracker[row], marker=r"$ {} $".format("L"), markersize=10, markerfacecolor="blue")
            if trial[2][row, 1] == 1:      # right
                    plt.plot(target[row], tracker[row], marker=r"$ {} $".format("R"), ms=10, mfc="red")

    plt.savefig("./{}/{} GRAPH D delta+ (Keypress and Trajectories) Trial {}".format(current_folder, condition, trial_name))

    plt.close(fig_d_neg)
    plt.close(fig_d_pos)


    ## GRAPH E:
    # # neural_state[4]
    # trial[4].shape  # knoblin.Y
    # neural_state = trial[4]
    #
    # # neural_input_L[5]
    # trial[5].shape  # knoblin.I
    # neural_input = trial[5]


    # Plot Input-receptor Neuron 1, and output motor-neurons 4 & 6
    fig_e = plt.figure("GRAPH E, Trial {}".format(trial_name))
    ax = fig_e.add_subplot(111, projection='3d')

    # Label Axes, title
    ax.set_title("States of Input-receptor Neuron 1, and output motor-neurons 4 & 6")
    ax.set_xlabel('Neuron 4')
    ax.set_ylabel('Neuron 6')
    ax.set_zlabel('Neuron 1')

    # Plot
    if condition == "single":
        ax.plot(xs = neural_state[:,3], ys=neural_state[:,5], zs = neural_state[:,0], color="red")

    if condition == "joint":
        ax.plot(xs=neural_state_L[:, 3], ys=neural_state_L[:, 5], zs=neural_state_L[:, 0], color="red", label="Left Agent")
        ax.plot(xs=neural_state_R[:, 3], ys=neural_state_R[:, 5], zs=neural_state_R[:, 0], color="blue", label="Right Agent")
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0., fancybox=True)


    plt.savefig("./{}/{} GRAPH E (Neural Activity of Neuron 1,4,6) Trial {}".format(current_folder,
                                                                                    condition,
                                                                                    trial_name))
    plt.close(fig_e)


    # Plot average Neural-state and Trajectories (Target, Tracker)
    if condition == "single":
        average = [np.mean(i) for i in neural_state]

    if condition == "joint":
        average_L = [np.mean(l) for l in neural_state_L]
        average_R = [np.mean(r) for r in neural_state_R]


    fig_e_b = plt.figure("GRAPH E, Trial {}".format(trial_name))
    ax = fig_e_b.add_subplot(111, projection='3d')

    # axes limits
    ax.set_xlim(-20.5, 20.5)
    ax.set_ylim(-20.5, 20.5)

    # Label Axes, title
    ax.set_title('Network excitation')
    ax.set_xlabel('Target Position')
    ax.set_ylabel('Tracker Position')
    ax.set_zlabel('Average Neural State')

    # set color
    colorsMap = 'jet'
    cm = plt.get_cmap(colorsMap)
    if condition == "single":
        cNorm = matplotlib.colors.Normalize(vmin=min(average), vmax=max(average))
    if condition == "joint":
        cNorm = matplotlib.colors.Normalize(vmin=min(min(average_L), min(average_R)), vmax=max(max(average_L), max(average_R)))

    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)

    if condition == "single":
        ax.scatter(xs=target, ys=tracker, zs=average, c=scalarMap.to_rgba(average), lw=0, s=1.5)

    if condition == "joint":
        ax.scatter(xs=target, ys=tracker, zs=average_L, c="red" ,lw=0, s=1.5, label="Left Agent")    # c=scalarMap.to_rgba(average_L)
        ax.scatter(xs=target, ys=tracker, zs=average_R, c="blue" ,lw=0, s=1.5, label="Right Agent")  # c=scalarMap.to_rgba(average_R)
        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.,
                  fancybox=True, markerscale=3)



    # scalarMap.set_array(average)
    # fig_e_b.colorbar(scalarMap)

    plt.savefig("./{}/{} GRAPH E_b (Network excitation and trajectories) Trial {}".format(current_folder,
                                                                                          condition,
                                                                                          trial_name))
    plt.close(fig_e_b)




    # GRAPH F:
    fig_f = plt.figure("GRAPH F, Motor Neurons, Target-Tracker Distance Trial {}".format(trial_name))
    ax = fig_f.add_subplot(111, projection='3d')

    # axes limits
    ax.set_zlim(-20.5, 20.5)

    # Label Axes, title
    ax.set_xlabel('Neuron 4')
    ax.set_ylabel('Neuron 6')
    ax.set_zlabel('Distance Target-Tracker')

    # target-tracker: Distance
    # Plot
    if condition == "single":
        ax.plot(xs=neural_state[:, 3], ys=neural_state[:, 5], zs=target-tracker, color="darkviolet")

        for row in range(len(trial[2])):
            if trial[2][row, 0] == -1:  # left press
                ax.scatter(neural_state[row, 3], neural_state[row, 5], zs=(target-tracker)[row], marker=r"$ {} $".format("L"),
                         s=30, lw=0, c="blue")
            if trial[2][row, 1] == 1:   # right
                plt.scatter(neural_state[row, 3], neural_state[row, 5], zs=(target-tracker)[row],
                         marker=r"$ {} $".format("R"), s=30, lw=0, c="red")

    if condition == "joint":
        ax.plot(xs=neural_state_L[:, 3], ys=neural_state_L[:, 5], zs=target-tracker, color="royalblue",
                label="Left Agent")
        ax.plot(xs=neural_state_R[:, 3], ys=neural_state_R[:, 5], zs=target-tracker, color="fuchsia",
                label="Right Agent")

        for row in range(len(trial[2])):
            if trial[2][row, 0] == -1:  # left press
                ax.scatter(neural_state_L[row, 3], neural_state_L[row, 5], zs=(target - tracker)[row],
                           marker=r"$ {} $".format("L"),
                           s=30, lw=0, c="blue")
            if trial[2][row, 1] == 1:  # right
                plt.scatter(neural_state_R[row, 3], neural_state_R[row, 5], zs=(target - tracker)[row],
                            marker=r"$ {} $".format("R"), s=30, lw=0, c="red")

        ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0., fancybox=True)

    plt.savefig("./{}/{} GRAPH F (Motor Neuron Activity of Neuron 4,6 and Distance Target-Tracker) Trial {}".format(current_folder,
                                                                                    condition,
                                                                                    trial_name))

    plt.close(fig_f)

    ## GRAPH G:
    # TODO: Dynamical Graph (Neural state y, df/dy)

    # Y = []
    # for i in range(sa.simlength*2):
    #     Y.append(sa.knoblin.Y)
    #     sa.knoblin.next_state()
    #
    # meanY = [np.mean(i) for i in Y]
    #
    # for i in range(sa.simlength*2):
    #     for j in range(sa.knoblin.Y.shape[0]):
    #         plt.plot(i,Y[i][j], marker="o", markeredgewidth=0.0, ms=1)
    #
    # plt.plot(meanY)

    # DYDT = []
    # Y = np.matrix(np.zeros((len(sa.knoblin.Y),1)))
    # for i in np.arange(-20,21):
    #     tempY = np.matrix(np.zeros((len(sa.knoblin.Y),1)))
    #     tempY[0] = i
    #     Y = np.append(Y,tempY,1)
    #
    # for i in range(Y.shape[1]):
    #     O = sigmoid(np.multiply(sa.knoblin.G, Y[:,i] + sa.knoblin.Theta))
    #     DYDT.append(np.multiply(1 / sa.knoblin.Tau, - Y[:,i] + np.dot(sa.knoblin.W, O) + sa.knoblin.I) * sa.knoblin.h)
    #
    #
    # for i in range(len(DYDT)):
    #     for j in range(len(sa.knoblin.Y)):
    #         plt.plot(i, DYDT[i][j], marker="o", ms=5., markeredgewidth=0.0, c=col[j])










