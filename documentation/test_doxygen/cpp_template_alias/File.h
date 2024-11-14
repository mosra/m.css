/** @file
 * @brief A file.
 */

/** @brief Class with template parameters */
template<class T, class U = void, class = int> struct Template {
    /**
     * @brief Template alias
     * @tparam V Well, this is V as well
     *
     * Should include both template lists, with _3 for unnamed parameter.
     */
    template<class V, bool = false> using Foo = Buuu<V, false>;
};

/* Not putting the second sentence into detailed docs to verify that just a
   presence of tparam alone makes the detailed docs appear */
/**
@brief A templated type with just template details. The `UndocumentedTemplate` shouldn't appear in the template detailed description.
@tparam T Template param
*/
template<class T, class UndocumentedTemplate, typename = void> using Foo = Bar<T, int>;
