/** @dir DeprecatedDirectory
 * @brief A dir with pretty old things.
 * @m_deprecated_since{2010,02} Yes it is.
 */

/** @file
 * @brief Pretty old things.
 * @m_deprecated_since{2010,02} Yes it is.
 */

/**
@brief A namespace
@m_deprecated_since{2010,02} Yes it is.
*/
namespace DeprecatedFoo {

/**
@brief A class
@m_deprecated_since{2010,02} Yes it is.
*/
class DeprecatedClass {};

/**
@brief A subclass
@m_deprecated_since{2010,02} Yes it is.
*/
struct DeprecatedSubclass: DeprecatedClass {};

/**
@brief A function
@m_deprecated_since{2010,02} Yes it is.

Details should have the badge too.
*/
void deprecatedFoo();

/**
@brief A typedef
@m_deprecated_since{2010,02} Yes it is.

Details should have the badge too.
*/
typedef DeprecatedClass DeprecatedKlazz;

/**
@brief An enum
@m_deprecated_since{2010,02} Yes it is.

Details should have the badge too.
*/
enum DeprecatedEnum {
    /**
     * This thing is deprecated.
     *
     * Yes.
     *
     * @m_deprecated_since{2010,02} Yes it is.
     */
    DeprecatedOldValue = 0,

    /* Some other. */
    NewValue = 3
};

/**
@brief A constant
@m_deprecated_since{2010,02} Yes it is.

Details should have the badge too.
*/
constexpr int DeprecatedFive = 5;

}

/**
@brief A define
@m_deprecated_since{2010,02} Yes it is.

Details should have the badge too.
*/
#define DEPRECATED_DEFINE
