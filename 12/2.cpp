#include <iostream>
#include <unordered_set>
#include <cstring>
#include <array>

int compare(int a, int b)
{
    return a < b ? 1 : a > b ? -1 : 0;
}

void applyGravity(std::array<int, 24> &state, int a, int b)
{
    int x = compare(state[a], state[b]);
    int y = compare(state[a + 1], state[b + 1]);
    int z = compare(state[a + 2], state[b + 2]);

    state[a + 3] += x;
    state[a + 4] += y;
    state[a + 5] += z;
    state[b + 3] -= x;
    state[b + 4] -= y;
    state[b + 5] -= z;
}

void move(std::array<int, 24> &state, int a)
{
    state[a + 0] += state[a + 3];
    state[a + 1] += state[a + 4];
    state[a + 2] += state[a + 5];
}

void processState(std::array<int, 24> &state)
{
    applyGravity(state, 0, 6);
    applyGravity(state, 0, 12);
    applyGravity(state, 0, 18);
    applyGravity(state, 6, 12);
    applyGravity(state, 6, 18);
    applyGravity(state, 12, 18);

    move(state, 0);
    move(state, 6);
    move(state, 12);
    move(state, 18);
}

namespace std
{
    template<typename T, size_t N>
    struct hash<array<T, N> >
    {
        typedef array<T, N> argument_type;
        typedef size_t result_type;

        result_type operator()(const argument_type& a) const
        {
            hash<T> hasher;
            result_type h = 0;
            for (result_type i = 0; i < N; ++i)
            {
                h = h * 31 + hasher(a[i]);
            }
            return h;
        }
    };
}

int main(int argc, char* argv[])
{
    std::array<int, 24> state;

    state[0] = -7;
    state[1] = 17; 
    state[2] = -11; 
    state[3] = 0;
    state[4] = 0; 
    state[5] = 0; 

    state[6] = 9;
    state[7] = 12; 
    state[8] = 5; 
    state[9] = 0;
    state[10] = 0; 
    state[11] = 0; 

    state[12] = -9;
    state[13] = 0; 
    state[14] = -4; 
    state[15] = 0;
    state[16] = 0; 
    state[17] = 0; 

    state[18] = 4;
    state[19] = 6; 
    state[20] = 0; 
    state[21] = 0;
    state[22] = 0; 
    state[23] = 0; 

    // <x=-1, y=0, z=2>
    // <x=2, y=-10, z=-7>
    // <x=4, y=-8, z=8>
    // <x=3, y=5, z=-1>

    // state[0] = -1;
    // state[1] = 0; 
    // state[2] = 2; 

    // state[6] = 2;
    // state[7] = -10; 
    // state[8] = -7; 

    // state[12] = 4;
    // state[13] = -8; 
    // state[14] = 8; 

    // state[18] = 3;
    // state[19] = 5; 
    // state[20] = -1; 

    std::unordered_set<std::array<int, 24>> states;

    for(unsigned long long i = 0; /*i < 1000000*/; ++i)
    {
        processState(state);
        // std::array<int, 24> stateCopy = state;

        if(states.find(state) != states.end())
        {
            std::cout << i << std::endl;
            break;
        }
        else if(i % 1000 == 0)
        {
            states.insert(state);
        }

        if(i % 500000 == 0)
        {
            std::cout << i << std::endl;
        }
    }

    for(int i = 0; i < 24; ++i)
    {
        std::cout << state[i] << std::endl;
    }
}