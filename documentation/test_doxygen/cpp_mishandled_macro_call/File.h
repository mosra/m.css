/** @file
 * @brief A file.
 */

/** @brief A function-defining macro */
#define DEFINE_FUNCTION(name) int function_ ## name(int param)

/**
@brief A function-defining macro call

This one is misparsed as a function definition and because it doesn't do
anything that would make it look suspicious, it will appear in the output.
*/
DEFINE_FUNCTION(a) {
    return param;
}

/**
@brief A function-defining macro call

In this case the $ will however lead to the parameter to have a declname but
not a type, which triggers a suspicion in the parser and so the whole function
gets ignored.
*/
DEFINE_FUNCTION($) {
    return param;
}
