/** @defgroup group A group
@brief Brief description. If this is not present, the detailed description gets interpreted as brief in 1.8.18. FFS.

Detailed description.
@{ */

/** @brief A foo */
void foo();

/* Since 1.8.17, the original short-hand group closing doesn't work anymore.
   FFS. */
/**
 * @}
 */

/** @defgroup group2 Another group
@brief Brief description
@{ */

/** @brief A bar */
void bar();

/* Since 1.8.17, the original short-hand group closing doesn't work anymore.
   FFS. */
/**
 * @}
 */

/**
@defgroup subgroup A subgroup
@brief Subgroup brief description
@ingroup group

@section subgroup-description Description

Subgroup description. There are **no members**, so there should be also no
Reference section in the TOC.
*/
