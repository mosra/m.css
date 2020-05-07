/** @defgroup group A group

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
