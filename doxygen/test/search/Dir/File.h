/** @dir Dir
 * @brief A directory
 */

/** @file
 * @brief A file
 */

/** @brief A namespace */
namespace Namespace {

/** @brief A class */
class Class {
    public:
        /** @brief Function without arguments */
        void foo();

        void foo() const; /**< @overload */

        void foo() &&; /**< @overload */

        /** @brief Function with arguments */
        void foo(const Enum& first, Typedef second);
};

/** @brief A variable */
constexpr int Variable = 5;

/** @brief A typedef */
typedef int Typedef;

/** @brief An enum */
enum class Enum {
    Value = 15  /**< Enum value */
};

/** @defgroup group A group
 * @{
 */

/** @brief An union */
union Union {};

/** @brief A struct */
struct Struct {};

/*@}*/

}

/** @brief A macro */
#define MACRO

/** @brief Macro function */
#define MACRO_FUNCTION()

/** @brief Macro function with params */
#define MACRO_FUNCTION_WITH_PARAMS(params)

namespace UndocumentedNamespace {}

class UndocumentedClass {};

void undocumentedFunction();

constexpr int UndocumentedVariable = 42;

typedef int UndocumentedTypedef;

enum class UndocumentedEnum {
    UndocumentedValue
};

#define UNDOCUMENTED_MACRO
