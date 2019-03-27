/** @brief A templated structure */
template<class T> struct S {};

/** @brief A templated structure specialization */
template<class T> struct S<T*> {
    /** @brief Inner struct */
    struct SS {};
};

// template <class T>
// struct S
// {
// };
//
// template <class T>
// struct S<T*>
// {
//   struct SS {};
// };
