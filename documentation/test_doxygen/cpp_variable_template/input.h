/** @brief A non-template class */
struct Foo {
    /** @brief Template variable without template docs */
    template<class T> static T* variable;

    /* Not putting the second sentence into detailed docs to verify that just a
       presence of tparam alone makes the detailed docs appear */
    /**
     * @brief Template variable with template docs. The `UndocumentedTemplate` shouldn't appear in the template detailed description.
     * @tparam T Well, the type
     */
    template<class T, class UndocumentedTemplate> static T& another;
};

/** @brief Template class */
template<class T> struct Bar {
    /** @brief Template variable inside a template class without template docs */
    template<class U> static Foo<U>* instance;

    /**
     * @brief Template variable inside a template class with template docs
     * @tparam U Well, the type
     */
    template<class U> static Foo<U>& another;
};
