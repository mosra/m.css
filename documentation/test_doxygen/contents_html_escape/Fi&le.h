/** @file
 * @brief The file path should be escaped, in the file list also
 */

/**
@brief The class include name as well as derived class reference should be escaped
*/
template<class T> struct Class {
    /** @brief Function */
    void suffixShouldBeEscaped(const Type<char>::ShouldBeEscaped& = "default value <&> should be escaped") &&;

    /** @brief Enum */
    enum Enum {
        Value = Initializer<char&>::ShouldBeEscaped
    };
};

template<class, class> struct Sub;

template<class T> struct Sub<char, T>: Class<T> {
    /** @brief The outer class name should be escaped, in the class list as well */
    struct Nested {};
};

/** @struct Sub<char, T> Fi&le.h FakeFi&le.h
 * @brief The class name as well as base class reference should be escaped, in the class list as well; the faked include should be escaped here too */

/** @brief Function specialization */
template<> void functionShouldHaveSpecializedNameEscaped<char&>();
