/** @file
 * @brief A file
 */

/**
@brief A friend class

Not displayed among @ref Class friends because Doxygen doesn't provide any
useful info for it.
*/
class FriendClassWarning {};

/**
@brief A friend class

Not displayed among @ref Class friends because Doxygen doesn't provide any
useful info for it.
*/
class GroupedFriendClassWarning {};

/** @brief A class */
class Class {
    public:
        /* Ignored */
        friend class FriendClass;
        friend struct FriendStruct;
        friend union FriendUnion;

        /** @brief A friend function */
        friend void friendFunction(int a, void* b);

        /** @brief A 'hidden friend' operator */
        friend bool operator==(const Class&, const Class&) noexcept;

        /** @brief A constexpr 'hidden friend' operator */
        friend constexpr bool operator!=(const Class&, const Class&) noexcept;

        /** @{ @name Group with friend functions */

        /** @brief A friend grouped function */
        friend void friendGroupedFunction();

        /* Since 1.8.17, the original short-hand group closing doesn't work
           anymore. FFS. */
        /**
         * @}
         */
};

/** @brief A class producing warnings */
struct Warning {
    /** @brief Ignored friend class with a warning because it has docs */
    friend class FriendClassWarning;

    /** @{ @name Group with friend functions */

    /** @brief Ignored friend class with a warning because it has docs */
    friend class GroupedFriendClassWarning;

    /* Since 1.8.17, the original short-hand group closing doesn't work
        anymore. FFS. */
    /**
     * @}
     */
};

/** @brief Class with template parameters */
template<class T, class U = void, class = int> class Template {
    protected: /* Shouldn't matter */
        /**
         * @brief Friend function
         * @tparam V This is a V
         *
         * This is broken in doxygen itself as it doesn't include any scope
         * from the class.
         */
        template<class V> friend void foobar();
};
