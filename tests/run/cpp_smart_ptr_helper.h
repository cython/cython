class CountAllocDealloc {
  public:
      CountAllocDealloc(int* alloc_count, int* dealloc_count)
          : _alloc_count(alloc_count), _dealloc_count(dealloc_count) {
        (*_alloc_count)++;
      }
      ~CountAllocDealloc() {
        (*_dealloc_count)++;
      }
  private:
    int* _alloc_count;
    int* _dealloc_count;
};

template<typename T>
struct FreePtr {
  void operator()( T * t )
  {
    if(t != nullptr) {
      delete t;
      t=nullptr;
    }
  }
};
