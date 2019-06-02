"""Assess a betting strategy.

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Sebastian De la Paz
GT User ID: cdelpaz3
GT ID: 902770611
"""

import numpy as np
import matplotlib.pyplot as plt

def author():
    return 'cdelapaz3' # replace tb34 with your Georgia Tech username.

def gtid():
    return 902770611 # replace with your GT ID number

def get_spin_result(win_prob):
    result = False
    if np.random.random() <= win_prob:
            result = True
    return result

def test_code():
    np.random.seed(gtid()) # do this only once
    np.set_printoptions(suppress=True)

    experiment1()
    experiment2()


def experiment1():
    experiment(1, False)

def experiment2():
    experiment(3, True)


def experiment(exp, bankroll):
    # ---- A: Run simulation 10 times and plot all points for all 10 simulations
    if(exp == 1):
        reset_plot()
        for i in range(10):
            data,wround = martingale_simulation(bankroll)
            plt.plot(data, label='Simulation ' + str(i+1))

        title = 'Figure ' + str(exp)
        plt.legend(framealpha=1, frameon=False);
        plt.title(title)
        plt.savefig(title.replace(" ","") + '.png')


    #
    # ---- B:  Run simulation 1000 times and plot means for each spin
    #
    reset_plot()
    simulations = []
    wrounds = 0
    for i in range(1000):
        data, wround = martingale_simulation(bankroll)
        simulations.append(data)
        wrounds += wround


    extra_stats(simulations, wrounds)

    data =  np.vstack(simulations)
    means = data.mean(axis=0)
    stds = data.std(axis=0)
    mean_plus_std = means + stds
    mean_minus_std = means - stds

    plt.plot(means, label='Means')
    plt.plot(mean_plus_std, label='Means + STD')
    plt.plot(mean_minus_std, label='Means - STD')
    title = 'Figure ' + str(exp + 1)
    plt.title(title)
    plt.legend(framealpha=1, frameon=False);
    plt.savefig(title.replace(" ","") +'.png')

    #
    # --- C:  Plot medians
    #
    reset_plot()
    medians = np.median(data, axis=0)
    stds = data.std(axis=0)
    median_plus_std = medians + stds
    median_minus_std = medians - stds

    plt.plot(medians, label = 'Medians')
    plt.plot(median_plus_std, label = 'Medians + STD')
    plt.plot(median_minus_std, label = 'Medians - STD')
    title = 'Figure ' + str(exp + 2)
    plt.title(title)
    plt.legend(framealpha=1, frameon=False);
    plt.savefig(title.replace(" ","") +'.png')

def extra_stats(simulations, wrounds):
    N = float(len(simulations))
    wins = loses = 0
    total = 0

    for s in simulations:
        if s[-1] == 80:
            wins += 1
        elif s[-1] == -256:
            loses += 1
        total += s[-1]

    if False:
        print("Prob=" + str(wins/N) + ", Wins=" + str(wins) + ", Loses=" + str(loses))
        print("Spins=" + str(N) +", EV=" + str(total/N))
        print("Winning Spin = " + str(wrounds/N))


def reset_plot():
    plt.close()
    plt.xlim([0,300])
    plt.ylim([-256,100])

    plt.xlabel("Spin")
    plt.ylabel("Winnings")


def martingale_simulation(bankroll_enabled):
    win_prob = 0.4737
    target = 80
    num_spins = 1000
    bankroll = float("-inf") if not bankroll_enabled else -256

    earnings = 0
    spin = 0
    winnings = np.zeros(num_spins, dtype=int)
    wround = 0

    while spin < num_spins:
        if earnings >= target or earnings <= bankroll:
            spin += 1
            wround = spin if wround == 0 else wround
            if spin < num_spins:
                winnings[spin] = winnings[spin - 1]
            continue

        won = False
        bet_amount = 1
        while not won:
            spin += 1
            assert bet_amount > 0
            if get_spin_result(win_prob):
                earnings += bet_amount
                won = True
            else:
                earnings -= bet_amount
                bet_amount *=  2

                max_bet = abs(bankroll - earnings)
                bet_amount = min(max_bet, bet_amount) #Don't go over bankroll!

            assert earnings >= bankroll
            if spin < num_spins:
                winnings[spin] = earnings

            if earnings <= bankroll or earnings > target:
                break

    return winnings, wround


if __name__ == "__main__":
    test_code()
