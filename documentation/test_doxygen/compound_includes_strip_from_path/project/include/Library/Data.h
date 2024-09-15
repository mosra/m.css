/** @file
 * @brief A library data header
 *
 * Should be shown as `include/Library/Data.h` in the page and also in the
 * file tree, neither of them prefixed with `project/`. Its contents should
 * then show `#include <Library/Data.h>`, without the `project/include/`
 * prefix.
 */

namespace Library {

/**
 * @brief A library structure
 *
 * Should have `#include <Library/Data.h>` listed, without `project/include/`.
 */
struct Struct {};

class Class {
    public:
        /**
         * @brief Class function
         *
         * The class has the location overriden to `Library.h` and thus
         * location for the function (which is in `Data.h` and can't be
         * overriden) doesn't match the class. Showing a different include for
         * it won't make sense tho as it's a member, so the code pretends the
         * current include matches the actual location and not what was
         * overriden.
         */
        void foo();
};

/** @class Class project/include/Library/Library.h FakeHeader.h
 * @brief A class with overriden header file and name
 *
 * The overriden header *file* is used as the target location (where it links
 * to the `Library.h` file, *not* to `Data.h` in which it's defined), the
 * header *name* is what gets displayed.
 */

/**
 * @brief A helper subnamespace
 *
 * Should have `#include <Library/Data.h>` listed, without `project/include/`.
 */
namespace Helper {
    /**
     * @brief Library version
     *
     * Should have no incldue listed, as the namespace is contained in a single
     * file.
     */
    unsigned version();
}

/**
 * @brief A library typedef
 *
 * Should have `#include <Library/Data.h>` listed, without `project/include/`.
 */
typedef Struct Typedef;

}
