# PRNG Prediction
We created a custom random number generator using XOR-Shift to help us generate pseudorandom numbers. THere may have been an issue with our initialization. Here are the first 5 generated values. Can you predict the next one?
http://prng-pred.aws.jerseyctf.com:5000/

## Solution
This is xor128shift+. The challenges version uses 3 particular shifts of `13 left`, `7 right` and `17 left`. I used z3 to create states that satisfy certain consecutive outputs and hence predict the origincal state. Then we can predict all the subsequent outputs! Remember to & 0xffffffff after each left shift else the number will grow beyong 32 bits!

## Flag
jctfv{Predictable_PRNG_Rizzed}