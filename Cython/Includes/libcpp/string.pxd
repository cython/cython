
# deprecated cimport for backwards compatibility:
from libc.string cimport const_char

extern from "<string>" namespace "std::string" nogil:
    const usize npos

extern from "<string>" namespace "std" nogil:
    cdef cppclass string:
        ctypedef char value_type

        # these should really be allocator_type.size_type and
        # allocator_type.difference_type to be true to the C++ definition
        # but cython doesn't support deferred access on template arguments
        ctypedef usize size_type
        ctypedef ptrdiff_t difference_type

        cppclass const_iterator
        cppclass iterator:
            iterator() except +
            iterator(iterator&) except +
            value_type& operator*()
            iterator operator++()
            iterator operator--()
            iterator operator++(i32)
            iterator operator--(i32)
            iterator operator+(size_type)
            iterator operator-(size_type)
            difference_type operator-(iterator)
            difference_type operator-(const_iterator)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)
            bint operator<(iterator)
            bint operator<(const_iterator)
            bint operator>(iterator)
            bint operator>(const_iterator)
            bint operator<=(iterator)
            bint operator<=(const_iterator)
            bint operator>=(iterator)
            bint operator>=(const_iterator)
        cppclass const_iterator:
            const_iterator() except +
            const_iterator(iterator&) except +
            const_iterator(const_iterator&) except +
            operator=(iterator&) except +
            const value_type& operator*()
            const_iterator operator++()
            const_iterator operator--()
            const_iterator operator++(i32)
            const_iterator operator--(i32)
            const_iterator operator+(size_type)
            const_iterator operator-(size_type)
            difference_type operator-(iterator)
            difference_type operator-(const_iterator)
            bint operator==(iterator)
            bint operator==(const_iterator)
            bint operator!=(iterator)
            bint operator!=(const_iterator)
            bint operator<(iterator)
            bint operator<(const_iterator)
            bint operator>(iterator)
            bint operator>(const_iterator)
            bint operator<=(iterator)
            bint operator<=(const_iterator)
            bint operator>=(iterator)
            bint operator>=(const_iterator)

        cppclass const_reverse_iterator
        cppclass reverse_iterator:
            reverse_iterator() except +
            reverse_iterator(reverse_iterator&) except +
            value_type& operator*()
            reverse_iterator operator++()
            reverse_iterator operator--()
            reverse_iterator operator++(i32)
            reverse_iterator operator--(i32)
            reverse_iterator operator+(size_type)
            reverse_iterator operator-(size_type)
            difference_type operator-(iterator)
            difference_type operator-(const_iterator)
            bint operator==(reverse_iterator)
            bint operator==(const_reverse_iterator)
            bint operator!=(reverse_iterator)
            bint operator!=(const_reverse_iterator)
            bint operator<(reverse_iterator)
            bint operator<(const_reverse_iterator)
            bint operator>(reverse_iterator)
            bint operator>(const_reverse_iterator)
            bint operator<=(reverse_iterator)
            bint operator<=(const_reverse_iterator)
            bint operator>=(reverse_iterator)
            bint operator>=(const_reverse_iterator)
        cppclass const_reverse_iterator:
            const_reverse_iterator() except +
            const_reverse_iterator(reverse_iterator&) except +
            operator=(reverse_iterator&) except +
            const value_type& operator*()
            const_reverse_iterator operator++()
            const_reverse_iterator operator--()
            const_reverse_iterator operator++(i32)
            const_reverse_iterator operator--(i32)
            const_reverse_iterator operator+(size_type)
            const_reverse_iterator operator-(size_type)
            difference_type operator-(iterator)
            difference_type operator-(const_iterator)
            bint operator==(reverse_iterator)
            bint operator==(const_reverse_iterator)
            bint operator!=(reverse_iterator)
            bint operator!=(const_reverse_iterator)
            bint operator<(reverse_iterator)
            bint operator<(const_reverse_iterator)
            bint operator>(reverse_iterator)
            bint operator>(const_reverse_iterator)
            bint operator<=(reverse_iterator)
            bint operator<=(const_reverse_iterator)
            bint operator>=(reverse_iterator)
            bint operator>=(const_reverse_iterator)

        string() except +
        string(const string& s) except +
        string(const string& s, usize pos) except +
        string(const string& s, usize pos, usize len) except +
        string(const char* s) except +
        string(const char* s, usizen) except +
        string(usize n, char c) except +
        string(iterator first, iterator last) except +

        iterator begin()
        const_iterator const_begin "begin"()
        const_iterator cbegin()
        iterator end()
        const_iterator const_end "end"()
        const_iterator cend()
        reverse_iterator rbegin()
        const_reverse_iterator const_rbegin "rbegin"()
        const_reverse_iterator crbegin()
        reverse_iterator rend()
        const_reverse_iterator const_rend "rend"()
        const_reverse_iterator crend()

        const char* c_str()
        const char* data()
        usize size()
        usize max_size()
        usize length()
        void resize(usize) except +
        void resize(usize, char) except +
        void shrink_to_fit() except +
        void swap(string& other)
        usize capacity()
        void reserve(usize) except +
        void clear()
        bint empty()

        iterator erase(iterator first, iterator last)
        iterator erase(iterator p)
        iterator erase(const_iterator first, const_iterator last)
        iterator erase(const_iterator p)
        string& erase(usize pos, usize len) except +
        string& erase(usize) except +
        string& erase() except +

        char& at(usize pos) except +
        char& operator[](usize pos)
        char& front()
        char& back()
        int compare(const string& s)
        int compare(usize pos, usize len, const string& s) except +
        int compare(usize pos, usize len, const string& s, usize subpos, usize sublen) except +
        int compare(const char* s) except +
        int compare(usize pos, usize len, const char* s) except +
        int compare(usize pos, usize len, const char* s , usize n) except +

        string& append(const string& s) except +
        string& append(const string& s, usize subpos, usize sublen) except +
        string& append(const char* s) except +
        string& append(const char* s, usize n) except +
        string& append(usize n, char c) except +

        void push_back(char c) except +
        void pop_back()

        string& assign(const string& s) except +
        string& assign(const string& s, usize subpos, usize sublen) except +
        string& assign(const char* s, usize n) except +
        string& assign(const char* s) except +
        string& assign(usize n, char c) except +

        string& insert(usize pos, const string& s, usize subpos, usize sublen) except +
        string& insert(usize pos, const string& s) except +
        string& insert(usize pos, const char* s, usize n) except +
        string& insert(usize pos, const char* s) except +
        string& insert(usize pos, usize n, char c) except +
        void insert(iterator p, usize n, char c) except +
        iterator insert(iterator p, char c) except +

        usize copy(char* s, usize len, usize pos) except +
        usize copy(char* s, usize len) except +

        usize find(const string& s, usize pos)
        usize find(const string& s)
        usize find(const char* s, usize pos, usize n)
        usize find(const char* s, usize pos)
        usize find(const char* s)
        usize find(char c, usize pos)
        usize find(char c)

        usize rfind(const string&, usize pos)
        usize rfind(const string&)
        usize rfind(const char* s, usize pos, usize n)
        usize rfind(const char* s, usize pos)
        usize rfind(const char* s)
        usize rfind(char c, usize pos)
        usize rfind(char c)

        usize find_first_of(const string&, usize pos)
        usize find_first_of(const string&)
        usize find_first_of(const char* s, usize pos, usize n)
        usize find_first_of(const char* s, usize pos)
        usize find_first_of(const char* s)
        usize find_first_of(char c, usize pos)
        usize find_first_of(char c)

        usize find_first_not_of(const string& s, usize pos)
        usize find_first_not_of(const string& s)
        usize find_first_not_of(const char* s, usize pos, usize n)
        usize find_first_not_of(const char* s, usize pos)
        usize find_first_not_of(const char*)
        usize find_first_not_of(char c, usize pos)
        usize find_first_not_of(char c)

        usize find_last_of(const string& s, usize pos)
        usize find_last_of(const string& s)
        usize find_last_of(const char* s, usize pos, usize n)
        usize find_last_of(const char* s, usize pos)
        usize find_last_of(const char* s)
        usize find_last_of(char c, usize pos)
        usize find_last_of(char c)

        usize find_last_not_of(const string& s, usize pos)
        usize find_last_not_of(const string& s)
        usize find_last_not_of(const char* s, usize pos, usize n)
        usize find_last_not_of(const char* s, usize pos)
        usize find_last_not_of(const char* s)
        usize find_last_not_of(char c, usize pos)
        usize find_last_not_of(char c)

        string substr(usize pos, usize len) except +
        string substr(usize pos) except +
        string substr()

        # C++20
        bint starts_with(char c) except +
        bint starts_with(const char* s)
        bint ends_with(char c) except +
        bint ends_with(const char* s)
        # C++23
        bint contains(char c) except +
        bint contains(const char* s)

        #string& operator= (const string&)
        #string& operator= (const char*)
        #string& operator= (char)

        string operator+ (const string&) except +
        string operator+ (const char*) except +

        bint operator==(const string&)
        bint operator==(const char*)

        bint operator!= (const string&)
        bint operator!= (const char*)

        bint operator< (const string&)
        bint operator< (const char*)

        bint operator> (const string&)
        bint operator> (const char*)

        bint operator<= (const string&)
        bint operator<= (const char*)

        bint operator>= (const string&)
        bint operator>= (const char*)


    string to_string(i32 val) except +
    string to_string(long val) except +
    string to_string(long long val) except +
    string to_string(unsigned val) except +
    string to_string(usize val) except +
    string to_string(ssize_t val) except +
    string to_string(unsigned long val) except +
    string to_string(u128 val) except +
    string to_string(float val) except +
    string to_string(double val) except +
    string to_string(long double val) except +

    int stoi(const string& s, usize* idx, i32 base) except +
    int stoi(const string& s, usize* idx) except +
    int stoi(const string& s) except +
    long stol(const string& s, usize* idx, i32 base) except +
    long stol(const string& s, usize* idx) except +
    long stol(const string& s) except +
    long long stoll(const string& s, usize* idx, i32 base) except +
    long long stoll(const string& s, usize* idx) except +
    long long stoll(const string& s) except +

    u64 stoul(const string& s, usize* idx, i32 base) except +
    u64 stoul(const string& s, usize* idx) except +
    u64 stoul(const string& s) except +
    u128 stoull(const string& s, usize* idx, i32 base) except +
    u128 stoull(const string& s, usize* idx) except +
    u128 stoull(const string& s) except +

    float stof(const string& s, usize* idx) except +
    float stof(const string& s) except +
    double stod(const string& s, usize* idx) except +
    double stod(const string& s) except +
    long double stold(const string& s, usize* idx) except +
    long double stold(const string& s) except +
