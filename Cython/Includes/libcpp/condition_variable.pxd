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

    void notify_all_at_thread_exit(condition_variable& cv, unique_lock[mutex] lock) except+
