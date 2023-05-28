# SCProject. By: Abe & Alfredo

These environments have the purpose of completing the project assigned in the subject Computer Systems at ULA.

### Instructions

1. You need to have installed gym and python in your computer.
2. Install requirements.
3. Go to V0 / V1 folder.
4. Execute main file to solve the respectiv puzzle.
-----------------------------
## V0: The Pirate Ship
Version 0 of environment.

- Action Space = Discrete(4)
- Observation Space = Discrete(3.891.888)
- Import = gym.make("Pirate-Ship-v0")

### Description
The Pirate Ship consists of the adventure of a Pirate in saving his ship. She needs to move 2 boxes, one of them must be on a strategic location, and it will be on the coin symbol. But, there are bombs that will affect the life of the agent, and it will cause the ship to sink if the 2 bombs explode.

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
7 6 = Character position.
7 2 = Box #1.
5 3 = Box #2.
3 2 = Solution point.
4 4 = Bomb #1.
6 0 = Bomb #2.
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
The observation is a value that represents the current position of the agent (n_rows * n_cols), so there will be 81 positions that the character will have. The boxes will have 78 and 77 respectively, and the 2 bombs must be included along with the 4 directions.

In total there will be around **3.891.888** possible observations.

### Rewards
- -1 any move.
- -10 there is no movement, it stays in the same place.
- 0 if you have finished the game.
- -30 if a bomb has exploded.
- -100 if the second bomb has exploded.

### Arguments
gym.make("Pirate-Ship-v0")

### Video Demo
YouTube: https://youtu.be/qbmOHc5kCQQ

---

## V1: Bombermine Treasure
Version 1 of environment.

- Action Space = Discrete(4)
- Observation Space = Discrete(324)
- Import = gym.make("BomberMine-V1")

### Description
A prince is lost and wants to return to his castle, all he has are bombs to unlock it and reach the door of his castle.

**Map**:
```
9 9
S S S S S S S S S
S S S S S S S S S
S S S S S S S S S
S S S S S S S S S
S S S S S S S S S
S S S S S S S S S
S S S S S S I S S
S S S S S I I I S
S S S S S I I I S
7 6 = Character
3 2 = Goal
```
### Actions Agent
There are 5 discrete deterministic actions:
- 0: Move left.
- 1: Move down.
- 2: Move right.
- 3: Move up.
- 4: Put boom.
### Rewards
- -1 any move.
- -10 there is no movement, it stays in the same place.
- 0 if you have finished the game.
- -30 if a bomb has exploded.
- -100 if the second bomb has exploded.
