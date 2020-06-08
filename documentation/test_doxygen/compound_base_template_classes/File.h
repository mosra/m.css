/** @file
 * @brief A file
 */

/** @brief A namespace */
namespace Namespace {

/** @brief A base */
template<class> struct Base {};

/**
@brief A class with two different template bases

The @ref Namespace gets stripped from the references.
*/
struct MyClass: Base<int>, Base<Base<float>> {};

}
