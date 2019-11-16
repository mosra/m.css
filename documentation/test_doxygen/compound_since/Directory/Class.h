/* WHAT THE FUCK DOXYGEN WHY IS THIS MATCHING THE NAME PARTIALLY?! WHAT */
/** @dir compound_since/Directory
 * @brief A dir with pretty old things.
 * @m_since{2010,02}
 */

/** @file
 * @brief Pretty old things.
 * @m_since{2010,02}
 */

/**
@brief A namespace
@m_since{2010,02}
*/
namespace Foo {

/**
@brief A class
@m_since{2019,11}
*/
class Class {};

/**
@brief A subclass
@m_since{2019,11}
*/
struct Subclass: Class {};

/**
@brief A function
@m_since{2010,02}

Details should have the badge too.
*/
void foo();

/**
@brief A typedef
@m_since{2010,02}

Details should have the badge too.
*/
typedef Class Klazz;

/**
@brief An enum
@m_since{2010,02}

Details should have the badge too.
*/
enum Enum {
    OldValue = 0,

    /**
     * This thing is new.
     *
     * Yes.
     *
     * @m_since{2019,11}
     */
    NewValue = 3
};

/**
@brief A constant
@m_since{2010,02}

Details should have the badge too.
*/
constexpr int Five = 5;

}

/**
@brief A define
@m_since{2010,02}

Details should have the badge too.
*/
#define A_DEFINE
