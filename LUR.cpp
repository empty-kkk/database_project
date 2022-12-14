#include<stdio.h>
#include<iostream>
using namespace std;
#include <list>
#include <unordered_map>
class LRUCache
{
    list<std::pair< int, int> > _list;
    unordered_map< int, std::list<std::pair<int, int>>::iterator > _map;
    int capacity; 
public:
    LRUCache(unsigned int capacity):capacity(capacity)
    {
    }
    int get(int key);
    void put(int key, int value);
};

void LRUCache::put(int key, int value)
{
    auto iteramap = _map.find(key);
    if(iteramap != _map.end())
    {
        _list.erase(iteramap->second);
        _list.push_front(std::pair<int, int>(key, value));
        _map[key] = _list.begin();
    }
    else{
    if(_map.size() >= capacity)
    {
        _map.erase(_list.back().first);
        _list.pop_back(); 
    }
    _list.push_front(std::pair<int, int>(key, value));
    _map[key] = _list.begin();
    }   
}


int LRUCache::get(int key)
{
    auto iteramap = _map.find(key);
    if(iteramap == _map.end()){
        return -1;
    }
    _list.push_front(std::pair<int, int>(key,  iteramap->second->second));
    _list.erase(iteramap->second);
    _map[key] = _list.begin();
    return iteramap->second->second;
}