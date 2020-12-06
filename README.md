# GameStatPlotter
## Tool to visualize the data from your card games

### Directory Structure
Save your data in an csv. 
The direcotry structure is as follows.
In the 'data' directory you create a directory for your game.
In this directory you create a directory, which is called 'raw'.
In there you can store the .csv. I would suggest to name the csv, the date on which you played the game.
The format should then be '%d-%m-%Y'.

This is structue is shown with the example.csv.example

In this file you can also see, how the csv file has to be setup.

### Running the plotter
You run the programm with the command 

```bash
python3 main.py
```

You can add the following parameters:
* "-g=\<game\>", where game is the directory of the name you want to plot
* "-c", Counts the non zero entries
* "-d=\<date\>", with specifing the name (here the date) of the csv you can only plot a single file

### Differences between plotting all and one file
Plotting all files usually takes the last entry in the list.

When plotting a single file it shows by default all values as a graph.

### Note
As I am german, for now it is parsing the entries in the csv with the german words. Keep this in mind. I will change this later.   

