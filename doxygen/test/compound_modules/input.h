/** @defgroup group A group

Detailed description.
@{ */

/** @brief A foo */
void foo();

/*@}*/

/** @defgroup group2 Another group
@brief Brief description
@{ */

/** @brief A bar */
void bar();

/*@}*/

/**
@defgroup subgroup A subgroup
@brief Subgroup brief description
@ingroup group
@{ */

/**
@brief Returns 5 every 5 runs or something

Did I pass the interview now?
*/
int fizzbuzz();

/*@}*/
