"""
Data logger and live plotting code for dice rolling experiment.
Enter the number of dice used and the number of rolls you want to
perform to begin. The inputs are:

d --> Remove the last entry
sequence of numbers denoting roll results (e.g. 124) --> log entry

Just copy-paste the final printed results into a text file for later analysis.
"""

import numpy as np
import matplotlib.pyplot as plt

def dice_experiment(N_dice, N_roll):
    Total = 0
    index = np.arange(N_dice, N_dice*6+1)
    bar_width = 0.6
    rolls = np.zeros(len(index))
    sequence = []
    i = 0
    while i < N_roll:
        plt.clf()
        entry = str(input("\nEnter result (e.g. 612): ")).replace(" ", "")
        if entry == "d" and i>1:
            last = sequence[-1]
            sequence.pop()
            Total -= last
            rolls[last-N_dice] -= 1
            i -= 1
            print("Total: ", Total, "\nIteration: ", i, "/", N_roll)
            plt.bar(index, rolls, bar_width,align='center')
            plt.xlabel('Rolls')
            plt.ylabel('Repeats')
            title = str('Dice rolls for '+ str(N_dice)+ "dices at "+ str(i)+ " rolls")
            plt.title(title)
            plt.grid("on")
            plt.draw()
            plt.pause(0.01)
        
        elif len(entry)==N_dice:
            result = 0
            valid = True
            for e in entry:
                result += int(e)
                if int(e) > 6:
                    valid = False
        
            if (int(result) >= N_dice) and (int(result) <= N_dice*6) and valid:
                Total += int(result)
                rolls[int(result)-N_dice] += 1
                sequence.append(int(result))
                i += 1
                print("Total: ", Total, "\nIteration: ", i, "/", N_roll)
                plt.bar(index, rolls, bar_width,align='center')
                plt.xlabel('Rolls')
                plt.ylabel('Repeats')
                title = str('Results for '+ str(N_dice)+ " dice after "+ str(i)+ " rolls")
                plt.title(title)
                plt.grid("on")
                plt.draw()
                plt.pause(0.01)
            
            else:
                print("Invalid input, enter again.")

        else:
            print("Invalid input, enter again.")
    print(index)
    print(rolls)

dice_experiment(2, 100)