/** @file
 * @brief Include file for group 1
 */

/**
@brief A namespace

This is a namespace. It is spread across two files.
*/
namespace Namespace {

/**
 * @defgroup group1 First group
 * @brief The first group, containing two functions
 * @{
 */

/**
@brief A function

With detailed description.
*/
void function1();

/**
@brief Another function

Also with detailed description.
*/
void function2();

/**
@brief A typedef

With details.
*/
typedef int FooBar;

/**
@brief A variable

Detailed description.
*/
constexpr FooBar FizzBuzz = 5;

/* Since 1.8.17, the original short-hand group closing doesn't work anymore.
   FFS. */
/**
 * @}
 */

}
