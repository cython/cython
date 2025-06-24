# cython: preliminary_late_includes_cy28=True

from libcpp.mutex cimport unique_lock, mutex
from libcpp.stop_token cimport stop_token
from libcpp cimport bool as _bool

cdef extern from "<condition_variable>" namespace "std" nogil:
    cdef enum class cv_status:
        no_timeout
        timeout

    cdef cppclass condition_variable:
        cppclass native_handle_type:
            pass

        condition_variable() except+

        void notify_one() noexcept
        void notify_all() noexcept

        # Be very wary of calling any of the wait functions with the GIL held.
        # Also be a little wary of re-acquiring the GIL in the predicate
        # (because in principle it may deadlock with the lock).
        # The predicate should not require the GIL or throw Python exceptions.
        void wait(unique_lock[mutex]& lock) except+
        void wait[Predicate](unique_lock[mutex]& lock, Predicate pred) except+

        cv_status wait_for[Duration](unique_lock[mutex]& lock, const Duration &duration) except+
        _bool wait_for[Duration, Predicate](unique_lock[mutex]& lock, const Duration &duration, Predicate pred) except+
        cv_status wait_until[TimePoint](unique_lock[mutex]& lock, const TimePoint& time_point) except+
        _bool wait_until[TimePoint, Predicate](unique_lock[mutex]& lock, const TimePoint& time_point, Predicate pred) except+

        native_handle_type native_handle() except+

    cdef cppclass condition_variable_any:
        condition_variable_any() except+

        void notify_one() noexcept
        void notify_all() noexcept

        # Be very wary of calling any of the wait functions with the GIL held.
        # Also be a little wary of re-acquiring the GIL in the predicate
        # (because in principle it may deadlock with the lock).
        # The predicate should not require the GIL or throw Python exceptions.
        void wait[Lock](Lock& lock) except+
        void wait[Lock, Predicate](Lock& lock, Predicate pred) except+
        _bool wait[Lock, Predicate](Lock& lock, stop_token stoken, Predicate pred) except+

        cv_status wait_for[Lock, Duration](Lock& lock, const Duration &duration) except+
        _bool wait_for[Lock, Duration, Predicate](Lock& lock, const Duration &duration, Predicate pred) except+
        _bool wait_for[Lock, Duration, Predicate](Lock& lock, stop_token stoken, const Duration &duration, Predicate pred) except+
        cv_status wait_until[Lock, TimePoint](Lock& lock, const TimePoint &time_point) except+
        _bool wait_until[Lock, TimePoint, Predicate](Lock& lock, const TimePoint &time_point, Predicate pred) except+
        _bool wait_until[Lock, TimePoint, Predicate](Lock& lock, stop_token stoken, const TimePoint &time_point, Predicate pred) except+

    void notify_all_at_thread_exit(condition_variable& cv, unique_lock[mutex]& lock) except+

cdef inline void _dummy_force_utility_code_inclusion() nogil:
    with nogil:
        pass

cdef extern from *:
    """
    namespace {

    template <typename Lock>
    void __Pyx_libcpp_cv_relock_at_end(Lock& lock, __Pyx_UnknownThreadState &ts) {
        if (__Pyx_UnknownThreadStateMayHaveHadGil(ts)) {
            lock.unlock();  // unlocking should not throw
            __Pyx_RestoreUnknownThread(ts);
            // ensure_gil, release_gil and py_safe_std_lock are defined in mutex.pdx
            PyGILState_STATE gil_state = __pyx_libcpp_mutex_limited_api_ensure_gil();
            auto cleanup = __pyx_make_libcpp_mutex_cleanup_on_exit([&gil_state](){
                __pyx_libcpp_mutex_limited_api_release_gil(gil_state);
            });
            __pyx_py_safe_std_lock(lock);
        } else {
            __Pyx_RestoreUnknownThread(ts);
        }
    }

    template <typename Lock, typename Predicate>
    class __Pyx_libcpp_cv_WrappedPySafePredicate {
        Lock *lock;
        Predicate *pred;
        __Pyx_UnknownThreadState *ts;
    public:
        __Pyx_libcpp_cv_WrappedPySafePredicate(Lock *l, Predicate *p, __Pyx_UnknownThreadState *ts) 
            : lock(l)
            , pred(p)
            , ts(ts)
        {}

        bool operator()() const {
            PyGILState_STATE gil_state;
            lock->unlock();
            int had_gil_on_call = __Pyx_UnknownThreadStateDefinitelyHadGil(*ts);
            if (had_gil_on_call) {
                __Pyx_RestoreUnknownThread(*ts);
            } else {
                gil_state = PyGILState_Ensure();
            }
            auto release_gil = __pyx_make_libcpp_mutex_cleanup_on_exit(
                [&]() {
                    if (had_gil_on_call) {
                        *ts = __Pyx_SaveUnknownThread();
                    } else {
                        PyGILState_Release(gil_state);
                    }
                });
            __pyx_py_safe_std_lock(*lock);
            // No need to unlock - the condition variable is responsible for that and it shouldn't be possible
            // to deadlock from here.
            bool result = (*pred)();
            if (PyErr_Occurred()) {
                // The PyErr_Occurred check in __Pyx_CppExn2PyErr will deal with
                // presenting the exception to Cython.
                throw std::exception();
            }
            return result;
        }
    };

    template <typename Lock, typename Predicate>
    __Pyx_libcpp_cv_WrappedPySafePredicate<Lock, Predicate> __Pyx_libcpp_cv_py_safe_wrap_predicate(Lock* lock, Predicate* pred, __Pyx_UnknownThreadState* ts) {
        return __Pyx_libcpp_cv_WrappedPySafePredicate<Lock, Predicate>(lock, pred, ts);
    }

    class __Pyx_libcpp_cv_WrappedPyObjectPredicate {
        PyObject *pred; // unowned
    public:
        explicit __Pyx_libcpp_cv_WrappedPyObjectPredicate(PyObject *pred) : pred(pred) {}

        bool operator()() const {
            PyObject *res = PyObject_CallObject(pred, nullptr);
            if (res) {
                auto is_true = PyObject_IsTrue(res);
                Py_DECREF(res);
                return is_true; // exceptions don't matter - we have a PyErr_Occurred check outside
            }
            return false; // we have a PyErr_Occurred check outside
        }
    };

    template <typename Lock, typename CV_T>
    void __Pyx_libcpp_cv_py_safe_wait_impl(CV_T& cv, Lock& lock) {
        __Pyx_UnknownThreadState ts = __Pyx_SaveUnknownThread();
        auto cleanup = __pyx_make_libcpp_mutex_cleanup_on_exit(
            [&ts, &lock](){
                __Pyx_libcpp_cv_relock_at_end(lock, ts);
            }
        );
        cv.wait(lock);
    }

    inline bool __Pyx_libcpp_cv_dummy_predicate() { return true; }  // Just used for type deduction, not called

    template <typename Lock, typename Predicate, typename CV_T, typename ...Args>
    auto __Pyx_libcpp_cv_py_safe_wait_impl(CV_T& cv, Lock& lock, Predicate pred, Args&&... args) 
        -> decltype(cv.wait(lock, std::forward<Args>(args)..., __Pyx_libcpp_cv_dummy_predicate)) {
        __Pyx_UnknownThreadState ts = __Pyx_SaveUnknownThread();
        auto cleanup = __pyx_make_libcpp_mutex_cleanup_on_exit(
            [&ts, &lock](){
                __Pyx_libcpp_cv_relock_at_end(lock, ts);
            });
        return cv.wait(lock, std::forward<Args>(args)..., __Pyx_libcpp_cv_py_safe_wrap_predicate(&lock, &pred, &ts));
    }

    // StopToken only templated to support c++11 (where it doesn't yet exist)
    template <typename Lock, typename Predicate, typename StopToken>
    bool __Pyx_libcpp_cv_py_safe_wait_4arg(std::condition_variable_any& cv, Lock& lock, StopToken stoken, Predicate pred) {
        // note in impl, predicate comes first
        return __Pyx_libcpp_cv_py_safe_wait_impl(cv, lock, std::move(pred), std::move(stoken));
    }

    template <typename Lock, typename CV_T, typename ...Args>
    auto __Pyx_libcpp_cv_py_safe_wait_object(CV_T& cv, Lock& lock, Args&&... args, PyObject *pred) ->
        decltype(__Pyx_libcpp_cv_py_safe_wait_impl(
            cv, lock,
            __Pyx_libcpp_cv_dummy_predicate,
            std::forward<Args>(args)...)) {
        return __Pyx_libcpp_cv_py_safe_wait_impl(
            cv, lock,
            __Pyx_libcpp_cv_WrappedPyObjectPredicate(pred),
            std::forward<Args>(args)...);
    }


    } // namespace
    """
    void py_safe_wait "__Pyx_libcpp_cv_py_safe_wait_impl" (condition_variable& cv, unique_lock[mutex]& lock) except+
    void py_safe_object_wait "__Pyx_libcpp_cv_py_safe_wait_object" (condition_variable& cv, unique_lock[mutex]& lock, object predicate) except+
    void py_safe_wait "__Pyx_libcpp_cv_py_safe_wait_impl" [Predicate](condition_variable& cv, unique_lock[mutex]& lock, Predicate predicate) except+
    void py_safe_wait "__Pyx_libcpp_cv_py_safe_wait_impl" [Lock](condition_variable_any& cv, Lock& lock) except+
    void py_safe_object_wait "__Pyx_libcpp_cv_py_safe_wait_object" [Lock](condition_variable_any& cv, Lock& lock, object predicate) except+
    void py_safe_wait "__Pyx_libcpp_cv_py_safe_wait_impl" [Lock, Predicate](condition_variable_any& cv, Lock& lock, Predicate predicate) except+
    _bool py_safe_object_wait "__Pyx_libcpp_cv_py_safe_wait_object" [Lock](condition_variable_any& cv, Lock& lock, stop_token stoken, object predicate) except+
    _bool py_safe_wait "__Pyx_libcpp_cv_py_safe_wait_impl" [Lock, Predicate](condition_variable_any& cv, Lock& lock, stop_token stoken, Predicate predicate) except+

    cv_status py_safe_wait_for[Duration](condition_variable& cv, unique_lock[mutex]& lock, const Duration &duration) except+
    _bool wait_for[Duration](condition_variable& cv, unique_lock[mutex]& lock, const Duration &duration, object pred) except+
    _bool wait_for[Duration, Predicate](condition_variable& cv, unique_lock[mutex]& lock, const Duration &duration, Predicate pred) except+
    cv_status wait_for[Lock, Duration](condition_variable_any& cv, Lock& lock, const Duration &duration) except+
    _bool wait_for[Lock, Duration, Predicate](condition_variable_any& cv, Lock& lock, const Duration &duration, object pred) except+
    _bool wait_for[Lock, Duration, Predicate](condition_variable_any& cv, Lock& lock, const Duration &duration, Predicate pred) except+
    _bool wait_for[Lock, Duration, Predicate](condition_variable_any& cv, Lock& lock, stop_token stoken, const Duration &duration, object pred) except+
    _bool wait_for[Lock, Duration, Predicate](condition_variable_any& cv, Lock& lock, stop_token stoken, const Duration &duration, Predicate pred) except+

    cv_status py_safe_wait_until[TimePoint](condition_variable& cv, unique_lock[mutex]& lock, const TimePoint &time_point) except+
    _bool wait_until[TimePoint](condition_variable& cv, unique_lock[mutex]& lock, const TimePoint &time_point, object pred) except+
    _bool wait_until[TimePoint, Predicate](condition_variable& cv, unique_lock[mutex]& lock, const TimePoint &time_point, Predicate pred) except+
    cv_status wait_until[Lock, TimePoint](condition_variable_any& cv, Lock& lock, const TimePoint &time_point) except+
    _bool wait_until[Lock, TimePoint, Predicate](condition_variable_any& cv, Lock& lock, const TimePoint &time_point, object pred) except+
    _bool wait_until[Lock, TimePoint, Predicate](condition_variable_any& cv, Lock& lock, const TimePoint &time_point, Predicate pred) except+
    _bool wait_until[Lock, TimePoint, Predicate](condition_variable_any& cv, Lock& lock, stop_token stoken, const TimePoint &time_point, object pred) except+
    _bool wait_until[Lock, TimePoint, Predicate](condition_variable_any& cv, Lock& lock, stop_token stoken, const TimePoint &time_point, Predicate pred) except+
        