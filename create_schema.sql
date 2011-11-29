create table states (identity text, utility real);
create table reveal_transitions(start text, destination text, occurances text);
create table flag_history(identity text, correctFlags integer, incorrectFlags integer);
create table constants(learningCoefficient real, mineReward real, correctFlagReward real, incorrectFlagReward real, unknownFlagReward real, revealedReward real, unrevealedReward real, scope integer);
