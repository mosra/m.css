m.dox
#####

.. role:: dox-flat(dox)
    :class: m-flat

-   Function link: :dox:`Utility::Path::make()`
-   Class link: :dox:`Containers::String`
-   Page link: :dox:`building-corrade`
-   File link: :dox:`/home/mosra/Code/corrade/src/Corrade/Corrade.h`
-   Typedef link: :dox:`Containers::StringView`
-   Enum link: :dox:`Utility::Path::ListFlag`
-   Enum value link: :dox:`Utility::Path::ListFlag::SkipDirectories`
-   Define link: :dox:`CORRADE_TARGET_AVX512F`
-   Macro function link: :dox:`CORRADE_ASSERT()`
-   Variable link: :dox:`Containers::AllocatedInit`
-   :dox:`Custom link title <testsuite>`
-   :dox:`Page link with custom title <corrade-cmake>`
-   :dox:`Link to index page <corrade>`
-   :dox:`Link to class documentation section <Containers-String-stl>`
-   :dox:`Link to index page with hash after <corrade#search>`
-   :dox:`Link to page with hash after <corrade-cmake#search>`
-   :dox:`Link to class with query and hash after <Utility::Path?q=hello#search>`
-   Flat link: :dox-flat:`plugin-management`

STL tagfile, which uses slightly different semantic:

-   Function: :dox:`std::memchr()`
-   Variable: :dox:`std::div_t::quot`

These should produce warnings:

-   Link to nonexistent name will be rendered as code: :dox:`nonExistent()`
-   :dox:`Link to nonexistent name with custom title will be just text <nonExistent()>`
-   Link to a section that doesn't have a title will keep the ID (this *may*
    break on tagfile update, watch out): :dox:`corrade-cmake-add-test`
-   Link to index page without title will have the tag file basename:
    :dox:`corrade`
