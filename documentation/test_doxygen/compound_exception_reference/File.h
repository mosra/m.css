/** @file
 * @brief A file
 */

/** @brief An exception */
struct MyException {};

/**
@brief A function that throws
@throw std::runtime_exception This one doesn't have a reference
@throw MyException This one does
*/
void foo();
