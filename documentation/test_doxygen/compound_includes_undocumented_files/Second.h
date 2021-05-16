/* @file
 * @brief Turn this into a Doxygen comment to enable include info
 */

/* This file needs to be kept the same as compound_includes/Second.h except for
   the above @file block. */

namespace Spread {

/** @brief A function */
void foo();

/** @{ @name A group */

/** @brief Flag in a group */
enum Flag {};

/* Since 1.8.17, the original short-hand group closing doesn't work anymore.
   FFS. */
/**
 * @}
 */

/** @related Class
 * @brief A related enum in a different file. Detailed info only if includes not disabled.
 */
enum RelatedEnum {};

/** @related Class
 * @brief A related typedef in a different file. Detailed info only if includes not disabled.
 */
typedef int RelatedInt;

/** @related Class
 * @brief A related variable in a different file. Detailed info only if includes not disabled.
 */
constexpr const int RelatedVar = 3;

/** @related Class
 * @brief A related function in a different file. Detailed info only if includes not disabled.
 */
void relatedFunc();

/** @related Class
 * @brief A related define in a different file. Detailed info only if includes not disabled.
 */
#define RELATED_DEFINE

}

/**
@brief A class forward-declared in one file but defined in another

Because Doxygen is stupid, it reports the class to be defined in First.h even
though there's just a fwdecl. Happens only if the class is a template,
a non-templated class would have its location reported correctly.

If includes are enabled, members should have Second.h listed as their include,
but if they are disabled, brief-only members shouldn't have detailed sections
at all.
*/
template<class T> struct SpreadClass {
    /** @brief A function with (detailed) include information but no details if includes are disabled */
    void foo();
};
