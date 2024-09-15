/** @file
 * @brief A library header
 *
 * Should be shown as `include/Library/Library.h` in the page and also in the
 * file tree, neither of them prefixed with `project/`. Its contents should
 * then show `#include <Library/Library.h>`, without the `project/include/`
 * prefix.
 */

/**
 * @brief A library namespace
 *
 * Should have no include listed, as it's spread over multiple files.
 */
namespace Library {

/**
 * @brief A library entrypoint
 *
 * Should have `#include <Library/Library.h>` listed, without
 * `project/include/`.
 */
void function();

/**
 * @brief A library enum
 *
 * Should have `#include <Library/Library.h>` listed, without
 * `project/include/`.
 */
enum Enum {};

/** @related Class
 * @brief A related function
 *
 * This function is related to the class, but is in a different header, so it
 * should have `#include <Library/Library.h>` even though the class has
 * overriden the header file (but not name) to point to `Library.h`. The code
 * still treats `Data.h` as the actual class definiton because otherwise all
 * class members would list redundant `#include` in its detailed docs.
 */
void related();

}
