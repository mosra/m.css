/** @brief Private base class, should not list any derived */
class PrivateBase {};

/** @brief Protected base, should list a derived, but w/o any label */
class ProtectedBase {};

class UndocumentedBase {};

/** @brief Virtual base, should list a derived, but w/o any label */
class VirtualBase {};

/**
@brief A class

Should list one protected base and one virtual base, one derived class.
*/
class A: PrivateBase, protected ProtectedBase, public UndocumentedBase, public virtual VirtualBase {};

/** @brief A derived class */
class Derived: public A {};

struct UndocumentedDerived: A {};
