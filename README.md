# SCProject. By: Abe & Alfredo

These environments have the purpose of completing the project assigned in the subject Computer Systems at ULA.

### Intructions

1. You need to have installed gym and python in your computer.
2. Install requirements.
3. Go to V0 / V1 folder.
4. Execute main file to solve the respectiv puzzle.

## V0: The Pirate Ship
Version 0 of environment.

### Description
POR DEFINIR

**Map**:
```
S S S S S S S I S
S S I I I I I I S
S S I I S I S I S
S S I S S I S I S
S S S I I S I I S
S S S I I S S I S
I I I I I I I I S
S S I I I I S I S
S S S S S S S S S
```
### Actions Agent
There are 5 discrete deterministic actions:
- 0: Move left.
- 1: Move down.
- 2: Move right.
- 3: Move up.
- 4: Push box.
### Actions Push Box
There are 4 discrete deterministic actions:
- (0, -1): Left.
- (1, 0): Down.
- (0, 1): Right.
- (-1, 0): Up.
### Observations


### Rewards
- -1 any move.
- -10 there is no movement, it stays in the same place.
- 0 if you have finished the game.
- -30 if a bomb has exploded.
- -100 if the second bomb has exploded.

### Arguments
gym.make('Blocks-v0')

## V1
Version 1 of environment
