/*
    This file is part of m.css.

    Copyright © 2017, 2018 Vladimír Vondruš <mosra@centrum.cz>

    Permission is hereby granted, free of charge, to any person obtaining a
    copy of this software and associated documentation files (the "Software"),
    to deal in the Software without restriction, including without limitation
    the rights to use, copy, modify, merge, publish, distribute, sublicense,
    and/or sell copies of the Software, and to permit persons to whom the
    Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included
    in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
    DEALINGS IN THE SOFTWARE.
*/

"use strict"; /* it summons the Cthulhu in a proper way, they say */

var Search = {
    trie: null,
    map: null,
    dataSize: 0,
    symbolCount: 0,
    maxResults: 0,

    /* Always contains at least the root node offset and then one node offset
       per entered character */
    searchString: '',
    searchStack: [],

    init: function(buffer, maxResults) {
        let view = new DataView(buffer);

        /* The file is too short to contain at least the headers */
        if(view.byteLength < 18) {
            console.error("Search data too short");
            return false;
        }

        if(view.getUint8(0) != 'M'.charCodeAt(0) ||
           view.getUint8(1) != 'C'.charCodeAt(0) ||
           view.getUint8(2) != 'S'.charCodeAt(0)) {
            console.error("Invalid search data signature");
            return false;
        }

        if(view.getUint8(3) != 0) {
            console.error("Invalid search data version");
            return false;
        }

        /* Separate the data into the trie and the result map */
        let mapOffset = view.getUint32(4, true);
        this.trie = new DataView(buffer, 8, mapOffset - 8);
        this.map = new DataView(buffer, mapOffset);

        /* Set initial properties */
        this.dataSize = Math.round(buffer.byteLength/102.4)/10;
        this.symbolCount = (this.map.getUint32(0, true) & 0x00ffffff)/4 - 1;
        this.maxResults = maxResults ? maxResults : 100;
        this.searchString = '';
        this.searchStack = [this.trie.getUint32(0, true)];

        /* istanbul ignore if */
        if(typeof document !== 'undefined') {
            document.getElementById('search-symbolcount').innerHTML =
                this.symbolCount + " symbols (" + this.dataSize + " kB)";
            document.getElementById('search-input').disabled = false;
            document.getElementById('search-input').placeholder = "Type something here …";
            document.getElementById('search-input').focus();

            /* Search for the input value (there might be something already,
               for example when going back in the browser) */
            let value = document.getElementById('search-input').value;
            if(value.length) Search.renderResults(value, Search.search(value));
        }

        return true;
    },

    download: /* istanbul ignore next */ function(url) {
        var req = window.XDomainRequest ? new XDomainRequest() : new XMLHttpRequest();
        if(!req) return;

        req.open("GET", url, true);
        req.responseType = 'arraybuffer';
        req.onreadystatechange = function() {
            if(req.readyState != 4) return;

            Search.init(req.response);
        }
        req.send();
    },

    base85decode: function(base85string) {
        function charValue(char) {
            if(char >=  48 && char <  58) /* 0-9 -> 0-9 */
                return char - 48 + 0;
            if(char >=  65 && char <  91) /* A-Z -> 10-35 */
                return char - 65 + 10;
            if(char >=  97 && char < 123) /* a-z -> 36-61 */
                return char - 97 + 36;
            if(char ==  33)               /*  !  -> 62 */
                return 62;
            /* skipping 34 (') */
            if(char >=  35 && char <  39) /* #-& -> 63-66 */
                return char - 35 + 63;
            /* skipping 39 (") */
            if(char >=  40 && char <  44) /* (-+ -> 67-70 */
                return char - 40 + 67;
            /* skipping 44 (,) */
            if(char ==  45)               /*  -  -> 71 */
                return 71;
            if(char >=  59 && char <  65) /* ;-@ -> 72-77 */
                return char - 59 + 72;
            if(char >=  94 && char <  97) /* ^-` -> 78-80 */
                return char - 94 + 78;
            if(char >= 123 && char < 127) /* {-~ -> 81-84 */
                return char - 123 + 81;

            return 0; /* Interpret padding values as zeros */
        }

        /* Pad the string for easier decode later. We don't read past the file
           end, so it doesn't matter what garbage is there. */
        if(base85string.length % 5) {
            console.log("Expected properly padded base85 data");
            return;
        }

        let buffer = new ArrayBuffer(base85string.length*4/5);
        let data8 = new DataView(buffer);
        for(let i = 0; i < base85string.length; i += 5) {
            let char1 = charValue(base85string.charCodeAt(i + 0));
            let char2 = charValue(base85string.charCodeAt(i + 1));
            let char3 = charValue(base85string.charCodeAt(i + 2));
            let char4 = charValue(base85string.charCodeAt(i + 3));
            let char5 = charValue(base85string.charCodeAt(i + 4));

            data8.setUint32(i*4/5, char5 +
                                   char4*85 +
                                   char3*85*85 +
                                   char2*85*85*85 +
                                   char1*85*85*85*85, false); /* BE, yes */
        }

        return buffer;
    },

    load: function(base85string) {
        return this.init(this.base85decode(base85string));
    },

    /* http://ecmanaut.blogspot.com/2006/07/encoding-decoding-utf8-in-javascript.html */
    toUtf8: function(string) { return unescape(encodeURIComponent(string)); },
    fromUtf8: function(string) { return decodeURIComponent(escape(string)); },

    /* Returns the values in UTF-8, but input is in whatever shitty 16bit
       encoding JS has */
    search: function(searchString) {
        /* Normalize the search string first, convert to UTF-8 */
        searchString = this.toUtf8(searchString.toLowerCase().trim());

        /* TODO: maybe i could make use of InputEvent.data and others here */

        /* Find longest common prefix of previous and current value so we don't
           need to needlessly search again */
        let max = Math.min(searchString.length, this.searchString.length);
        let commonPrefix = 0;
        for(; commonPrefix != max; ++commonPrefix)
            if(searchString[commonPrefix] != this.searchString[commonPrefix]) break;

        /* Drop items off the stack if it has has more than is needed for the
           common prefix (it needs to have at least one item, though) */
        if(commonPrefix + 1 < this.searchStack.length)
            this.searchStack.splice(commonPrefix + 1, this.searchStack.length - commonPrefix - 1);

        /* Add new characters from the search string */
        let foundPrefix = commonPrefix;
        for(; foundPrefix != searchString.length; ++foundPrefix) {
            /* Calculate offset and count of children */
            let offset = this.searchStack[this.searchStack.length - 1];
            let nodeSize = this.trie.getUint8(offset)*2;
            let relChildOffset = 2 + this.trie.getUint8(offset + 1)*2;
            let childCount = (nodeSize - relChildOffset)/4;

            /* Go through all children and find the next offset */
            let childOffset = offset + relChildOffset;
            let found = false;
            for(let j = 0; j != childCount; ++j) {
                if(String.fromCharCode(this.trie.getUint8(childOffset + j*4 + 3)) != searchString[foundPrefix])
                    continue;

                this.searchStack.push(this.trie.getUint32(childOffset + j*4, true) & 0x007fffff);
                found = true;
                break;
            }

            /* Character not found, exit */
            if(!found) break;
        }

        /* Save the whole found prefix for next time */
        this.searchString = searchString.substr(0, foundPrefix);

        /* If the whole thing was not found, return an empty result and offer
           external search */
        if(foundPrefix != searchString.length) {
            /* istanbul ignore if */
            if(typeof document !== 'undefined') {
                let link = document.getElementById('search-external');
                if(link)
                    link.href = link.dataset.searchEngine.replace('{query}', encodeURIComponent(searchString));
            }
            return [];
        }

        /* Otherwise recursively gather the results */
        let results = [];
        this.gatherResults(this.searchStack[this.searchStack.length - 1], 0, results);
        return results;
    },

    gatherResults: function(offset, suffixLength, results) {
        let valueCount = this.trie.getUint8(offset + 1);

        /* Populate the results with all values associated with this node */
        for(let i = 0; i != valueCount; ++i) {
            let index = this.trie.getUint16(offset + (i + 1)*2, true);
            let flags = this.map.getUint8(index*4 + 3);
            let resultOffset = this.map.getUint32(index*4, true) & 0x00ffffff;

            /* The result has a suffix, extract its length */
            let resultSuffixLength = 0;
            if(flags & 0x01) {
                resultSuffixLength = this.map.getUint8(resultOffset);
                ++resultOffset;
            }

            let nextResultOffset = this.map.getUint32((index + 1)*4, true) & 0x00ffffff;

            let name = '';
            let j = resultOffset;
            for(; j != nextResultOffset; ++j) {
                let c = this.map.getUint8(j);

                /* End of null-delimited name */
                if(!c) {
                    ++j;
                    break; /* null-delimited */
                }

                name += String.fromCharCode(c); /* eheh. IS THIS FAST?! */
            }

            let url = '';
            for(; j != nextResultOffset; ++j) {
                url += String.fromCharCode(this.map.getUint8(j));
            }

            /* Keeping in UTF-8, as we need that for proper slicing */
            results.push({name: name,
                          url: url,
                          flags: flags,
                          suffixLength: suffixLength + resultSuffixLength});

            /* 'nuff said. */
            /* TODO: remove once proper barriers are in */
            if(results.length >= this.maxResults) return true;
        }

        /* Dig deeper. If the child already has enough, return. */
        /* TODO: hmmm. this is helluvalot duplicated code. hmm. */
        let nodeSize = this.trie.getUint8(offset)*2;
        let relChildOffset = 2 + this.trie.getUint8(offset + 1)*2;
        let childCount = (nodeSize - relChildOffset)/4;
        let childOffset = offset + relChildOffset;
        for(let j = 0; j != childCount; ++j) {
            let offsetBarrier = this.trie.getUint32(childOffset + j*4, true);

            /* Lookahead barrier, don't dig deeper */
            if(offsetBarrier & 0x00800000) continue;

            if(this.gatherResults(offsetBarrier & 0x007fffff, suffixLength + 1, results))
                return true;
        }

        /* Still hungry. */
        return false;
    },

    escapeForRtl: function(name) {
        /* Besides the obvious escaping of HTML entities we also need
           to escape punctuation, because due to the RTL hack to cut
           text off on left side the punctuation characters get
           reordered (of course). Prepending &lrm; works for most
           characters, parentheses we need to *soak* in it. But only
           the right ones. And that for some reason needs to be also for &.
           Huh. https://en.wikipedia.org/wiki/Right-to-left_mark */
        return name.replace(/[\"&<>]/g, function (a) {
            return { '"': '&quot;', '&': '&amp;', '<': '&lt;', '>': '&gt;' }[a];
        }).replace(/[:=]/g, '&lrm;$&').replace(/(\)|&gt;|&amp;|\/)/g, '&lrm;$&&lrm;');
    },

    renderResults: /* istanbul ignore next */ function(value, results) {
        /* Normalize the value and encode as UTF-8 so the slicing works
           properly */
        value = this.toUtf8(value.trim());

        if(!value.length) {
            document.getElementById('search-help').style.display = 'block';
            document.getElementById('search-results').style.display = 'none';
            document.getElementById('search-notfound').style.display = 'none';
            return;
        }

        document.getElementById('search-help').style.display = 'none';

        if(results.length) {
            document.getElementById('search-results').style.display = 'block';
            document.getElementById('search-notfound').style.display = 'none';

            let list = '';
            for(let i = 0; i != results.length; ++i) {
                let type = '';
                let color = '';
                switch(results[i].flags >> 4) {
                    case 1:
                        type = 'namespace';
                        color = 'm-primary';
                        break;
                    case 2:
                        type = 'class';
                        color = 'm-primary';
                        break;
                    case 3:
                        type = 'struct';
                        color = 'm-primary';
                        break;
                    case 4:
                        type = 'union';
                        color = 'm-primary';
                        break;
                    case 5:
                        type = 'typedef';
                        color = 'm-primary';
                        break;
                    case 6:
                        type = 'func';
                        color = 'm-info';
                        break;
                    case 7:
                        type = 'var';
                        color = 'm-default';
                        break;
                    case 8:
                        type = 'enum';
                        color = 'm-primary';
                        break;
                    case 9:
                        type = 'enum val';
                        color = 'm-default';
                        break;
                    case 10:
                        type = 'define';
                        color = 'm-info';
                        break;
                    case 11:
                        type = 'group';
                        color = 'm-success';
                        break;
                    case 12:
                        type = 'page';
                        color = 'm-success';
                        break;
                    case 13:
                        type = 'dir';
                        color = 'm-warning';
                        break;
                    case 14:
                        type = 'file';
                        color = 'm-warning';
                        break;
                }

                list += this.fromUtf8('<li' + (i ? '' : ' id="search-current"') + '><a href="' + results[i].url + '" onmouseover="selectResult(event)"><div class="m-label m-flat ' + color + '">' + type + '</div>' + (results[i].flags & 2 ? '<div class="m-label m-danger">deprecated</div>' : '') + '<div><span class="m-text m-dim">' + this.escapeForRtl(results[i].name.substr(0, results[i].name.length - value.length - results[i].suffixLength)) + '</span><span class="m-dox-search-typed">' + this.escapeForRtl(results[i].name.substr(results[i].name.length - value.length - results[i].suffixLength, value.length)) + '</span>' + this.escapeForRtl(results[i].name.substr(results[i].name.length - results[i].suffixLength)) + '</div></a></li>');
            }
            document.getElementById('search-results').innerHTML = list;
            document.getElementById('search-current').scrollIntoView(true);

        } else {
            document.getElementById('search-results').style.display = 'none';
            document.getElementById('search-notfound').style.display = 'block';
        }
    },
};

/* istanbul ignore next */
function selectResult(event) {
    if(event.currentTarget.parentNode.id == 'search-current') return;

    let current = document.getElementById('search-current');
    current.id = '';
    event.currentTarget.parentNode.id = 'search-current';
}

/* istanbul ignore next */
function showSearch() {
    window.location.hash = '#search';

    /* Prevent accidental scrolling of the body, prevent page layout jumps */
    let scrolledBodyWidth = document.body.offsetWidth;
    document.body.style.overflow = 'hidden';
    document.body.style.paddingRight = (document.body.offsetWidth - scrolledBodyWidth) + 'px';

    document.getElementById('search-input').value = '';
    document.getElementById('search-input').focus();
    document.getElementById('search-results').style.display = 'none';
    document.getElementById('search-notfound').style.display = 'none';
    document.getElementById('search-help').style.display = 'block';
    return false;
}

/* istanbul ignore next */
function hideSearch() {
    window.location.hash = '#!';
    window.history.pushState('', '', window.location.pathname);

    /* Restore scrollbar, prevent page layout jumps */
    document.body.style.overflow = 'auto';
    document.body.style.paddingRight = '0';

    return false;
}

/* Only in case we're running in a browser. Why a simple if(document) doesn't
   work is beyond me. */ /* istanbul ignore if */
if(typeof document !== 'undefined') {
    document.getElementById('search-input').oninput = function(event) {
        let value = document.getElementById('search-input').value;
        let prev = performance.now();
        let results = Search.search(value);
        let after = performance.now();
        Search.renderResults(value, results);
        if(value.trim().length) {
            document.getElementById('search-symbolcount').innerHTML =
                results.length + (results.length >= Search.maxResults ? '+' : '') + " results (" + Math.round((after - prev)*10)/10 + " ms)";
        } else
            document.getElementById('search-symbolcount').innerHTML =
                Search.symbolCount + " symbols (" + Search.dataSize + " kB)";
    };

    document.onkeydown = function(event) {
        /* Search shown */
        if(window.location.hash == '#search') {
            /* Close the search */
            if(event.key == 'Escape') {
                hideSearch();

            /* Select next item */
            } else if(event.key == 'ArrowDown' || (event.key == 'Tab' && !event.shiftKey)) {
                let current = document.getElementById('search-current');
                if(current) {
                    let next = current.nextSibling;
                    if(next) {
                        current.id = '';
                        next.id = 'search-current';
                        next.scrollIntoView(false);
                    }
                }
                return false; /* so the keypress doesn't affect input cursor */

            /* Select prev item */
            } else if(event.key == 'ArrowUp' || (event.key == 'Tab' && event.shiftKey)) {
                let current = document.getElementById('search-current');
                if(current) {
                    let prev = current.previousSibling;
                    if(prev) {
                        current.id = '';
                        prev.id = 'search-current';
                        prev.scrollIntoView(false);
                    }
                }
                return false; /* so the keypress doesn't affect input cursor */

            /* Go to result */
            } else if(event.key == 'Enter') {
                document.getElementById('search-current').firstElementChild.click();
                return false; /* so the keypress doesn't affect input cursor */
            }

        /* Search hidden */
        } else {
            /* Open the search on the T or Tab key */
            if(event.key.toLowerCase() == 't' || event.key == 'Tab') {
                showSearch();
                return false; /* so T doesn't get entered into the box */
            }
        }
    };
}

/* For Node.js testing */ /* istanbul ignore else */
if(typeof module !== 'undefined') { module.exports = { Search: Search }; }
