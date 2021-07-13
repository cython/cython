
# deprecated cimport for backwards compatibility:
from libc.string cimport const_char

cdef extern from "<string>" namespace "std::string" nogil:
    const size_t npos

cdef extern from "<string>" namespace "std" nogil:
    cdef cppclass string:
        cppclass iterator:
            iterator()
            char& operator*()
            iterator(iterator &)
            iterator operator++()
            iterator operator--()
            bint operator==(iterator)
            bint operator!=(iterator)
        cppclass reverse_iterator:
            char& operator*()
            iterator operator++()
            iterator operator--()
            iterator operator+(size_t)
            iterator operator-(size_t)
            bint operator==(reverse_iterator)
            bint operator!=(reverse_iterator)
            bint operator<(reverse_iterator)
            bint operator>(reverse_iterator)
            bint operator<=(reverse_iterator)
            bint operator>=(reverse_iterator)
        cppclass const_iterator(iterator):
            pass
        cppclass const_reverse_iterator(reverse_iterator):
            pass

        string() except +
        string(const char *) except +
        string(const char *, size_t) except +
        string(const string&) except +
        # as a string formed by a repetition of character c, n times.
        string(size_t, char) except +
        # from a pair of iterators
        string(iterator first, iterator last) except +

        iterator begin()
        const_iterator const_begin "begin"()
        iterator end()
        const_iterator const_end "end"()
        reverse_iterator rbegin()
        const_reverse_iterator const_rbegin "rbegin"()
        reverse_iterator rend()
        const_reverse_iterator const_rend "rend"()

        const char* c_str()
        const char* data()
        size_t size()
        size_t max_size()
        size_t length()
        void resize(size_t) except +
        void resize(size_t, char) except +
        void shrink_to_fit() except +
        size_t capacity()
        void reserve(size_t) except +
        void clear()
        bint empty()
        iterator erase(iterator, iterator)
        iterator erase(iterator)
        iterator erase(const_iterator, const_iterator)
        iterator erase(const_iterator)
        string& erase(size_t, size_t) except +
        string& erase(size_t) except +
        string& erase() except +

        char& at(size_t) except +
        char& operator[](size_t)
        char& front()
        char& back()
        int compare(const string&)
        int compare(size_t, size_t, const string&) except +
        int compare(size_t, size_t, const string&, size_t, size_t) except +
        int compare(const char*) except +
        int compare(size_t, size_t, const char*) except +
        int compare(size_t, size_t, const char*, size_t) except +

        string& append(const string&) except +
        string& append(const string&, size_t, size_t) except +
        string& append(const char *) except +
        string& append(const char *, size_t) except +
        string& append(size_t, char) except +

        void push_back(char c) except +
        void pop_back()

        string& assign (const string&) except +
        string& assign (const string&, size_t, size_t) except +
        string& assign (const char *, size_t) except +
        string& assign (const char *) except +
        string& assign (size_t n, char c) except +

        string& insert(size_t, const string&, size_t, size_t) except +
        string& insert(size_t, const string&) except +
        string& insert(size_t, const char* s, size_t) except +
        string& insert(size_t, const char* s) except +
        string& insert(size_t, size_t, char c) except +
        void insert(iterator, size_t, char) except +
        iterator insert(iterator, char) except +

        size_t copy(char *, size_t, size_t) except +
        size_t copy(char *, size_t) except +

        size_t find(const string&, size_t pos)
        size_t find(const string&)
        size_t find(const char*, size_t pos, size_t n)
        size_t find(const char*, size_t pos)
        size_t find(const char*)
        size_t find(char c, size_t pos)
        size_t find(char c)

        size_t rfind(const string&, size_t pos)
        size_t rfind(const string&)
        size_t rfind(const char* s, size_t pos, size_t n)
        size_t rfind(const char*, size_t pos)
        size_t rfind(const char*)
        size_t rfind(char c, size_t pos)
        size_t rfind(char c)

        size_t find_first_of(const string&, size_t pos)
        size_t find_first_of(const string&)
        size_t find_first_of(const char* s, size_t pos, size_t n)
        size_t find_first_of(const char*, size_t pos)
        size_t find_first_of(const char*)
        size_t find_first_of(char c, size_t pos)
        size_t find_first_of(char c)

        size_t find_first_not_of(const string&, size_t pos)
        size_t find_first_not_of(const string&)
        size_t find_first_not_of(const char* s, size_t, size_t)
        size_t find_first_not_of(const char*, size_t pos)
        size_t find_first_not_of(const char*)
        size_t find_first_not_of(char c, size_t pos)
        size_t find_first_not_of(char c)

        size_t find_last_of(const string&, size_t pos)
        size_t find_last_of(const string&)
        size_t find_last_of(const char* s, size_t pos, size_t n)
        size_t find_last_of(const char*, size_t pos)
        size_t find_last_of(const char*)
        size_t find_last_of(char c, size_t pos)
        size_t find_last_of(char c)

        size_t find_last_not_of(const string&, size_t pos)
        size_t find_last_not_of(const string&)
        size_t find_last_not_of(const char* s, size_t pos, size_t n)
        size_t find_last_not_of(const char*, size_t pos)
        size_t find_last_not_of(const char*)
        size_t find_last_not_of(char c, size_t pos)
        size_t find_last_not_of(char c)

        string substr(size_t, size_t) except +
        string substr()
        string substr(size_t) except +

        #string& operator= (const string&)
        #string& operator= (const char*)
        #string& operator= (char)

        string operator+ (const string& rhs) except +
        string operator+ (const char* rhs) except +

        bint operator==(const string&)
        bint operator==(const char*)

        bint operator!= (const string& rhs )
        bint operator!= (const char* )

        bint operator< (const string&)
        bint operator< (const char*)

        bint operator> (const string&)
        bint operator> (const char*)

        bint operator<= (const string&)
        bint operator<= (const char*)

        bint operator>= (const string&)
        bint operator>= (const char*)


    string to_string(int) except +
    string to_string(long) except +
    string to_string(long long) except +
    string to_string(unsigned) except +
    string to_string(size_t) except +
    string to_string(ssize_t) except +
    string to_string(unsigned long) except +
    string to_string(unsigned long long) except +
    string to_string(float) except +
    string to_string(double) except +
    string to_string(long double) except +

    int stoi(const string&, size_t*, int) except +
    int stoi(const string&, size_t*) except +
    int stoi(const string&) except +
    long stol(const string&, size_t*, int) except +
    long stol(const string&, size_t*) except +
    long stol(const string&) except +
    long long stoll(const string&, size_t*, int) except +
    long long stoll(const string&, size_t*) except +
    long long stoll(const string&) except +

    unsigned long stoul(const string&, size_t*, int) except +
    unsigned long stoul(const string&, size_t*) except +
    unsigned long stoul(const string&) except +
    unsigned long long stoull(const string&, size_t*, int) except +
    unsigned long long stoull(const string&, size_t*) except +
    unsigned long long stoull(const string&) except +

    float stof(const string&, size_t*) except +
    float stof(const string&) except +
    double stod(const string&, size_t*) except +
    double stod(const string&) except +
    long double stold(const string&, size_t*) except +
    long double stold(const string&) except +

