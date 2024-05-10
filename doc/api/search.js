window.pdocSearch = (function () {
    /** elasticlunr - http://weixsong.github.io * Copyright (C) 2017 Oliver Nightingale * Copyright (C) 2017 Wei Song * MIT Licensed */!function () {
        function e(e) {
            if (null === e || "object" != typeof e) return e;
            var t = e.constructor();
            for (var n in e) e.hasOwnProperty(n) && (t[n] = e[n]);
            return t
        }

        var t = function (e) {
            var n = new t.Index;
            return n.pipeline.add(t.trimmer, t.stopWordFilter, t.stemmer), e && e.call(n, n), n
        };
        t.version = "0.9.5", lunr = t, t.utils = {}, t.utils.warn = function (e) {
            return function (t) {
                e.console && console.warn && console.warn(t)
            }
        }(this), t.utils.toString = function (e) {
            return void 0 === e || null === e ? "" : e.toString()
        }, t.EventEmitter = function () {
            this.events = {}
        }, t.EventEmitter.prototype.addListener = function () {
            var e = Array.prototype.slice.call(arguments), t = e.pop(), n = e;
            if ("function" != typeof t) throw new TypeError("last argument must be a function");
            n.forEach(function (e) {
                this.hasHandler(e) || (this.events[e] = []), this.events[e].push(t)
            }, this)
        }, t.EventEmitter.prototype.removeListener = function (e, t) {
            if (this.hasHandler(e)) {
                var n = this.events[e].indexOf(t);
                -1 !== n && (this.events[e].splice(n, 1), 0 == this.events[e].length && delete this.events[e])
            }
        }, t.EventEmitter.prototype.emit = function (e) {
            if (this.hasHandler(e)) {
                var t = Array.prototype.slice.call(arguments, 1);
                this.events[e].forEach(function (e) {
                    e.apply(void 0, t)
                }, this)
            }
        }, t.EventEmitter.prototype.hasHandler = function (e) {
            return e in this.events
        }, t.tokenizer = function (e) {
            if (!arguments.length || null === e || void 0 === e) return [];
            if (Array.isArray(e)) {
                var n = e.filter(function (e) {
                    return null === e || void 0 === e ? !1 : !0
                });
                n = n.map(function (e) {
                    return t.utils.toString(e).toLowerCase()
                });
                var i = [];
                return n.forEach(function (e) {
                    var n = e.split(t.tokenizer.seperator);
                    i = i.concat(n)
                }, this), i
            }
            return e.toString().trim().toLowerCase().split(t.tokenizer.seperator)
        }, t.tokenizer.defaultSeperator = /[\s\-]+/, t.tokenizer.seperator = t.tokenizer.defaultSeperator, t.tokenizer.setSeperator = function (e) {
            null !== e && void 0 !== e && "object" == typeof e && (t.tokenizer.seperator = e)
        }, t.tokenizer.resetSeperator = function () {
            t.tokenizer.seperator = t.tokenizer.defaultSeperator
        }, t.tokenizer.getSeperator = function () {
            return t.tokenizer.seperator
        }, t.Pipeline = function () {
            this._queue = []
        }, t.Pipeline.registeredFunctions = {}, t.Pipeline.registerFunction = function (e, n) {
            n in t.Pipeline.registeredFunctions && t.utils.warn("Overwriting existing registered function: " + n), e.label = n, t.Pipeline.registeredFunctions[n] = e
        }, t.Pipeline.getRegisteredFunction = function (e) {
            return e in t.Pipeline.registeredFunctions != !0 ? null : t.Pipeline.registeredFunctions[e]
        }, t.Pipeline.warnIfFunctionNotRegistered = function (e) {
            var n = e.label && e.label in this.registeredFunctions;
            n || t.utils.warn("Function is not registered with pipeline. This may cause problems when serialising the index.\n", e)
        }, t.Pipeline.load = function (e) {
            var n = new t.Pipeline;
            return e.forEach(function (e) {
                var i = t.Pipeline.getRegisteredFunction(e);
                if (!i) throw new Error("Cannot load un-registered function: " + e);
                n.add(i)
            }), n
        }, t.Pipeline.prototype.add = function () {
            var e = Array.prototype.slice.call(arguments);
            e.forEach(function (e) {
                t.Pipeline.warnIfFunctionNotRegistered(e), this._queue.push(e)
            }, this)
        }, t.Pipeline.prototype.after = function (e, n) {
            t.Pipeline.warnIfFunctionNotRegistered(n);
            var i = this._queue.indexOf(e);
            if (-1 === i) throw new Error("Cannot find existingFn");
            this._queue.splice(i + 1, 0, n)
        }, t.Pipeline.prototype.before = function (e, n) {
            t.Pipeline.warnIfFunctionNotRegistered(n);
            var i = this._queue.indexOf(e);
            if (-1 === i) throw new Error("Cannot find existingFn");
            this._queue.splice(i, 0, n)
        }, t.Pipeline.prototype.remove = function (e) {
            var t = this._queue.indexOf(e);
            -1 !== t && this._queue.splice(t, 1)
        }, t.Pipeline.prototype.run = function (e) {
            for (var t = [], n = e.length, i = this._queue.length, o = 0; n > o; o++) {
                for (var r = e[o], s = 0; i > s && (r = this._queue[s](r, o, e), void 0 !== r && null !== r); s++) ;
                void 0 !== r && null !== r && t.push(r)
            }
            return t
        }, t.Pipeline.prototype.reset = function () {
            this._queue = []
        }, t.Pipeline.prototype.get = function () {
            return this._queue
        }, t.Pipeline.prototype.toJSON = function () {
            return this._queue.map(function (e) {
                return t.Pipeline.warnIfFunctionNotRegistered(e), e.label
            })
        }, t.Index = function () {
            this._fields = [], this._ref = "id", this.pipeline = new t.Pipeline, this.documentStore = new t.DocumentStore, this.index = {}, this.eventEmitter = new t.EventEmitter, this._idfCache = {}, this.on("add", "remove", "update", function () {
                this._idfCache = {}
            }.bind(this))
        }, t.Index.prototype.on = function () {
            var e = Array.prototype.slice.call(arguments);
            return this.eventEmitter.addListener.apply(this.eventEmitter, e)
        }, t.Index.prototype.off = function (e, t) {
            return this.eventEmitter.removeListener(e, t)
        }, t.Index.load = function (e) {
            e.version !== t.version && t.utils.warn("version mismatch: current " + t.version + " importing " + e.version);
            var n = new this;
            n._fields = e.fields, n._ref = e.ref, n.documentStore = t.DocumentStore.load(e.documentStore), n.pipeline = t.Pipeline.load(e.pipeline), n.index = {};
            for (var i in e.index) n.index[i] = t.InvertedIndex.load(e.index[i]);
            return n
        }, t.Index.prototype.addField = function (e) {
            return this._fields.push(e), this.index[e] = new t.InvertedIndex, this
        }, t.Index.prototype.setRef = function (e) {
            return this._ref = e, this
        }, t.Index.prototype.saveDocument = function (e) {
            return this.documentStore = new t.DocumentStore(e), this
        }, t.Index.prototype.addDoc = function (e, n) {
            if (e) {
                var n = void 0 === n ? !0 : n, i = e[this._ref];
                this.documentStore.addDoc(i, e), this._fields.forEach(function (n) {
                    var o = this.pipeline.run(t.tokenizer(e[n]));
                    this.documentStore.addFieldLength(i, n, o.length);
                    var r = {};
                    o.forEach(function (e) {
                        e in r ? r[e] += 1 : r[e] = 1
                    }, this);
                    for (var s in r) {
                        var u = r[s];
                        u = Math.sqrt(u), this.index[n].addToken(s, {ref: i, tf: u})
                    }
                }, this), n && this.eventEmitter.emit("add", e, this)
            }
        }, t.Index.prototype.removeDocByRef = function (e) {
            if (e && this.documentStore.isDocStored() !== !1 && this.documentStore.hasDoc(e)) {
                var t = this.documentStore.getDoc(e);
                this.removeDoc(t, !1)
            }
        }, t.Index.prototype.removeDoc = function (e, n) {
            if (e) {
                var n = void 0 === n ? !0 : n, i = e[this._ref];
                this.documentStore.hasDoc(i) && (this.documentStore.removeDoc(i), this._fields.forEach(function (n) {
                    var o = this.pipeline.run(t.tokenizer(e[n]));
                    o.forEach(function (e) {
                        this.index[n].removeToken(e, i)
                    }, this)
                }, this), n && this.eventEmitter.emit("remove", e, this))
            }
        }, t.Index.prototype.updateDoc = function (e, t) {
            var t = void 0 === t ? !0 : t;
            this.removeDocByRef(e[this._ref], !1), this.addDoc(e, !1), t && this.eventEmitter.emit("update", e, this)
        }, t.Index.prototype.idf = function (e, t) {
            var n = "@" + t + "/" + e;
            if (Object.prototype.hasOwnProperty.call(this._idfCache, n)) return this._idfCache[n];
            var i = this.index[t].getDocFreq(e), o = 1 + Math.log(this.documentStore.length / (i + 1));
            return this._idfCache[n] = o, o
        }, t.Index.prototype.getFields = function () {
            return this._fields.slice()
        }, t.Index.prototype.search = function (e, n) {
            if (!e) return [];
            e = "string" == typeof e ? {any: e} : JSON.parse(JSON.stringify(e));
            var i = null;
            null != n && (i = JSON.stringify(n));
            for (var o = new t.Configuration(i, this.getFields()).get(), r = {}, s = Object.keys(e), u = 0; u < s.length; u++) {
                var a = s[u];
                r[a] = this.pipeline.run(t.tokenizer(e[a]))
            }
            var l = {};
            for (var c in o) {
                var d = r[c] || r.any;
                if (d) {
                    var f = this.fieldSearch(d, c, o), h = o[c].boost;
                    for (var p in f) f[p] = f[p] * h;
                    for (var p in f) p in l ? l[p] += f[p] : l[p] = f[p]
                }
            }
            var v, g = [];
            for (var p in l) v = {
                ref: p,
                score: l[p]
            }, this.documentStore.hasDoc(p) && (v.doc = this.documentStore.getDoc(p)), g.push(v);
            return g.sort(function (e, t) {
                return t.score - e.score
            }), g
        }, t.Index.prototype.fieldSearch = function (e, t, n) {
            var i = n[t].bool, o = n[t].expand, r = n[t].boost, s = null, u = {};
            return 0 !== r ? (e.forEach(function (e) {
                var n = [e];
                1 == o && (n = this.index[t].expandToken(e));
                var r = {};
                n.forEach(function (n) {
                    var o = this.index[t].getDocs(n), a = this.idf(n, t);
                    if (s && "AND" == i) {
                        var l = {};
                        for (var c in s) c in o && (l[c] = o[c]);
                        o = l
                    }
                    n == e && this.fieldSearchStats(u, n, o);
                    for (var c in o) {
                        var d = this.index[t].getTermFrequency(n, c), f = this.documentStore.getFieldLength(c, t),
                            h = 1;
                        0 != f && (h = 1 / Math.sqrt(f));
                        var p = 1;
                        n != e && (p = .15 * (1 - (n.length - e.length) / n.length));
                        var v = d * a * h * p;
                        c in r ? r[c] += v : r[c] = v
                    }
                }, this), s = this.mergeScores(s, r, i)
            }, this), s = this.coordNorm(s, u, e.length)) : void 0
        }, t.Index.prototype.mergeScores = function (e, t, n) {
            if (!e) return t;
            if ("AND" == n) {
                var i = {};
                for (var o in t) o in e && (i[o] = e[o] + t[o]);
                return i
            }
            for (var o in t) o in e ? e[o] += t[o] : e[o] = t[o];
            return e
        }, t.Index.prototype.fieldSearchStats = function (e, t, n) {
            for (var i in n) i in e ? e[i].push(t) : e[i] = [t]
        }, t.Index.prototype.coordNorm = function (e, t, n) {
            for (var i in e) if (i in t) {
                var o = t[i].length;
                e[i] = e[i] * o / n
            }
            return e
        }, t.Index.prototype.toJSON = function () {
            var e = {};
            return this._fields.forEach(function (t) {
                e[t] = this.index[t].toJSON()
            }, this), {
                version: t.version,
                fields: this._fields,
                ref: this._ref,
                documentStore: this.documentStore.toJSON(),
                index: e,
                pipeline: this.pipeline.toJSON()
            }
        }, t.Index.prototype.use = function (e) {
            var t = Array.prototype.slice.call(arguments, 1);
            t.unshift(this), e.apply(this, t)
        }, t.DocumentStore = function (e) {
            this._save = null === e || void 0 === e ? !0 : e, this.docs = {}, this.docInfo = {}, this.length = 0
        }, t.DocumentStore.load = function (e) {
            var t = new this;
            return t.length = e.length, t.docs = e.docs, t.docInfo = e.docInfo, t._save = e.save, t
        }, t.DocumentStore.prototype.isDocStored = function () {
            return this._save
        }, t.DocumentStore.prototype.addDoc = function (t, n) {
            this.hasDoc(t) || this.length++, this.docs[t] = this._save === !0 ? e(n) : null
        }, t.DocumentStore.prototype.getDoc = function (e) {
            return this.hasDoc(e) === !1 ? null : this.docs[e]
        }, t.DocumentStore.prototype.hasDoc = function (e) {
            return e in this.docs
        }, t.DocumentStore.prototype.removeDoc = function (e) {
            this.hasDoc(e) && (delete this.docs[e], delete this.docInfo[e], this.length--)
        }, t.DocumentStore.prototype.addFieldLength = function (e, t, n) {
            null !== e && void 0 !== e && 0 != this.hasDoc(e) && (this.docInfo[e] || (this.docInfo[e] = {}), this.docInfo[e][t] = n)
        }, t.DocumentStore.prototype.updateFieldLength = function (e, t, n) {
            null !== e && void 0 !== e && 0 != this.hasDoc(e) && this.addFieldLength(e, t, n)
        }, t.DocumentStore.prototype.getFieldLength = function (e, t) {
            return null === e || void 0 === e ? 0 : e in this.docs && t in this.docInfo[e] ? this.docInfo[e][t] : 0
        }, t.DocumentStore.prototype.toJSON = function () {
            return {docs: this.docs, docInfo: this.docInfo, length: this.length, save: this._save}
        }, t.stemmer = function () {
            var e = {
                    ational: "ate",
                    tional: "tion",
                    enci: "ence",
                    anci: "ance",
                    izer: "ize",
                    bli: "ble",
                    alli: "al",
                    entli: "ent",
                    eli: "e",
                    ousli: "ous",
                    ization: "ize",
                    ation: "ate",
                    ator: "ate",
                    alism: "al",
                    iveness: "ive",
                    fulness: "ful",
                    ousness: "ous",
                    aliti: "al",
                    iviti: "ive",
                    biliti: "ble",
                    logi: "log"
                }, t = {icate: "ic", ative: "", alize: "al", iciti: "ic", ical: "ic", ful: "", ness: ""}, n = "[^aeiou]",
                i = "[aeiouy]", o = n + "[^aeiouy]*", r = i + "[aeiou]*", s = "^(" + o + ")?" + r + o,
                u = "^(" + o + ")?" + r + o + "(" + r + ")?$", a = "^(" + o + ")?" + r + o + r + o,
                l = "^(" + o + ")?" + i, c = new RegExp(s), d = new RegExp(a), f = new RegExp(u), h = new RegExp(l),
                p = /^(.+?)(ss|i)es$/, v = /^(.+?)([^s])s$/, g = /^(.+?)eed$/, m = /^(.+?)(ed|ing)$/, y = /.$/,
                S = /(at|bl|iz)$/, x = new RegExp("([^aeiouylsz])\\1$"), w = new RegExp("^" + o + i + "[^aeiouwxy]$"),
                I = /^(.+?[^aeiou])y$/,
                b = /^(.+?)(ational|tional|enci|anci|izer|bli|alli|entli|eli|ousli|ization|ation|ator|alism|iveness|fulness|ousness|aliti|iviti|biliti|logi)$/,
                E = /^(.+?)(icate|ative|alize|iciti|ical|ful|ness)$/,
                D = /^(.+?)(al|ance|ence|er|ic|able|ible|ant|ement|ment|ent|ou|ism|ate|iti|ous|ive|ize)$/,
                F = /^(.+?)(s|t)(ion)$/, _ = /^(.+?)e$/, P = /ll$/, k = new RegExp("^" + o + i + "[^aeiouwxy]$"),
                z = function (n) {
                    var i, o, r, s, u, a, l;
                    if (n.length < 3) return n;
                    if (r = n.substr(0, 1), "y" == r && (n = r.toUpperCase() + n.substr(1)), s = p, u = v, s.test(n) ? n = n.replace(s, "$1$2") : u.test(n) && (n = n.replace(u, "$1$2")), s = g, u = m, s.test(n)) {
                        var z = s.exec(n);
                        s = c, s.test(z[1]) && (s = y, n = n.replace(s, ""))
                    } else if (u.test(n)) {
                        var z = u.exec(n);
                        i = z[1], u = h, u.test(i) && (n = i, u = S, a = x, l = w, u.test(n) ? n += "e" : a.test(n) ? (s = y, n = n.replace(s, "")) : l.test(n) && (n += "e"))
                    }
                    if (s = I, s.test(n)) {
                        var z = s.exec(n);
                        i = z[1], n = i + "i"
                    }
                    if (s = b, s.test(n)) {
                        var z = s.exec(n);
                        i = z[1], o = z[2], s = c, s.test(i) && (n = i + e[o])
                    }
                    if (s = E, s.test(n)) {
                        var z = s.exec(n);
                        i = z[1], o = z[2], s = c, s.test(i) && (n = i + t[o])
                    }
                    if (s = D, u = F, s.test(n)) {
                        var z = s.exec(n);
                        i = z[1], s = d, s.test(i) && (n = i)
                    } else if (u.test(n)) {
                        var z = u.exec(n);
                        i = z[1] + z[2], u = d, u.test(i) && (n = i)
                    }
                    if (s = _, s.test(n)) {
                        var z = s.exec(n);
                        i = z[1], s = d, u = f, a = k, (s.test(i) || u.test(i) && !a.test(i)) && (n = i)
                    }
                    return s = P, u = d, s.test(n) && u.test(n) && (s = y, n = n.replace(s, "")), "y" == r && (n = r.toLowerCase() + n.substr(1)), n
                };
            return z
        }(), t.Pipeline.registerFunction(t.stemmer, "stemmer"), t.stopWordFilter = function (e) {
            return e && t.stopWordFilter.stopWords[e] !== !0 ? e : void 0
        }, t.clearStopWords = function () {
            t.stopWordFilter.stopWords = {}
        }, t.addStopWords = function (e) {
            null != e && Array.isArray(e) !== !1 && e.forEach(function (e) {
                t.stopWordFilter.stopWords[e] = !0
            }, this)
        }, t.resetStopWords = function () {
            t.stopWordFilter.stopWords = t.defaultStopWords
        }, t.defaultStopWords = {
            "": !0,
            a: !0,
            able: !0,
            about: !0,
            across: !0,
            after: !0,
            all: !0,
            almost: !0,
            also: !0,
            am: !0,
            among: !0,
            an: !0,
            and: !0,
            any: !0,
            are: !0,
            as: !0,
            at: !0,
            be: !0,
            because: !0,
            been: !0,
            but: !0,
            by: !0,
            can: !0,
            cannot: !0,
            could: !0,
            dear: !0,
            did: !0,
            "do": !0,
            does: !0,
            either: !0,
            "else": !0,
            ever: !0,
            every: !0,
            "for": !0,
            from: !0,
            get: !0,
            got: !0,
            had: !0,
            has: !0,
            have: !0,
            he: !0,
            her: !0,
            hers: !0,
            him: !0,
            his: !0,
            how: !0,
            however: !0,
            i: !0,
            "if": !0,
            "in": !0,
            into: !0,
            is: !0,
            it: !0,
            its: !0,
            just: !0,
            least: !0,
            let: !0,
            like: !0,
            likely: !0,
            may: !0,
            me: !0,
            might: !0,
            most: !0,
            must: !0,
            my: !0,
            neither: !0,
            no: !0,
            nor: !0,
            not: !0,
            of: !0,
            off: !0,
            often: !0,
            on: !0,
            only: !0,
            or: !0,
            other: !0,
            our: !0,
            own: !0,
            rather: !0,
            said: !0,
            say: !0,
            says: !0,
            she: !0,
            should: !0,
            since: !0,
            so: !0,
            some: !0,
            than: !0,
            that: !0,
            the: !0,
            their: !0,
            them: !0,
            then: !0,
            there: !0,
            these: !0,
            they: !0,
            "this": !0,
            tis: !0,
            to: !0,
            too: !0,
            twas: !0,
            us: !0,
            wants: !0,
            was: !0,
            we: !0,
            were: !0,
            what: !0,
            when: !0,
            where: !0,
            which: !0,
            "while": !0,
            who: !0,
            whom: !0,
            why: !0,
            will: !0,
            "with": !0,
            would: !0,
            yet: !0,
            you: !0,
            your: !0
        }, t.stopWordFilter.stopWords = t.defaultStopWords, t.Pipeline.registerFunction(t.stopWordFilter, "stopWordFilter"), t.trimmer = function (e) {
            if (null === e || void 0 === e) throw new Error("token should not be undefined");
            return e.replace(/^\W+/, "").replace(/\W+$/, "")
        }, t.Pipeline.registerFunction(t.trimmer, "trimmer"), t.InvertedIndex = function () {
            this.root = {docs: {}, df: 0}
        }, t.InvertedIndex.load = function (e) {
            var t = new this;
            return t.root = e.root, t
        }, t.InvertedIndex.prototype.addToken = function (e, t, n) {
            for (var n = n || this.root, i = 0; i <= e.length - 1;) {
                var o = e[i];
                o in n || (n[o] = {docs: {}, df: 0}), i += 1, n = n[o]
            }
            var r = t.ref;
            n.docs[r] ? n.docs[r] = {tf: t.tf} : (n.docs[r] = {tf: t.tf}, n.df += 1)
        }, t.InvertedIndex.prototype.hasToken = function (e) {
            if (!e) return !1;
            for (var t = this.root, n = 0; n < e.length; n++) {
                if (!t[e[n]]) return !1;
                t = t[e[n]]
            }
            return !0
        }, t.InvertedIndex.prototype.getNode = function (e) {
            if (!e) return null;
            for (var t = this.root, n = 0; n < e.length; n++) {
                if (!t[e[n]]) return null;
                t = t[e[n]]
            }
            return t
        }, t.InvertedIndex.prototype.getDocs = function (e) {
            var t = this.getNode(e);
            return null == t ? {} : t.docs
        }, t.InvertedIndex.prototype.getTermFrequency = function (e, t) {
            var n = this.getNode(e);
            return null == n ? 0 : t in n.docs ? n.docs[t].tf : 0
        }, t.InvertedIndex.prototype.getDocFreq = function (e) {
            var t = this.getNode(e);
            return null == t ? 0 : t.df
        }, t.InvertedIndex.prototype.removeToken = function (e, t) {
            if (e) {
                var n = this.getNode(e);
                null != n && t in n.docs && (delete n.docs[t], n.df -= 1)
            }
        }, t.InvertedIndex.prototype.expandToken = function (e, t, n) {
            if (null == e || "" == e) return [];
            var t = t || [];
            if (void 0 == n && (n = this.getNode(e), null == n)) return t;
            n.df > 0 && t.push(e);
            for (var i in n) "docs" !== i && "df" !== i && this.expandToken(e + i, t, n[i]);
            return t
        }, t.InvertedIndex.prototype.toJSON = function () {
            return {root: this.root}
        }, t.Configuration = function (e, n) {
            var e = e || "";
            if (void 0 == n || null == n) throw new Error("fields should not be null");
            this.config = {};
            var i;
            try {
                i = JSON.parse(e), this.buildUserConfig(i, n)
            } catch (o) {
                t.utils.warn("user configuration parse failed, will use default configuration"), this.buildDefaultConfig(n)
            }
        }, t.Configuration.prototype.buildDefaultConfig = function (e) {
            this.reset(), e.forEach(function (e) {
                this.config[e] = {boost: 1, bool: "OR", expand: !1}
            }, this)
        }, t.Configuration.prototype.buildUserConfig = function (e, n) {
            var i = "OR", o = !1;
            if (this.reset(), "bool" in e && (i = e.bool || i), "expand" in e && (o = e.expand || o), "fields" in e) for (var r in e.fields) if (n.indexOf(r) > -1) {
                var s = e.fields[r], u = o;
                void 0 != s.expand && (u = s.expand), this.config[r] = {
                    boost: s.boost || 0 === s.boost ? s.boost : 1,
                    bool: s.bool || i,
                    expand: u
                }
            } else t.utils.warn("field name in user configuration not found in index instance fields"); else this.addAllFields2UserConfig(i, o, n)
        }, t.Configuration.prototype.addAllFields2UserConfig = function (e, t, n) {
            n.forEach(function (n) {
                this.config[n] = {boost: 1, bool: e, expand: t}
            }, this)
        }, t.Configuration.prototype.get = function () {
            return this.config
        }, t.Configuration.prototype.reset = function () {
            this.config = {}
        }, lunr.SortedSet = function () {
            this.length = 0, this.elements = []
        }, lunr.SortedSet.load = function (e) {
            var t = new this;
            return t.elements = e, t.length = e.length, t
        }, lunr.SortedSet.prototype.add = function () {
            var e, t;
            for (e = 0; e < arguments.length; e++) t = arguments[e], ~this.indexOf(t) || this.elements.splice(this.locationFor(t), 0, t);
            this.length = this.elements.length
        }, lunr.SortedSet.prototype.toArray = function () {
            return this.elements.slice()
        }, lunr.SortedSet.prototype.map = function (e, t) {
            return this.elements.map(e, t)
        }, lunr.SortedSet.prototype.forEach = function (e, t) {
            return this.elements.forEach(e, t)
        }, lunr.SortedSet.prototype.indexOf = function (e) {
            for (var t = 0, n = this.elements.length, i = n - t, o = t + Math.floor(i / 2), r = this.elements[o]; i > 1;) {
                if (r === e) return o;
                e > r && (t = o), r > e && (n = o), i = n - t, o = t + Math.floor(i / 2), r = this.elements[o]
            }
            return r === e ? o : -1
        }, lunr.SortedSet.prototype.locationFor = function (e) {
            for (var t = 0, n = this.elements.length, i = n - t, o = t + Math.floor(i / 2), r = this.elements[o]; i > 1;) e > r && (t = o), r > e && (n = o), i = n - t, o = t + Math.floor(i / 2), r = this.elements[o];
            return r > e ? o : e > r ? o + 1 : void 0
        }, lunr.SortedSet.prototype.intersect = function (e) {
            for (var t = new lunr.SortedSet, n = 0, i = 0, o = this.length, r = e.length, s = this.elements, u = e.elements; ;) {
                if (n > o - 1 || i > r - 1) break;
                s[n] !== u[i] ? s[n] < u[i] ? n++ : s[n] > u[i] && i++ : (t.add(s[n]), n++, i++)
            }
            return t
        }, lunr.SortedSet.prototype.clone = function () {
            var e = new lunr.SortedSet;
            return e.elements = this.toArray(), e.length = e.elements.length, e
        }, lunr.SortedSet.prototype.union = function (e) {
            var t, n, i;
            this.length >= e.length ? (t = this, n = e) : (t = e, n = this), i = t.clone();
            for (var o = 0, r = n.toArray(); o < r.length; o++) i.add(r[o]);
            return i
        }, lunr.SortedSet.prototype.toJSON = function () {
            return this.toArray()
        },function (e, t) {
            "function" == typeof define && define.amd ? define(t) : "object" == typeof exports ? module.exports = t() : e.elasticlunr = t()
        }(this, function () {
            return t
        })
    }();
    /** pdoc search index */const docs = [{
        "fullname": "tinyqsim",
        "modulename": "tinyqsim",
        "kind": "module",
        "doc": "<p></p>\n"
    }, {
        "fullname": "tinyqsim.arrow_fix",
        "modulename": "tinyqsim.arrow_fix",
        "kind": "module",
        "doc": "<p>Fix for Arrow3D problem introduced by matplotlib 3.5.\nSee: <a href=\"https://github.com/matplotlib/matplotlib/issues/21688\">https://github.com/matplotlib/matplotlib/issues/21688</a></p>\n"
    }, {
        "fullname": "tinyqsim.bloch",
        "modulename": "tinyqsim.bloch",
        "kind": "module",
        "doc": "<p>Prototype Bloch sphere.</p>\n\n<p>Licensed under MIT license: see LICENSE.txt\nCopyright (c) 2024 Jon Brumfitt</p>\n"
    }, {
        "fullname": "tinyqsim.bloch.SIZE",
        "modulename": "tinyqsim.bloch",
        "qualname": "SIZE",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "0.7"
    }, {
        "fullname": "tinyqsim.bloch.bloch_to_qubit",
        "modulename": "tinyqsim.bloch",
        "qualname": "bloch_to_qubit",
        "kind": "function",
        "doc": "<p>Convert Bloch sphere angles to a qubit.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>phi</strong>:  Bloch sphere 'phi' angle in radians</li>\n<li><strong>theta</strong>:  Bloch sphere 'theta' angle in radians</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>A qubit</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">phi</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"n\">theta</span><span class=\"p\">:</span> <span class=\"nb\">float</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.bloch.qubit_to_bloch",
        "modulename": "tinyqsim.bloch",
        "qualname": "qubit_to_bloch",
        "kind": "function",
        "doc": "<p>Convert qubit to Bloch sphere angles (phi, theta).</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>psi</strong>:  qubit state</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>Bloch sphere angles (phi, theta) in radians</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">psi</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">tuple</span><span class=\"p\">[</span><span class=\"nb\">float</span><span class=\"p\">,</span> <span class=\"nb\">float</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.bloch.random_bloch",
        "modulename": "tinyqsim.bloch",
        "qualname": "random_bloch",
        "kind": "function",
        "doc": "<p>Return random point on Bloch sphere.\n0 &lt;= theta &lt;= pi,  0 &lt;= phi &lt; 2*pi</p>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>phi, theta (radians)</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"return-annotation\">) -> <span class=\"nb\">tuple</span><span class=\"p\">[</span><span class=\"nb\">float</span><span class=\"p\">,</span> <span class=\"nb\">float</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.bloch.random_qubit",
        "modulename": "tinyqsim.bloch",
        "qualname": "random_qubit",
        "kind": "function",
        "doc": "<p>Return random qubit (uniformly distributed on Bloch sphere.\n0 &lt;= theta &lt;= pi,  0 &lt;= phi &lt; 2*pi</p>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>A qubit (uniformly distributed on Bloch sphere.)</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.bloch.plot_bloch",
        "modulename": "tinyqsim.bloch",
        "qualname": "plot_bloch",
        "kind": "function",
        "doc": "<p>Plot bloch sphere.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>phi</strong>:  Bloch sphere 'phi' angle in radians</li>\n<li><strong>theta</strong>:  Bloch sphere 'theta' angle in radians</li>\n<li><strong>scale</strong>:  scaling factor</li>\n<li><strong>azimuth</strong>:  view-point azimuth (radians)</li>\n<li><strong>elevation</strong>:  view-point elevation (radians)</li>\n<li><strong>save</strong>:  File name to save image (or None)</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">phi</span><span class=\"p\">:</span> <span class=\"nb\">float</span>,</span><span class=\"param\">\t<span class=\"n\">theta</span><span class=\"p\">:</span> <span class=\"nb\">float</span>,</span><span class=\"param\">\t<span class=\"n\">scale</span><span class=\"o\">=</span><span class=\"mi\">1</span>,</span><span class=\"param\">\t<span class=\"n\">azimuth</span><span class=\"o\">=</span><span class=\"mi\">35</span>,</span><span class=\"param\">\t<span class=\"n\">elevation</span><span class=\"o\">=</span><span class=\"mi\">10</span>,</span><span class=\"param\">\t<span class=\"n\">save</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.gates",
        "modulename": "tinyqsim.gates",
        "kind": "module",
        "doc": "<p>Quantum gates</p>\n\n<p>Licensed under MIT license: see LICENSE.txt\nCopyright (c) 2024 Jon Brumfitt</p>\n"
    }, {
        "fullname": "tinyqsim.gates.RT2",
        "modulename": "tinyqsim.gates",
        "qualname": "RT2",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "1.4142135623730951"
    }, {
        "fullname": "tinyqsim.gates.ID",
        "modulename": "tinyqsim.gates",
        "qualname": "ID",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[1, 0],\n       [0, 1]])"
    }, {
        "fullname": "tinyqsim.gates.X",
        "modulename": "tinyqsim.gates",
        "qualname": "X",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[0, 1],\n       [1, 0]])"
    }, {
        "fullname": "tinyqsim.gates.Y",
        "modulename": "tinyqsim.gates",
        "qualname": "Y",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[ 0.+0.j, -0.-1.j],\n       [ 0.+1.j,  0.+0.j]])"
    }, {
        "fullname": "tinyqsim.gates.Z",
        "modulename": "tinyqsim.gates",
        "qualname": "Z",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[ 1,  0],\n       [ 0, -1]])"
    }, {
        "fullname": "tinyqsim.gates.H",
        "modulename": "tinyqsim.gates",
        "qualname": "H",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[ 0.70710678,  0.70710678],\n       [ 0.70710678, -0.70710678]])"
    }, {
        "fullname": "tinyqsim.gates.S",
        "modulename": "tinyqsim.gates",
        "qualname": "S",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[1.+0.j, 0.+0.j],\n       [0.+0.j, 0.+1.j]])"
    }, {
        "fullname": "tinyqsim.gates.T",
        "modulename": "tinyqsim.gates",
        "qualname": "T",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[1.        +0.j        , 0.        +0.j        ],\n       [0.        +0.j        , 0.70710678+0.70710678j]])"
    }, {
        "fullname": "tinyqsim.gates.SX",
        "modulename": "tinyqsim.gates",
        "qualname": "SX",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[0.5+0.5j, 0.5-0.5j],\n       [0.5-0.5j, 0.5+0.5j]])"
    }, {
        "fullname": "tinyqsim.gates.SWAP",
        "modulename": "tinyqsim.gates",
        "qualname": "SWAP",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[1, 0, 0, 0],\n       [0, 0, 1, 0],\n       [0, 1, 0, 0],\n       [0, 0, 0, 1]])"
    }, {
        "fullname": "tinyqsim.gates.cu",
        "modulename": "tinyqsim.gates",
        "qualname": "cu",
        "kind": "function",
        "doc": "<p>Return controlled version of U (big endian).</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>u</strong>:  Unitary matrix of gate</li>\n<li><strong>n_controls</strong>:  Number of controls</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>The controlled-U gate</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">u</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>, </span><span class=\"param\"><span class=\"n\">n_controls</span><span class=\"o\">=</span><span class=\"mi\">1</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.gates.CX",
        "modulename": "tinyqsim.gates",
        "qualname": "CX",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[1, 0, 0, 0],\n       [0, 1, 0, 0],\n       [0, 0, 0, 1],\n       [0, 0, 1, 0]])"
    }, {
        "fullname": "tinyqsim.gates.CY",
        "modulename": "tinyqsim.gates",
        "qualname": "CY",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],\n       [ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j],\n       [ 0.+0.j,  0.+0.j,  0.+0.j, -0.-1.j],\n       [ 0.+0.j,  0.+0.j,  0.+1.j,  0.+0.j]])"
    }, {
        "fullname": "tinyqsim.gates.CZ",
        "modulename": "tinyqsim.gates",
        "qualname": "CZ",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[ 1,  0,  0,  0],\n       [ 0,  1,  0,  0],\n       [ 0,  0,  1,  0],\n       [ 0,  0,  0, -1]])"
    }, {
        "fullname": "tinyqsim.gates.CS",
        "modulename": "tinyqsim.gates",
        "qualname": "CS",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],\n       [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],\n       [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],\n       [0.+0.j, 0.+0.j, 0.+0.j, 0.+1.j]])"
    }, {
        "fullname": "tinyqsim.gates.CT",
        "modulename": "tinyqsim.gates",
        "qualname": "CT",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[1.        +0.j        , 0.        +0.j        ,\n        0.        +0.j        , 0.        +0.j        ],\n       [0.        +0.j        , 1.        +0.j        ,\n        0.        +0.j        , 0.        +0.j        ],\n       [0.        +0.j        , 0.        +0.j        ,\n        1.        +0.j        , 0.        +0.j        ],\n       [0.        +0.j        , 0.        +0.j        ,\n        0.        +0.j        , 0.70710678+0.70710678j]])"
    }, {
        "fullname": "tinyqsim.gates.CCX",
        "modulename": "tinyqsim.gates",
        "qualname": "CCX",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[1, 0, 0, 0, 0, 0, 0, 0],\n       [0, 1, 0, 0, 0, 0, 0, 0],\n       [0, 0, 1, 0, 0, 0, 0, 0],\n       [0, 0, 0, 1, 0, 0, 0, 0],\n       [0, 0, 0, 0, 1, 0, 0, 0],\n       [0, 0, 0, 0, 0, 1, 0, 0],\n       [0, 0, 0, 0, 0, 0, 0, 1],\n       [0, 0, 0, 0, 0, 0, 1, 0]])"
    }, {
        "fullname": "tinyqsim.gates.CSWAP",
        "modulename": "tinyqsim.gates",
        "qualname": "CSWAP",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "array([[1, 0, 0, 0, 0, 0, 0, 0],\n       [0, 1, 0, 0, 0, 0, 0, 0],\n       [0, 0, 1, 0, 0, 0, 0, 0],\n       [0, 0, 0, 1, 0, 0, 0, 0],\n       [0, 0, 0, 0, 1, 0, 0, 0],\n       [0, 0, 0, 0, 0, 0, 1, 0],\n       [0, 0, 0, 0, 0, 1, 0, 0],\n       [0, 0, 0, 0, 0, 0, 0, 1]])"
    }, {
        "fullname": "tinyqsim.gates.P",
        "modulename": "tinyqsim.gates",
        "qualname": "P",
        "kind": "function",
        "doc": "<p>Phase gate: Rotation by 'phi radians about Z axis.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>phi</strong>:  Phase angle in radians</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>the phase gate</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">phi</span><span class=\"p\">:</span> <span class=\"nb\">float</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.gates.CP",
        "modulename": "tinyqsim.gates",
        "qualname": "CP",
        "kind": "function",
        "doc": "<p>Controlled phase gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>phi</strong>:  Phase angle in radians</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>the controlled-phase gate</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">phi</span><span class=\"p\">:</span> <span class=\"nb\">float</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.gates.RX",
        "modulename": "tinyqsim.gates",
        "qualname": "RX",
        "kind": "function",
        "doc": "<p>RX gate: Rotation by 'theta' radians about X axis.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>theta</strong>:  angle in radians</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>the gate</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">theta</span><span class=\"p\">:</span> <span class=\"nb\">float</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.gates.RY",
        "modulename": "tinyqsim.gates",
        "qualname": "RY",
        "kind": "function",
        "doc": "<p>RY gate: Rotation by 'theta' radians about Y axis.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>theta</strong>:  angle in radians</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>the gate</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">theta</span><span class=\"p\">:</span> <span class=\"nb\">float</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.gates.GATES",
        "modulename": "tinyqsim.gates",
        "qualname": "GATES",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "{&#x27;CCX&#x27;: array([[1, 0, 0, 0, 0, 0, 0, 0],\n       [0, 1, 0, 0, 0, 0, 0, 0],\n       [0, 0, 1, 0, 0, 0, 0, 0],\n       [0, 0, 0, 1, 0, 0, 0, 0],\n       [0, 0, 0, 0, 1, 0, 0, 0],\n       [0, 0, 0, 0, 0, 1, 0, 0],\n       [0, 0, 0, 0, 0, 0, 0, 1],\n       [0, 0, 0, 0, 0, 0, 1, 0]]), &#x27;CP&#x27;: &lt;function CP&gt;, &#x27;CS&#x27;: array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],\n       [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],\n       [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j],\n       [0.+0.j, 0.+0.j, 0.+0.j, 0.+1.j]]), &#x27;CSWAP&#x27;: array([[1, 0, 0, 0, 0, 0, 0, 0],\n       [0, 1, 0, 0, 0, 0, 0, 0],\n       [0, 0, 1, 0, 0, 0, 0, 0],\n       [0, 0, 0, 1, 0, 0, 0, 0],\n       [0, 0, 0, 0, 1, 0, 0, 0],\n       [0, 0, 0, 0, 0, 0, 1, 0],\n       [0, 0, 0, 0, 0, 1, 0, 0],\n       [0, 0, 0, 0, 0, 0, 0, 1]]), &#x27;CT&#x27;: array([[1.        +0.j        , 0.        +0.j        ,\n        0.        +0.j        , 0.        +0.j        ],\n       [0.        +0.j        , 1.        +0.j        ,\n        0.        +0.j        , 0.        +0.j        ],\n       [0.        +0.j        , 0.        +0.j        ,\n        1.        +0.j        , 0.        +0.j        ],\n       [0.        +0.j        , 0.        +0.j        ,\n        0.        +0.j        , 0.70710678+0.70710678j]]), &#x27;CX&#x27;: array([[1, 0, 0, 0],\n       [0, 1, 0, 0],\n       [0, 0, 0, 1],\n       [0, 0, 1, 0]]), &#x27;CY&#x27;: array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],\n       [ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j],\n       [ 0.+0.j,  0.+0.j,  0.+0.j, -0.-1.j],\n       [ 0.+0.j,  0.+0.j,  0.+1.j,  0.+0.j]]), &#x27;CZ&#x27;: array([[ 1,  0,  0,  0],\n       [ 0,  1,  0,  0],\n       [ 0,  0,  1,  0],\n       [ 0,  0,  0, -1]]), &#x27;H&#x27;: array([[ 0.70710678,  0.70710678],\n       [ 0.70710678, -0.70710678]]), &#x27;I&#x27;: array([[1, 0],\n       [0, 1]]), &#x27;P&#x27;: &lt;function P&gt;, &#x27;RX&#x27;: &lt;function RX&gt;, &#x27;RY&#x27;: &lt;function RY&gt;, &#x27;S&#x27;: array([[1.+0.j, 0.+0.j],\n       [0.+0.j, 0.+1.j]]), &#x27;SX&#x27;: array([[0.5+0.5j, 0.5-0.5j],\n       [0.5-0.5j, 0.5+0.5j]]), &#x27;SWAP&#x27;: array([[1, 0, 0, 0],\n       [0, 0, 1, 0],\n       [0, 1, 0, 0],\n       [0, 0, 0, 1]]), &#x27;T&#x27;: array([[1.        +0.j        , 0.        +0.j        ],\n       [0.        +0.j        , 0.70710678+0.70710678j]]), &#x27;X&#x27;: array([[0, 1],\n       [1, 0]]), &#x27;Y&#x27;: array([[ 0.+0.j, -0.-1.j],\n       [ 0.+1.j,  0.+0.j]]), &#x27;Z&#x27;: array([[ 1,  0],\n       [ 0, -1]])}"
    }, {
        "fullname": "tinyqsim.model",
        "modulename": "tinyqsim.model",
        "kind": "module",
        "doc": "<p>Model for quantum circuit.</p>\n\n<p>Licensed under MIT license: see LICENSE.txt\nCopyright (c) 2024 Jon Brumfitt</p>\n"
    }, {
        "fullname": "tinyqsim.model.Model",
        "modulename": "tinyqsim.model",
        "qualname": "Model",
        "kind": "class",
        "doc": "<p>Model for quantum circuit.</p>\n"
    }, {
        "fullname": "tinyqsim.model.Model.__init__",
        "modulename": "tinyqsim.model",
        "qualname": "Model.__init__",
        "kind": "function",
        "doc": "<p>Initialize circuit model.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>nqubits</strong>:  Number of qubits.</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">nqubits</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span>)</span>"
    }, {
        "fullname": "tinyqsim.model.Model.nqubits",
        "modulename": "tinyqsim.model",
        "qualname": "Model.nqubits",
        "kind": "variable",
        "doc": "<p></p>\n"
    }, {
        "fullname": "tinyqsim.model.Model.items",
        "modulename": "tinyqsim.model",
        "qualname": "Model.items",
        "kind": "variable",
        "doc": "<p></p>\n",
        "annotation": ": list[str, list[int], list]"
    }, {
        "fullname": "tinyqsim.model.Model.add_gate",
        "modulename": "tinyqsim.model",
        "qualname": "Model.add_gate",
        "kind": "function",
        "doc": "<p>Add gate to circuit.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>name</strong>:  Name of gate</li>\n<li><strong>qubits</strong>:  qubits to which gate is applied</li>\n<li><strong>params</strong>:   parameters</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">name</span><span class=\"p\">:</span> <span class=\"nb\">str</span>, </span><span class=\"param\"><span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span>, </span><span class=\"param\"><span class=\"n\">params</span><span class=\"o\">=</span><span class=\"kc\">None</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.plotting",
        "modulename": "tinyqsim.plotting",
        "kind": "module",
        "doc": "<p>Plotting routines.</p>\n\n<p>Licensed under MIT license: see LICENSE.txt\nCopyright (c) 2024 Jon Brumfitt</p>\n"
    }, {
        "fullname": "tinyqsim.plotting.plot_histogram",
        "modulename": "tinyqsim.plotting",
        "qualname": "plot_histogram",
        "kind": "function",
        "doc": "<p>Plot histogram of data.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>data</strong>:  The data to plot</li>\n<li><strong>save</strong>:  File name to save image (or None)</li>\n<li><strong>ylabel</strong>:  Label for the Y-axis</li>\n<li><strong>height</strong>:  Height of the plot in inches</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">data</span>, </span><span class=\"param\"><span class=\"n\">save</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"kc\">False</span>, </span><span class=\"param\"><span class=\"n\">ylabel</span><span class=\"o\">=</span><span class=\"kc\">None</span>, </span><span class=\"param\"><span class=\"n\">height</span><span class=\"o\">=</span><span class=\"mf\">2.5</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit",
        "modulename": "tinyqsim.qcircuit",
        "kind": "module",
        "doc": "<p>Quantum Circuit.</p>\n\n<p>Licensed under MIT license: see LICENSE.txt\nCopyright (c) 2024 Jon Brumfitt</p>\n"
    }, {
        "fullname": "tinyqsim.qcircuit.EPS",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "EPS",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "1e-12"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit",
        "kind": "class",
        "doc": "<p>Class representing a quantum circuit.</p>\n\n<p>QCircuit ties together all the components of a quantum simulation\nand presents them as a quantum circuit with methods to add gates\nand perform measurements.</p>\n"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.__init__",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.__init__",
        "kind": "function",
        "doc": "<p>Initialize QCircuit.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>nqubits: number of qubits</li>\n<li>init: initialization 'zeros' or 'random'</li>\n<li>auto_exec: Enable on-the-fly execution</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">nqubits</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">init</span><span class=\"o\">=</span><span class=\"s1\">&#39;zeros&#39;</span>, </span><span class=\"param\"><span class=\"n\">auto_exec</span><span class=\"o\">=</span><span class=\"kc\">True</span></span>)</span>"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.version",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.version",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&#x27;0.0.1&#x27;"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.state_vector",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.state_vector",
        "kind": "variable",
        "doc": "<p>Return copy of the quantum state vector.</p>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>copy of quantum state vector</p>\n</blockquote>\n",
        "annotation": ": numpy.ndarray"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.n_qubits",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.n_qubits",
        "kind": "variable",
        "doc": "<p>Return the number of qubits.</p>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>number of qbits</p>\n</blockquote>\n",
        "annotation": ": int"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.components",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.components",
        "kind": "function",
        "doc": "<p>Return complex components of state vector as a dictionary.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>decimals</strong>:  number of decimal places (default=5)</li>\n<li><strong>include_zeros</strong>:  True to include zero values (default=False)</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>Dictionary of state components</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">decimals</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">=</span> <span class=\"mi\">5</span>, </span><span class=\"param\"><span class=\"n\">include_zeros</span><span class=\"p\">:</span> <span class=\"nb\">bool</span> <span class=\"o\">=</span> <span class=\"kc\">False</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">dict</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.counts",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.counts",
        "kind": "function",
        "doc": "<p>Return measurement counts for repeated experiment.\nThe state is not changed (collapsed).\n            :param qubits: list of qubits</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>runs</strong>:  Number of test runs (default=1000)</li>\n<li><strong>include_zeros</strong>:  True to include zero values (default=False)</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>frequencies of outcomes as a dictionary</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">runs</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">=</span> <span class=\"mi\">1000</span>,</span><span class=\"param\">\t<span class=\"n\">include_zeros</span><span class=\"p\">:</span> <span class=\"nb\">bool</span> <span class=\"o\">=</span> <span class=\"kc\">False</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">dict</span><span class=\"p\">[</span><span class=\"nb\">str</span><span class=\"p\">,</span> <span class=\"nb\">int</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.probabilities",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.probabilities",
        "kind": "function",
        "doc": "<p>Return dictionary of the probabilities of each outcome.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>qubits</strong>:  list of qubits</li>\n<li><strong>decimals</strong>:  number of decimal places (default=5)</li>\n<li><strong>include_zeros</strong>:  True to include zero values (default=False)</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>dictionary of outcome->probability</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"n\">Iterable</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">decimals</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">=</span> <span class=\"mi\">5</span>,</span><span class=\"param\">\t<span class=\"n\">include_zeros</span><span class=\"p\">:</span> <span class=\"nb\">bool</span> <span class=\"o\">=</span> <span class=\"kc\">False</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">dict</span><span class=\"p\">[</span><span class=\"nb\">str</span><span class=\"p\">,</span> <span class=\"nb\">float</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.measure",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.measure",
        "kind": "function",
        "doc": "<p>Add a measurement gate to one or more qubits.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>qubits</strong>:  list of qubits</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"n\">Iterable</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.draw",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.draw",
        "kind": "function",
        "doc": "<p>Draw the quantum circuit.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>scale: scale factor (default=1)</li>\n<li>show: show the quantum circuit</li>\n<li>save: file to save image if required</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">scale</span><span class=\"p\">:</span> <span class=\"nb\">float</span> <span class=\"o\">=</span> <span class=\"mi\">1</span>,</span><span class=\"param\">\t<span class=\"n\">show</span><span class=\"p\">:</span> <span class=\"nb\">bool</span> <span class=\"o\">=</span> <span class=\"kc\">True</span>,</span><span class=\"param\">\t<span class=\"n\">save</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.plot_probabilities",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.plot_probabilities",
        "kind": "function",
        "doc": "<p>Plot histogram of probabilities for list of qubits.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>qubits</strong>:  list of qubits (None =&gt; all)</li>\n<li><strong>save</strong>:  file to save image if required</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"n\">Iterable</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>, </span><span class=\"param\"><span class=\"n\">save</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">False</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.plot_counts",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.plot_counts",
        "kind": "function",
        "doc": "<p>Plot histogram of measurement counts.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>qubits</strong>:  list of qubits</li>\n<li><strong>runs</strong>:  number of test runs (default=1000)</li>\n<li><strong>save</strong>:  file to save image if required</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">runs</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">=</span> <span class=\"mi\">1000</span>,</span><span class=\"param\">\t<span class=\"n\">save</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">|</span> <span class=\"kc\">None</span> <span class=\"o\">=</span> <span class=\"kc\">False</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.ccu",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.ccu",
        "kind": "function",
        "doc": "<p>Add a controlled-controlled-U (CCU) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>name</strong>:  name of the gate</li>\n<li><strong>u</strong>:  unitary matrix</li>\n<li><strong>qubits</strong>:  list of qubits</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">u</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>, </span><span class=\"param\"><span class=\"n\">name</span><span class=\"p\">:</span> <span class=\"nb\">str</span>, </span><span class=\"param\"><span class=\"o\">*</span><span class=\"n\">qubits</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.ccx",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.ccx",
        "kind": "function",
        "doc": "<p>Add a controlled-controlled-X (CCX) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>c1</strong>:  control qubit</li>\n<li><strong>c2</strong>:  target qubit</li>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">c1</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">c2</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.cp",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.cp",
        "kind": "function",
        "doc": "<p>Add a controlled-phase (CP) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>phi</strong>:  phase angle</li>\n<li><strong>phi_text</strong>:  text of phase angle</li>\n<li><strong>c</strong>:  control qubit</li>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">phi</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"n\">phi_text</span><span class=\"p\">:</span> <span class=\"nb\">str</span>, </span><span class=\"param\"><span class=\"n\">c</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.cs",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.cs",
        "kind": "function",
        "doc": "<p>Add a controlled-S (CS) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>c</strong>:  control qubit</li>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">c</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.cswap",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.cswap",
        "kind": "function",
        "doc": "<p>Add a controlled-swap (CSWAP) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>c</strong>:  control qubit</li>\n<li><strong>t1</strong>:  target qubit</li>\n<li><strong>t2</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">c</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">t1</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">t2</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.ct",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.ct",
        "kind": "function",
        "doc": "<p>Add a controlled-T (CT) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>c</strong>:  control qubit</li>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">c</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.cu",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.cu",
        "kind": "function",
        "doc": "<p>Add a controlled-U (CU) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>u</strong>:  unitary matrix</li>\n<li><strong>name</strong>:  name of the gate</li>\n<li><strong>qubits</strong>:  list of qubits</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">u</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>, </span><span class=\"param\"><span class=\"n\">name</span><span class=\"p\">:</span> <span class=\"nb\">str</span>, </span><span class=\"param\"><span class=\"o\">*</span><span class=\"n\">qubits</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.cx",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.cx",
        "kind": "function",
        "doc": "<p>Add a controlled-X (CX) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>c</strong>:  control qubit</li>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">c</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.cy",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.cy",
        "kind": "function",
        "doc": "<p>Add a controlled-Y (CY) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>c</strong>:  control qubit</li>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">c</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.cz",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.cz",
        "kind": "function",
        "doc": "<p>Add a controlled-Z (CZ) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>c</strong>:  control qubit</li>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">c</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.h",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.h",
        "kind": "function",
        "doc": "<p>Add a Hadamard (H) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.i",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.i",
        "kind": "function",
        "doc": "<p>Add an identity (I) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.p",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.p",
        "kind": "function",
        "doc": "<p>Add a phase (P) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>phi</strong>:  phase angle</li>\n<li><strong>phi_text</strong>:  text value of phase angle</li>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">phi</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"n\">phi_text</span><span class=\"p\">:</span> <span class=\"nb\">str</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.rx",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.rx",
        "kind": "function",
        "doc": "<p>Add an RX gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>theta</strong>:  target qubit</li>\n<li><strong>theta_text</strong>:  text value of phase angle</li>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">theta</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"n\">theta_text</span><span class=\"p\">:</span> <span class=\"nb\">str</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.ry",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.ry",
        "kind": "function",
        "doc": "<p>Add an RY gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>theta</strong>:  target qubit</li>\n<li><strong>theta_text</strong>:  text value of phase angle</li>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">theta</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"n\">theta_text</span><span class=\"p\">:</span> <span class=\"nb\">str</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.s",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.s",
        "kind": "function",
        "doc": "<p>Add an S gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.swap",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.swap",
        "kind": "function",
        "doc": "<p>Add a swap (SWAP) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>t1</strong>:  target qubit</li>\n<li><strong>t2</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">t1</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">t2</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.sx",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.sx",
        "kind": "function",
        "doc": "<p>Add a sqrt(X) gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.t",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.t",
        "kind": "function",
        "doc": "<p>Add a T gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.u",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.u",
        "kind": "function",
        "doc": "<p>Add a custom unitary gate (U).</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>u</strong>:  unitary matrix</li>\n<li><strong>name</strong>:  name of the gate</li>\n<li><strong>qubits</strong>:  list of qubits</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">u</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>, </span><span class=\"param\"><span class=\"n\">name</span><span class=\"p\">:</span> <span class=\"nb\">str</span>, </span><span class=\"param\"><span class=\"o\">*</span><span class=\"n\">qubits</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.x",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.x",
        "kind": "function",
        "doc": "<p>Add an X gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.y",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.y",
        "kind": "function",
        "doc": "<p>Add a Y gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.z",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.z",
        "kind": "function",
        "doc": "<p>Add a Z gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>t</strong>:  target qubit</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.qcircuit.QCircuit.barrier",
        "modulename": "tinyqsim.qcircuit",
        "qualname": "QCircuit.barrier",
        "kind": "function",
        "doc": "<p>Add a barrier to the circuit.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum",
        "modulename": "tinyqsim.quantum",
        "kind": "module",
        "doc": "<p>Functions for working with qubits and quantum states.</p>\n\n<p>Licensed under MIT license: see LICENSE.txt\nCopyright (c) 2024 Jon Brumfitt</p>\n"
    }, {
        "fullname": "tinyqsim.quantum.init_state",
        "modulename": "tinyqsim.quantum",
        "qualname": "init_state",
        "kind": "function",
        "doc": "<p>Initialize an N-qubit state to all |0>.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>n</strong>:  number of qubits</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>the initialized state vector</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">n</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.random_state",
        "modulename": "tinyqsim.quantum",
        "qualname": "random_state",
        "kind": "function",
        "doc": "<p>Return a random pure state vector.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>nqubits</strong>:  number of qubits</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>random quantum state vector</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">nqubits</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.n_qubits",
        "modulename": "tinyqsim.quantum",
        "qualname": "n_qubits",
        "kind": "function",
        "doc": "<p>Return the number of qubits of a state or unitary matrix.\nThe argument should be a power of two.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>a</strong>:  state or unitary matrix</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>number of qubits</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">a</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">int</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.basis_names",
        "modulename": "tinyqsim.quantum",
        "qualname": "basis_names",
        "kind": "function",
        "doc": "<p>Return list of integers &lt; 2**nqubits as binary strings.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>nqubits</strong>:  number of qubits</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>list of integers as binary strings</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">nqubits</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">str</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.state_to_tensor",
        "modulename": "tinyqsim.quantum",
        "qualname": "state_to_tensor",
        "kind": "function",
        "doc": "<p>Convert state vector to tensor representation.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>a</strong>:  state vector</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>tensor representation of state</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">a</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.tensor_to_state",
        "modulename": "tinyqsim.quantum",
        "qualname": "tensor_to_state",
        "kind": "function",
        "doc": "<p>Convert tensor into a state vector.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>t</strong>:  tensor representation of state</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>state vector</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">t</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.unitary_to_tensor",
        "modulename": "tinyqsim.quantum",
        "qualname": "unitary_to_tensor",
        "kind": "function",
        "doc": "<p>Convert unitary matrix to tensor representation.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>u</strong>:  unitary matrix</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>tensor representation of unitary</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">u</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.apply_tensor",
        "modulename": "tinyqsim.quantum",
        "qualname": "apply_tensor",
        "kind": "function",
        "doc": "<p>Apply tensor of unitary to specified qubits of state.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>tv</strong>:  quantum state tensor</li>\n<li><strong>tu</strong>:  tensor of unitary</li>\n<li><strong>qubits</strong>:  list of qubits</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>updated state tensor</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">tv</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>, </span><span class=\"param\"><span class=\"n\">tu</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>, </span><span class=\"param\"><span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.sum_except_qubits",
        "modulename": "tinyqsim.quantum",
        "qualname": "sum_except_qubits",
        "kind": "function",
        "doc": "<p>Sum data over indices except those in 'qubits'.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>data</strong>:  data to sum</li>\n<li><strong>qubits</strong>:  list of qubits to retain</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>summed data</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">data</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>, </span><span class=\"param\"><span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"n\">Iterable</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.components_dict",
        "modulename": "tinyqsim.quantum",
        "qualname": "components_dict",
        "kind": "function",
        "doc": "<p>Return complex components of the state vector.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>state</strong>:  State vector</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>Dictionary of state components</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">state</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">dict</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.probabilities",
        "modulename": "tinyqsim.quantum",
        "qualname": "probabilities",
        "kind": "function",
        "doc": "<p>Return the probabilities of each outcome.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>state</strong>:  State vector</li>\n<li><strong>qubits</strong>:  List of qubit indices</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>list of probabilities</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">state</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>, </span><span class=\"param\"><span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"n\">Iterable</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.probability_dict",
        "modulename": "tinyqsim.quantum",
        "qualname": "probability_dict",
        "kind": "function",
        "doc": "<p>Return dictionary of the probabilities of each outcome.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>state</strong>:  State vector</li>\n<li><strong>qubits</strong>:  List of qubit indices</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>dictionary of outcome->probability</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">state</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>,</span><span class=\"param\">\t<span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"n\">Optional</span><span class=\"p\">[</span><span class=\"n\">Iterable</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]]</span> <span class=\"o\">=</span> <span class=\"mi\">0</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">dict</span><span class=\"p\">[</span><span class=\"nb\">str</span><span class=\"p\">,</span> <span class=\"nb\">float</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.counts_dict",
        "modulename": "tinyqsim.quantum",
        "qualname": "counts_dict",
        "kind": "function",
        "doc": "<p>Return measurement counts for repeated experiment.\nThe state is not changed (collapsed).</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>state</strong>:  State vector</li>\n<li><strong>qubits</strong>:  List of qubits</li>\n<li><strong>runs</strong>:  Number of test runs (default=1000)</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>Dictionary of counts for each state</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">state</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>,</span><span class=\"param\">\t<span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span>,</span><span class=\"param\">\t<span class=\"n\">runs</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">=</span> <span class=\"mi\">1000</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">dict</span><span class=\"p\">[</span><span class=\"nb\">str</span><span class=\"p\">,</span> <span class=\"nb\">int</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.measure_qubit",
        "modulename": "tinyqsim.quantum",
        "qualname": "measure_qubit",
        "kind": "function",
        "doc": "<p>Measure a single qubit of a state vector with collapse.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>state</strong>:  State vector</li>\n<li><strong>index</strong>:  Index of qubit</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>(measured, new_state) where 'measured' is the measured value</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">state</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>, </span><span class=\"param\"><span class=\"n\">index</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">=</span> <span class=\"mi\">0</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">tuple</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">,</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.quantum.measure_qubits",
        "modulename": "tinyqsim.quantum",
        "qualname": "measure_qubits",
        "kind": "function",
        "doc": "<p>Measure a list of qubits with collapse.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>state</strong>:  Initial state vector</li>\n<li><strong>indices</strong>:  List of qubit indices</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>(bits, new_state) where bits is list of measured values</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"n\">state</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>,</span><span class=\"param\">\tindices: [&lt;class &#x27;int&#x27;&gt;]</span><span class=\"return-annotation\">) -> <span class=\"nb\">tuple</span><span class=\"p\">[</span><span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span><span class=\"p\">,</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic",
        "modulename": "tinyqsim.schematic",
        "kind": "module",
        "doc": "<p>Graphics for QCircuit Schematic.</p>\n\n<p>Licensed under MIT license: see LICENSE.txt\nCopyright (c) 2024 Jon Brumfitt</p>\n"
    }, {
        "fullname": "tinyqsim.schematic.UNITS_PER_CM",
        "modulename": "tinyqsim.schematic",
        "qualname": "UNITS_PER_CM",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "10"
    }, {
        "fullname": "tinyqsim.schematic.CM_PER_IN",
        "modulename": "tinyqsim.schematic",
        "qualname": "CM_PER_IN",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "2.54"
    }, {
        "fullname": "tinyqsim.schematic.QUBIT_PITCH",
        "modulename": "tinyqsim.schematic",
        "qualname": "QUBIT_PITCH",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "18"
    }, {
        "fullname": "tinyqsim.schematic.XSTEP",
        "modulename": "tinyqsim.schematic",
        "qualname": "XSTEP",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "18"
    }, {
        "fullname": "tinyqsim.schematic.HBW",
        "modulename": "tinyqsim.schematic",
        "qualname": "HBW",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "5"
    }, {
        "fullname": "tinyqsim.schematic.BW",
        "modulename": "tinyqsim.schematic",
        "qualname": "BW",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "10"
    }, {
        "fullname": "tinyqsim.schematic.LEFT_MARGIN",
        "modulename": "tinyqsim.schematic",
        "qualname": "LEFT_MARGIN",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "6"
    }, {
        "fullname": "tinyqsim.schematic.TOP_MARGIN",
        "modulename": "tinyqsim.schematic",
        "qualname": "TOP_MARGIN",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "1"
    }, {
        "fullname": "tinyqsim.schematic.BOTTOM_MARGIN",
        "modulename": "tinyqsim.schematic",
        "qualname": "BOTTOM_MARGIN",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "4"
    }, {
        "fullname": "tinyqsim.schematic.FONT_SIZE",
        "modulename": "tinyqsim.schematic",
        "qualname": "FONT_SIZE",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "13"
    }, {
        "fullname": "tinyqsim.schematic.TINY_FONT",
        "modulename": "tinyqsim.schematic",
        "qualname": "TINY_FONT",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "11"
    }, {
        "fullname": "tinyqsim.schematic.G_COLOR",
        "modulename": "tinyqsim.schematic",
        "qualname": "G_COLOR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&#x27;b&#x27;"
    }, {
        "fullname": "tinyqsim.schematic.H_COLOR",
        "modulename": "tinyqsim.schematic",
        "qualname": "H_COLOR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&#x27;#00A000&#x27;"
    }, {
        "fullname": "tinyqsim.schematic.BARRIER_COLOR",
        "modulename": "tinyqsim.schematic",
        "qualname": "BARRIER_COLOR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&#x27;#A0A0A0&#x27;"
    }, {
        "fullname": "tinyqsim.schematic.QUBIT_COLOR",
        "modulename": "tinyqsim.schematic",
        "qualname": "QUBIT_COLOR",
        "kind": "variable",
        "doc": "<p></p>\n",
        "default_value": "&#x27;k&#x27;"
    }, {
        "fullname": "tinyqsim.schematic.Scheduler",
        "modulename": "tinyqsim.schematic",
        "qualname": "Scheduler",
        "kind": "class",
        "doc": "<p>Simple time-slot scheduler for placing gates in schematic.</p>\n"
    }, {
        "fullname": "tinyqsim.schematic.Scheduler.schedule",
        "modulename": "tinyqsim.schematic",
        "qualname": "Scheduler.schedule",
        "kind": "function",
        "doc": "<p>Pack qubits into a slot.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>qubits</strong>:  Qubits of gate</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>Slot number for the gate</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">qubits</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">int</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic",
        "kind": "class",
        "doc": "<p>QCircuit Schematic.</p>\n"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.__init__",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.__init__",
        "kind": "function",
        "doc": "<p>Initialize Schematic.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>nqubits: number of qubits</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">nqubits</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span>)</span>"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw",
        "kind": "function",
        "doc": "<p>Draw the quantum circuit.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>model: QCircuit model</li>\n<li>scale: scale factor</li>\n<li>show: show quantum circuit</li>\n<li>save: File name to save image (or None)</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">model</span>,</span><span class=\"param\">\t<span class=\"n\">scale</span><span class=\"p\">:</span> <span class=\"nb\">float</span> <span class=\"o\">=</span> <span class=\"mi\">1</span>,</span><span class=\"param\">\t<span class=\"n\">show</span><span class=\"p\">:</span> <span class=\"nb\">bool</span> <span class=\"o\">=</span> <span class=\"kc\">True</span>,</span><span class=\"param\">\t<span class=\"n\">save</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"kc\">None</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_qubit_lines",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_qubit_lines",
        "kind": "function",
        "doc": "<p>Draw the qubit lines.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>xlength: Length of qubit lines</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">xlength</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_gate",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_gate",
        "kind": "function",
        "doc": "<p>Draw a gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>name: name of gate</li>\n<li>x: x position</li>\n<li>cqubits: list of control qubits</li>\n<li>tqubits: list of target qubits</li>\n<li>params: parameters</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">name</span><span class=\"p\">:</span> <span class=\"nb\">str</span>,</span><span class=\"param\">\t<span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span>,</span><span class=\"param\">\t<span class=\"n\">cqubits</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span>,</span><span class=\"param\">\t<span class=\"n\">tqubits</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span>,</span><span class=\"param\">\t<span class=\"n\">params</span><span class=\"o\">=</span><span class=\"kc\">None</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_generic_gate",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_generic_gate",
        "kind": "function",
        "doc": "<p>Draw a generic rectangular gate.\n    The gate can have any number of qubits, controls and an annotation\n    (e.g. for rotation angle).</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>x</strong>:  horizontal position</li>\n<li><strong>text</strong>:  name of gate</li>\n<li><strong>cqubits</strong>:  list of control qubits</li>\n<li><strong>qubits</strong>:  list of target qubits</li>\n<li><strong>label</strong>:  label to annotate the gate</li>\n<li><strong>color</strong>:  fill color of box</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span>,</span><span class=\"param\">\t<span class=\"n\">text</span><span class=\"p\">:</span> <span class=\"nb\">str</span>,</span><span class=\"param\">\t<span class=\"n\">cqubits</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span>,</span><span class=\"param\">\t<span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span>,</span><span class=\"param\">\t<span class=\"n\">label</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">color</span><span class=\"o\">=</span><span class=\"s1\">&#39;w&#39;</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_cx_gate",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_cx_gate",
        "kind": "function",
        "doc": "<p>Draw CX gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>x: x position</li>\n<li>q1: qubit 1 (control)</li>\n<li>q2: qubit 2 (target)</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"n\">q1</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">q2</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_cz_gate",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_cz_gate",
        "kind": "function",
        "doc": "<p>Draw CZ gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>x: x position</li>\n<li>q1: qubit 1 (control)</li>\n<li>q2: qubit 2 I(target)</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"n\">q1</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">q2</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_swap_gate",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_swap_gate",
        "kind": "function",
        "doc": "<p>Draw SWAP gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>x: x position</li>\n<li>q1: qubit 1</li>\n<li>q2: qubit 2</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_ccx_gate",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_ccx_gate",
        "kind": "function",
        "doc": "<p>Draw CCX gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>x: x position</li>\n<li>q1: qubit 1 (control 1)</li>\n<li>q2: qubit 2 (control 2)</li>\n<li>q3: qubit 3 (target)</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"n\">q1</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">q2</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">q3</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_cswap_gate",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_cswap_gate",
        "kind": "function",
        "doc": "<p>Draw CSWAP gate.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>x: x position</li>\n<li>q1: qubit 1 (control)</li>\n<li>q2: qubit 2 (target 1)</li>\n<li>q3: qubit 3 (target 2)</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"n\">q1</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">q2</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">q3</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_meters",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_meters",
        "kind": "function",
        "doc": "<p>Draw measurement 'gate' as meter symbols.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>x: x position</li>\n<li>qubits: list of qubits</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"o\">*</span><span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_barrier",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_barrier",
        "kind": "function",
        "doc": "<p>Draw barrier.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>x: x position</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_square",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_square",
        "kind": "function",
        "doc": "<p>Draw square gate symbol.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>x: x position</li>\n<li>qubit: qubit index</li>\n<li>text: Text to go in rectangle</li>\n<li>color: color</li>\n<li>fontsize: fontsize</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span>,</span><span class=\"param\">\t<span class=\"n\">qubit</span><span class=\"p\">:</span> <span class=\"nb\">int</span>,</span><span class=\"param\">\t<span class=\"n\">text</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">color</span><span class=\"o\">=</span><span class=\"s1\">&#39;w&#39;</span>,</span><span class=\"param\">\t<span class=\"n\">fontsize</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">=</span> <span class=\"mi\">13</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_circle",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_circle",
        "kind": "function",
        "doc": "<p>Draw circle.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>x: x position</li>\n<li>qubit: qubit index</li>\n<li>r: radius</li>\n<li>text: Text to go in circle</li>\n<li>color: color</li>\n<li>fontsize: fontsize</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code multiline\">(<span class=\"param\">\t<span class=\"bp\">self</span>,</span><span class=\"param\">\t<span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span>,</span><span class=\"param\">\t<span class=\"n\">qubit</span><span class=\"p\">:</span> <span class=\"nb\">int</span>,</span><span class=\"param\">\t<span class=\"n\">r</span><span class=\"o\">=</span><span class=\"mi\">5</span>,</span><span class=\"param\">\t<span class=\"n\">text</span><span class=\"p\">:</span> <span class=\"nb\">str</span> <span class=\"o\">=</span> <span class=\"kc\">None</span>,</span><span class=\"param\">\t<span class=\"n\">color</span><span class=\"o\">=</span><span class=\"s1\">&#39;w&#39;</span>,</span><span class=\"param\">\t<span class=\"n\">fontsize</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">=</span> <span class=\"mi\">13</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_dot",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_dot",
        "kind": "function",
        "doc": "<p>Draw dot.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>x: x position</li>\n<li>qubit: qubit index</li>\n<li>r: radious</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"n\">qubit</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">r</span><span class=\"p\">:</span> <span class=\"nb\">float</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_cross",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_cross",
        "kind": "function",
        "doc": "<p>Draw cross.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>x: x position</li>\n<li>qubit: qubit index</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"n\">qubit</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.schematic.Schematic.draw_vline",
        "modulename": "tinyqsim.schematic",
        "qualname": "Schematic.draw_vline",
        "kind": "function",
        "doc": "<p>Draw vertical line between two qubit lines.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li>x: x position</li>\n<li>q1: qubit 1</li>\n<li>q2: qubit 2</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">x</span><span class=\"p\">:</span> <span class=\"nb\">float</span>, </span><span class=\"param\"><span class=\"n\">q1</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">q2</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.simulator",
        "modulename": "tinyqsim.simulator",
        "kind": "module",
        "doc": "<p>Simulator for quantum circuit execution.</p>\n\n<p>Licensed under MIT license: see LICENSE.txt\nCopyright (c) 2024 Jon Brumfitt</p>\n"
    }, {
        "fullname": "tinyqsim.simulator.Simulator",
        "modulename": "tinyqsim.simulator",
        "qualname": "Simulator",
        "kind": "class",
        "doc": "<p>Simulator to evolve quantum state of system.</p>\n"
    }, {
        "fullname": "tinyqsim.simulator.Simulator.__init__",
        "modulename": "tinyqsim.simulator",
        "qualname": "Simulator.__init__",
        "kind": "function",
        "doc": "<p>Initialize simulator.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>nqubits</strong>:  Number of qubits</li>\n<li><strong>init: Initial state</strong>:  'zeros' or 'random'</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">nqubits</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">init</span><span class=\"o\">=</span><span class=\"s1\">&#39;zeros&#39;</span></span>)</span>"
    }, {
        "fullname": "tinyqsim.simulator.Simulator.state",
        "modulename": "tinyqsim.simulator",
        "qualname": "Simulator.state",
        "kind": "variable",
        "doc": "<p>Return quantum state as a vector.</p>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>quantum state vector</p>\n</blockquote>\n",
        "annotation": ": numpy.ndarray"
    }, {
        "fullname": "tinyqsim.simulator.Simulator.apply",
        "modulename": "tinyqsim.simulator",
        "qualname": "Simulator.apply",
        "kind": "function",
        "doc": "<p>Apply a unitary matrix to specified qubits of state.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>u</strong>:  unitary matrix</li>\n<li><strong>qubits</strong>:  qubits</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">u</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>, </span><span class=\"param\"><span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.simulator.Simulator.measure",
        "modulename": "tinyqsim.simulator",
        "qualname": "Simulator.measure",
        "kind": "function",
        "doc": "<p>Measure specified qubits.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">qubits</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.simulator.Simulator.execute",
        "modulename": "tinyqsim.simulator",
        "qualname": "Simulator.execute",
        "kind": "function",
        "doc": "<p>Execute the circuit.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>model</strong>:  Model to execute</li>\n</ul>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"bp\">self</span>, </span><span class=\"param\"><span class=\"n\">model</span><span class=\"p\">:</span> <span class=\"n\">tinyqsim</span><span class=\"o\">.</span><span class=\"n\">model</span><span class=\"o\">.</span><span class=\"n\">Model</span></span><span class=\"return-annotation\">) -> <span class=\"kc\">None</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.utils",
        "modulename": "tinyqsim.utils",
        "kind": "module",
        "doc": "<p>Miscellaneous utility functions.</p>\n\n<p>Licensed under MIT license: see LICENSE.txt\nCopyright (c) 2024 Jon Brumfitt</p>\n"
    }, {
        "fullname": "tinyqsim.utils.int_to_bits",
        "modulename": "tinyqsim.utils",
        "qualname": "int_to_bits",
        "kind": "function",
        "doc": "<p>Return integer 'n' as list of bits left-padded with zeros to width 'nbits'.\n'nbits' has no effect if it is smaller than the minimum required.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">n</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">nbits</span><span class=\"o\">=</span><span class=\"mi\">0</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.utils.bits_to_int",
        "modulename": "tinyqsim.utils",
        "qualname": "bits_to_int",
        "kind": "function",
        "doc": "<p>Convert list of bits (0 or 1) to an integer.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">bitlist</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">int</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.utils.round_complex",
        "modulename": "tinyqsim.utils",
        "qualname": "round_complex",
        "kind": "function",
        "doc": "<p>Round a complex number.</p>\n\n<h6 id=\"parameters\">Parameters</h6>\n\n<ul>\n<li><strong>z</strong>:  The complex number</li>\n<li><strong>decimals</strong>:  Number or decimal places</li>\n</ul>\n\n<h6 id=\"returns\">Returns</h6>\n\n<blockquote>\n  <p>The rounded result</p>\n</blockquote>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">z</span>, </span><span class=\"param\"><span class=\"n\">decimals</span><span class=\"p\">:</span> <span class=\"nb\">int</span> <span class=\"o\">=</span> <span class=\"mi\">3</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">complex</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.utils.complete",
        "modulename": "tinyqsim.utils",
        "qualname": "complete",
        "kind": "function",
        "doc": "<p>Complete a permutation, by appending missing integers in range(n).</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">perm</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span>, </span><span class=\"param\"><span class=\"n\">n</span><span class=\"p\">:</span> <span class=\"nb\">int</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"nb\">int</span><span class=\"p\">]</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.utils.normalize",
        "modulename": "tinyqsim.utils",
        "qualname": "normalize",
        "kind": "function",
        "doc": "<p>Normalize a complex vector</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">psi</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.utils.is_normalized",
        "modulename": "tinyqsim.utils",
        "qualname": "is_normalized",
        "kind": "function",
        "doc": "<p>Test whether a vector is normalized to given tolerance.</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">psi</span>, </span><span class=\"param\"><span class=\"n\">tol</span><span class=\"p\">:</span> <span class=\"nb\">float</span> <span class=\"o\">=</span> <span class=\"mf\">1e-14</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">bool</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.utils.is_unitary",
        "modulename": "tinyqsim.utils",
        "qualname": "is_unitary",
        "kind": "function",
        "doc": "<p>Test whether a matrix is unitary</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">m</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">bool</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.utils.is_hermitian",
        "modulename": "tinyqsim.utils",
        "qualname": "is_hermitian",
        "kind": "function",
        "doc": "<p>Test whether a matrix is Hermitian</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">m</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span></span><span class=\"return-annotation\">) -> <span class=\"nb\">bool</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.utils.kron_n",
        "modulename": "tinyqsim.utils",
        "qualname": "kron_n",
        "kind": "function",
        "doc": "<p>Return tensor product of 'n' instances of 'u'</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">n</span><span class=\"p\">:</span> <span class=\"nb\">int</span>, </span><span class=\"param\"><span class=\"n\">u</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.utils.kron_all",
        "modulename": "tinyqsim.utils",
        "qualname": "kron_all",
        "kind": "function",
        "doc": "<p>Return tensor product of a list of vectors or matrices.\ne.g. kron_all([H,H,H])</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">xs</span><span class=\"p\">:</span> <span class=\"nb\">list</span><span class=\"p\">[</span><span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span><span class=\"p\">]</span></span><span class=\"return-annotation\">) -> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span>:</span></span>",
        "funcdef": "def"
    }, {
        "fullname": "tinyqsim.utils.print_array",
        "modulename": "tinyqsim.utils",
        "qualname": "print_array",
        "kind": "function",
        "doc": "<p>Print matrix or vector in fixed-point with rounding</p>\n",
        "signature": "<span class=\"signature pdoc-code condensed\">(<span class=\"param\"><span class=\"n\">m</span><span class=\"p\">:</span> <span class=\"n\">numpy</span><span class=\"o\">.</span><span class=\"n\">ndarray</span></span><span class=\"return-annotation\">):</span></span>",
        "funcdef": "def"
    }];

    // mirrored in build-search-index.js (part 1)
    // Also split on html tags. this is a cheap heuristic, but good enough.
    elasticlunr.tokenizer.setSeperator(/[\s\-.;&_'"=,()]+|<[^>]*>/);

    let searchIndex;
    if (docs._isPrebuiltIndex) {
        console.info("using precompiled search index");
        searchIndex = elasticlunr.Index.load(docs);
    } else {
        console.time("building search index");
        // mirrored in build-search-index.js (part 2)
        searchIndex = elasticlunr(function () {
            this.pipeline.remove(elasticlunr.stemmer);
            this.pipeline.remove(elasticlunr.stopWordFilter);
            this.addField("qualname");
            this.addField("fullname");
            this.addField("annotation");
            this.addField("default_value");
            this.addField("signature");
            this.addField("bases");
            this.addField("doc");
            this.setRef("fullname");
        });
        for (let doc of docs) {
            searchIndex.addDoc(doc);
        }
        console.timeEnd("building search index");
    }

    return (term) => searchIndex.search(term, {
        fields: {
            qualname: {boost: 4},
            fullname: {boost: 2},
            annotation: {boost: 2},
            default_value: {boost: 2},
            signature: {boost: 2},
            bases: {boost: 2},
            doc: {boost: 1},
        },
        expand: true
    });
})();