create table states (identity text, utility real);
create table reveal_transitions(start string, destination string, occurances string);
create table constants(learningCoefficient real, mineReward real, correctFlagReward real, incorrectFlagReward real, unknownFlagReward real, revealedReward real, unrevealedReward real, scope integer);
