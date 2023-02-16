#include <vector>
#include <numeric>
#include <iostream>
#include <random>
#include <map>
#include <string>

class CounterItem{

};

class Counter
{
private:
    std::map<std::string, int> counter;
    std::string id;

public:
    Counter()
    {
        std::random_device rd;
        std::mt19937_64 gen(rd());
        std::uniform_int_distribution<uint64_t> dis;
        id = std::to_string(dis(gen));
    }

    void increment()
    {
        counter[id]++;
    }

    void merge(Counter *other)
    {
        for (auto const& [key, val] : other->counter)
        {
            this->counter[key] = std::max(this->counter[key], val);
        }
    }

    int GetCount()
    {
        int result = 0;
        for (auto const& [_, val] : counter)
        {
            result+=val;
        }
        
        return result;
    }
};