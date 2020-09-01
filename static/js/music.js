$(function(){
    window.M = window.M || {},
		    M.loadUrl = function(e, t, n, o) {
		        var i = /\.css(?:\?|#|$)/i.test(e)
		          , r = document.createElement(i ? "link" : "script");
		        n && (r.charset = n),
		        r.onload = r.onerror = r.onreadystatechange = function(e) {
		            /^(?:loaded|complete|undefined)$/.test(r.readyState) && (r.onload = r.onerror = r.onreadystatechange = null,
		            i || document.body.removeChild(r),
		            r = null,
		            t && t(e))
		        }
		        ,
		        i ? (r.rel = "stylesheet",
		        r.href = e) : (r.async = !0,
		        r.src = e,
		        o && (r.crossOrigin = "true")),
		        document.body.appendChild(r)
		    }
		    ,
		    M.getNetType = function() {
		        var e = navigator.userAgent.match(/\bNetType\/(\w+)/i);
		        return (e = e && e[1]) || "unknown"
		    }
		    ,
		    M.extend = function(e) {
		        var t = !1
		          , n = e
		          , o = [].slice.call(arguments, 1);
		        return "boolean" == typeof e && (t = e,
		        n = o.shift()),
		        o.forEach(function(e) {
		            !function e(t, n, o) {
		                for (var i in n) {
		                    var r = n[i];
		                    o && M.isPlainObject(r) || M.isArray(r) ? (M.isPlainObject(r) && !M.isPlainObject(t[i]) && (t[i] = {}),
		                    M.isArray(n[i]) && !M.isArray(t[i]) && (t[i] = []),
		                    e(t[i], n[i], o)) : void 0 !== r && (t[i] = r)
		                }
		            }(n, e, t)
		        }),
		        n
		    }
		    ,
		    M.offset = function(e) {
		        var t = e.getBoundingClientRect();
		        return {
		            left: t.left + window.pageXOffset,
		            top: t.top + window.pageYOffset,
		            width: Math.round(t.width),
		            height: Math.round(t.height)
		        }
		    }
		    ,
		    M.contains = function(e, t) {
		        return e !== t && e.contains(t)
		    }
		    ,
		    M.each = function(e, t) {
		        var n, o;
		        if ("number" == typeof e.length) {
		            for (n = 0; n < e.length; n++)
		                if (!1 === t.call(e[n], n, e[n]))
		                    return e
		        } else
		            for (o in e)
		                if (!1 === t.call(e[o], o, e[o]))
		                    return e;
		        return e
		    }
		    ,
		    M.fixUrl = function(e) {
		        var t = document.createElement("a");
		        if (t.href = e,
		        "pic.y.qq.com" === t.host)
		            return e;
		        var n = location.protocol;
		        return e && M.isString(e) && (/^http(s?):\/\//i.test(e) && (e = e.replace(/^http(s?):/i, n)),
		        /^\/\//.test(e) && (e = n + e),
		        /\.(jpg|png|gif|css|js)$/i.test(e) && (e += "?max_age=2592000"),
		        /\.(jpg|png|gif|css|js)\?/i.test(e) && !e.match(/^http(s?):\/\/y\.qq\.com\//i) && e.match(/^http(s?):\/\/[^\/]+\/(music|mediastyle)\//i) && (e = e.replace(new RegExp("^(" + n + ")\\/\\/[^\\/]+\\/(music|mediastyle)\\/","i"), function() {
		            return RegExp.$1 + "//y.qq.com/" + RegExp.$2 + "/"
		        }))),
		        e
		    }
		    ,
		    M.getACSRFToken = function(e, t) {
		        e = e || "skey";
		        var n = ""
		          , o = 5381;
		        if (n = t ? M.cookie.get("qqmusic_key") || M.cookie.get("p_skey") || M.cookie.get("skey") || M.cookie.get("p_lskey") || M.cookie.get("lskey") : M.cookie.get(e) || M.cookie.get("skey") || M.cookie.get("qqmusic_key"))
		            for (var i = 0, r = n.length; i < r; ++i)
		                o += (o << 5) + n.charCodeAt(i);
		        return 2147483647 & o
		    }
		    ,
		    M.param = function(e) {
		        var n = []
		          , t = function(e, t) {
		            n.push(encodeURIComponent(e) + "=" + encodeURIComponent(t))
		        };
		        for (var o in e) {
		            var i = e[o];
		            t(o, "object" == typeof i ? M.param(i) : i)
		        }
		        return n.join("&").replace(/%20/g, "+")
		    }
		    ,
		    M.inherits = function(e, t) {
		        if ("function" != typeof e && null !== t)
		            throw new TypeError("Super expression must either be null or a function, not " + typeof t);
		        e.prototype = Object.create(t && t.prototype, {
		            constructor: {
		                value: e,
		                enumerable: !1,
		                writable: !0,
		                configurable: !0
		            }
		        })
		    }
		    ,
		    M.createClass = function(t, e, n, o) {
		        function i(e, t) {
		            for (var n in t)
		                Object.defineProperty(e, n, {
		                    enumerable: !1,
		                    writable: !0,
		                    configurable: !0,
		                    value: t[n]
		                })
		        }
		        function r(e) {
		            if (!(instance instanceof t))
		                throw new TypeError("Cannot call a class as a function");
		            t.call(this, e)
		        }
		        return r.constructor = t,
		        e && M.inherits(r, e),
		        n && i(t.prototype, n),
		        o && i(t, o),
		        r
		    }
		    ,
		    M.createComponent = function(e) {
		        var n = preact.Component;
		        function t(e, t) {
		            n.call(this, e, t),
		            this.state = this.getInitialState ? this.getInitialState() : {},
		            this.refs = {},
		            this._refProxies = {}
		        }
		        function o() {}
		        return (e = M.extend({
		            constructor: t
		        }, e)).statics && M.extend(t, e.statics),
		        e.propTypes && (t.propTypes = e.propTypes),
		        e.defaultProps && (t.defaultProps = e.defaultProps),
		        e.getDefaultProps && (t.defaultProps = e.getDefaultProps.call(t)),
		        o.prototype = n.prototype,
		        t.prototype = M.extend(new o, e),
		        t.displayName = e.displayName || "Component",
		        t
		    }
		    ,
		    M.getPic = function(e, t, n) {
		        var o = location.protocol + "//y.qq.com/mediastyle/music_v11/extra/default_300x300.jpg?max_age=31536000";
		        return M.isString(t) && 14 <= t.length && (e = "album" == e ? "T002" : "singer" == e ? "T001" : e,
		        o = location.protocol + "//y.qq.com/music/photo_new/" + e + "R" + (n || 68) + "x" + (n || 68) + "M000" + t + ".jpg?max_age=2592000"),
		        o
		    }
		    ,
		    M.compare = function(e, t) {
		        for (e = ("" + e).split("."),
		        t = ("" + t).split("."); e.length + t.length; ) {
		            var n = e.shift() || "0"
		              , o = t.shift() || "0";
		            if (0 <= n && 0 <= o && (n = ~~n,
		            o = ~~o),
		            o < n)
		                return 1;
		            if (n < o)
		                return -1
		        }
		        return 0
		    }
		    ;
		    var A = function() {
		        if ("undefined" != typeof self)
		            return self;
		        if ("undefined" != typeof window)
		            return window;
		        if ("undefined" != typeof global)
		            return global;
		        throw new Error("unable to locate global object")
		    }();
                function getsign(e) {m.data = JSON.stringify(e);g = z.getSecuritySign(m.data);g=g.replace(/z/g,'MDAT~!').replace(/c/g,'ZYbp|%').replace(/a/g,'*a(d/v:wty;').replace(/e/g,'~##5fljfh8');return g}
		    A.__sign_hash_20200305 = function(e) {
		        function d(e, t) {
		            var n = (65535 & e) + (65535 & t);
		            return (e >> 16) + (t >> 16) + (n >> 16) << 16 | 65535 & n
		        }
		        function s(e, t, n, o, i, r) {
		            return d((a = d(d(t, e), d(o, r))) << (s = i) | a >>> 32 - s, n);
		            var a, s
		        }
		        function p(e, t, n, o, i, r, a) {
		            return s(t & n | ~t & o, e, t, i, r, a)
		        }
		        function m(e, t, n, o, i, r, a) {
		            return s(t & o | n & ~o, e, t, i, r, a)
		        }
		        function f(e, t, n, o, i, r, a) {
		            return s(t ^ n ^ o, e, t, i, r, a)
		        }
		        function h(e, t, n, o, i, r, a) {
		            return s(n ^ (t | ~o), e, t, i, r, a)
		        }
		        function t(e) {
		            return function(e) {
		                var t, n = "";
		                for (t = 0; t < 32 * e.length; t += 8)
		                    n += String.fromCharCode(e[t >> 5] >>> t % 32 & 255);
		                return n
		            }(function(e, t) {
		                e[t >> 5] |= 128 << t % 32,
		                e[14 + (t + 64 >>> 9 << 4)] = t;
		                var n, o, i, r, a, s = 1732584193, c = -271733879, l = -1732584194, u = 271733878;
		                for (n = 0; n < e.length; n += 16)
		                    c = h(c = h(c = h(c = h(c = f(c = f(c = f(c = f(c = m(c = m(c = m(c = m(c = p(c = p(c = p(c = p(i = c, l = p(r = l, u = p(a = u, s = p(o = s, c, l, u, e[n], 7, -680876936), c, l, e[n + 1], 12, -389564586), s, c, e[n + 2], 17, 606105819), u, s, e[n + 3], 22, -1044525330), l = p(l, u = p(u, s = p(s, c, l, u, e[n + 4], 7, -176418897), c, l, e[n + 5], 12, 1200080426), s, c, e[n + 6], 17, -1473231341), u, s, e[n + 7], 22, -45705983), l = p(l, u = p(u, s = p(s, c, l, u, e[n + 8], 7, 1770035416), c, l, e[n + 9], 12, -1958414417), s, c, e[n + 10], 17, -42063), u, s, e[n + 11], 22, -1990404162), l = p(l, u = p(u, s = p(s, c, l, u, e[n + 12], 7, 1804603682), c, l, e[n + 13], 12, -40341101), s, c, e[n + 14], 17, -1502002290), u, s, e[n + 15], 22, 1236535329), l = m(l, u = m(u, s = m(s, c, l, u, e[n + 1], 5, -165796510), c, l, e[n + 6], 9, -1069501632), s, c, e[n + 11], 14, 643717713), u, s, e[n], 20, -373897302), l = m(l, u = m(u, s = m(s, c, l, u, e[n + 5], 5, -701558691), c, l, e[n + 10], 9, 38016083), s, c, e[n + 15], 14, -660478335), u, s, e[n + 4], 20, -405537848), l = m(l, u = m(u, s = m(s, c, l, u, e[n + 9], 5, 568446438), c, l, e[n + 14], 9, -1019803690), s, c, e[n + 3], 14, -187363961), u, s, e[n + 8], 20, 1163531501), l = m(l, u = m(u, s = m(s, c, l, u, e[n + 13], 5, -1444681467), c, l, e[n + 2], 9, -51403784), s, c, e[n + 7], 14, 1735328473), u, s, e[n + 12], 20, -1926607734), l = f(l, u = f(u, s = f(s, c, l, u, e[n + 5], 4, -378558), c, l, e[n + 8], 11, -2022574463), s, c, e[n + 11], 16, 1839030562), u, s, e[n + 14], 23, -35309556), l = f(l, u = f(u, s = f(s, c, l, u, e[n + 1], 4, -1530992060), c, l, e[n + 4], 11, 1272893353), s, c, e[n + 7], 16, -155497632), u, s, e[n + 10], 23, -1094730640), l = f(l, u = f(u, s = f(s, c, l, u, e[n + 13], 4, 681279174), c, l, e[n], 11, -358537222), s, c, e[n + 3], 16, -722521979), u, s, e[n + 6], 23, 76029189), l = f(l, u = f(u, s = f(s, c, l, u, e[n + 9], 4, -640364487), c, l, e[n + 12], 11, -421815835), s, c, e[n + 15], 16, 530742520), u, s, e[n + 2], 23, -995338651), l = h(l, u = h(u, s = h(s, c, l, u, e[n], 6, -198630844), c, l, e[n + 7], 10, 1126891415), s, c, e[n + 14], 15, -1416354905), u, s, e[n + 5], 21, -57434055), l = h(l, u = h(u, s = h(s, c, l, u, e[n + 12], 6, 1700485571), c, l, e[n + 3], 10, -1894986606), s, c, e[n + 10], 15, -1051523), u, s, e[n + 1], 21, -2054922799), l = h(l, u = h(u, s = h(s, c, l, u, e[n + 8], 6, 1873313359), c, l, e[n + 15], 10, -30611744), s, c, e[n + 6], 15, -1560198380), u, s, e[n + 13], 21, 1309151649), l = h(l, u = h(u, s = h(s, c, l, u, e[n + 4], 6, -145523070), c, l, e[n + 11], 10, -1120210379), s, c, e[n + 2], 15, 718787259), u, s, e[n + 9], 21, -343485551),
		                    s = d(s, o),
		                    c = d(c, i),
		                    l = d(l, r),
		                    u = d(u, a);
		                return [s, c, l, u]
		            }(function(e) {
		                var t, n = [];
		                for (n[(e.length >> 2) - 1] = void 0,
		                t = 0; t < n.length; t += 1)
		                    n[t] = 0;
		                for (t = 0; t < 8 * e.length; t += 8)
		                    n[t >> 5] |= (255 & e.charCodeAt(t / 8)) << t % 32;
		                return n
		            }(e), 8 * e.length))
		        }
		        function n(e) {
		            return t(unescape(encodeURIComponent(e)))
		        }
		        return function(e) {
		            var t, n, o = "0123456789abcdef", i = "";
		            for (n = 0; n < e.length; n += 1)
		                t = e.charCodeAt(n),
		                i += o.charAt(t >>> 4 & 15) + o.charAt(15 & t);
		            return i
		        }(n(e))
		    }
		    ,
		    function s(c, l, u, d, p) {
		        p = p || [[this], [{}]];
		        for (var t = [], n = null, e = [function() {
		            return !0
		        }
		        , function() {}
		        , function() {
		            p.length = u[l++]
		        }
		        , function() {
		            p.push(u[l++])
		        }
		        , function() {
		            p.pop()
		        }
		        , function() {
		            var e = u[l++]
		              , t = p[p.length - 2 - e];
		            p[p.length - 2 - e] = p.pop(),
		            p.push(t)
		        }
		        , function() {
		            p.push(p[p.length - 1])
		        }
		        , function() {
		            p.push([p.pop(), p.pop()].reverse())
		        }
		        , function() {
		            p.push([d, p.pop()])
		        }
		        , function() {
		            p.push([p.pop()])
		        }
		        , function() {
		            var e = p.pop();  //e = (2) [Window, "location"]
		            p.push(e[0][e[1]])
		        }
		        , function() {
		            p.push(p[p.pop()[0]][0])
		        }
		        , function() {
		            var e = p[p.length - 2];
		            e[0][e[1]] = p[p.length - 1]
		        }
		        , function() {
		            p[p[p.length - 2][0]][0] = p[p.length - 1]
		        }
		        , function() {
		            var e = p.pop()
		              , t = p.pop();
					if (e === 'indexOf' && t[1] === 'host'){
						p.push(['i.y.qq.com', e])
						return
						}
		            p.push([t[0][t[1]], e])
		        }
		        , function() {
		            var e = p.pop();
		            p.push([p[p.pop()][0], e])
		        }
		        , function() {
		            var e = p.pop();
		            p.push(delete e[0][e[1]])
		        }
		        , function() {
		            var e = [];
		            for (var t in p.pop())
		                e.push(t);
		            p.push(e)
		        }
		        , function() {
		            p[p.length - 1].length ? p.push(p[p.length - 1].shift(), !0) : p.push(void 0, !1)
		        }
		        , function() {
		            var e = p[p.length - 2]
		              , t = Object.getOwnPropertyDescriptor(e[0], e[1]) || {
		                configurable: !0,
		                enumerable: !0
		            };
		            t.get = p[p.length - 1],
		            Object.defineProperty(e[0], e[1], t)
		        }
		        , function() {
		            var e = p[p.length - 2]
		              , t = Object.getOwnPropertyDescriptor(e[0], e[1]) || {
		                configurable: !0,
		                enumerable: !0
		            };
		            t.set = p[p.length - 1],
		            Object.defineProperty(e[0], e[1], t)
		        }
		        , function() {
		            l = u[l++]
		        }
		        , function() {
		            var e = u[l++];
		            p[p.length - 1] && (l = e)
		        }
		        , function() {
		            throw p[p.length - 1]
		        }
		        , function() {
		            var e = u[l++]
		              , t = e ? p.slice(-e) : [];
		            p.length -= e,
		            p.push(p.pop().apply(d, t))
		        }
		        , function() {
		            var e = u[l++]
		              , t = e ? p.slice(-e) : [];
		            p.length -= e;
		            var n = p.pop();
		            p.push(n[0][n[1]].apply(n[0], t))
		        }
		        , function() {
		            var e = u[l++]
		              , t = e ? p.slice(-e) : [];
		            p.length -= e,
		            t.unshift(null),
		            p.push(new (Function.prototype.bind.apply(p.pop(), t)))
		        }
		        , function() {
		            var e = u[l++]
		              , t = e ? p.slice(-e) : [];
		            p.length -= e,
		            t.unshift(null);
		            var n = p.pop();
		            p.push(new (Function.prototype.bind.apply(n[0][n[1]], t)))
		        }
		        , function() {
		            p.push(!p.pop())
		        }
		        , function() {
		            p.push(~p.pop())
		        }
		        , function() {
		            p.push(typeof p.pop())
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] == p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] === p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] > p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] >= p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] << p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] >> p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] >>> p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] + p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] - p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] * p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] / p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] % p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] | p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] & p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] ^ p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2]in p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2]instanceof p.pop()
		        }
		        , function() {
		            p[p[p.length - 1][0]] = void 0 === p[p[p.length - 1][0]] ? [] : p[p[p.length - 1][0]]
		        }
		        , function() {
		            for (var o = u[l++], i = [], e = u[l++], t = u[l++], r = [], n = 0; n < e; n++)
		                i[u[l++]] = p[u[l++]];
		            for (var a = 0; a < t; a++)
		                r[a] = u[l++];
		            p.push(function e() {
		                var t = i.slice(0);
		                t[0] = [this],
		                t[1] = [arguments],
		                t[2] = [e];
		                for (var n = 0; n < r.length && n < arguments.length; n++)
		                    0 < r[n] && (t[r[n]] = [arguments[n]]);
		                return s(c, o, u, d, t)
		            })
		        }
		        , function() {
		            t.push([u[l++], p.length, u[l++]])
		        }
		        , function() {
		            t.pop()
		        }
		        , function() {
		            return !!n
		        }
		        , function() {
		            n = null
		        }
		        , function() {
		            p[p.length - 1] += String.fromCharCode(u[l++])
		        }
		        , function() {
		            p.push("")
		        }
		        , function() {
		            p.push(void 0)
		        }
		        , function() {
		            p.push(null)
		        }
		        , function() {
		            p.push(!0)
		        }
		        , function() {
		            p.push(!1)
		        }
		        , function() {
		            p.length -= u[l++]
		        }
		        , function() {
		            p[p.length - 1] = u[l++]
		        }
		        , function() {
		            var e = p.pop()
		              , t = p[p.length - 1];
		            t[0][t[1]] = p[e[0]][0]
		        }
		        , function() {
		            var e = p.pop()
		              , t = p[p.length - 1];
		            t[0][t[1]] = e[0][e[1]]
		        }
		        , function() {
		            var e = p.pop()
		              , t = p[p.length - 1];
		            p[t[0]][0] = p[e[0]][0]
		        }
		        , function() {
		            var e = p.pop()
		              , t = p[p.length - 1];
		            p[t[0]][0] = e[0][e[1]]
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] < p.pop()
		        }
		        , function() {
		            p[p.length - 2] = p[p.length - 2] <= p.pop()
		        }
		        ]; ; )
		            try {
		                for (; !e[u[l++]](); )
		                    ;
		                if (n)
		                    throw n;
		                return p.pop()
		            } catch (e) {
		                var o = t.pop();
		                if (void 0 === o)
		                    throw e;
		                n = e,
		                l = o[0],
		                p.length = o[1],
		                o[2] && (p[o[2]][0] = n)
		            }
		    }(120731, 0, [21, 34, 50, 100, 57, 50, 102, 50, 98, 99, 101, 52, 54, 97, 52, 99, 55, 56, 52, 49, 57, 54, 57, 49, 56, 98, 102, 100, 100, 48, 48, 55, 55, 102, 2, 10, 3, 2, 9, 48, 61, 3, 9, 48, 61, 4, 9, 48, 61, 5, 9, 48, 61, 6, 9, 48, 61, 7, 9, 48, 61, 8, 9, 48, 61, 9, 9, 48, 4, 21, 427, 54, 2, 15, 3, 2, 9, 48, 61, 3, 9, 48, 61, 4, 9, 48, 61, 5, 9, 48, 61, 6, 9, 48, 61, 7, 9, 48, 61, 8, 9, 48, 61, 9, 9, 48, 61, 10, 9, 48, 61, 11, 9, 48, 61, 12, 9, 48, 61, 13, 9, 48, 61, 14, 9, 48, 61, 10, 9, 55, 54, 97, 54, 98, 54, 99, 54, 100, 54, 101, 54, 102, 54, 103, 54, 104, 54, 105, 54, 106, 54, 107, 54, 108, 54, 109, 54, 110, 54, 111, 54, 112, 54, 113, 54, 114, 54, 115, 54, 116, 54, 117, 54, 118, 54, 119, 54, 120, 54, 121, 54, 122, 54, 48, 54, 49, 54, 50, 54, 51, 54, 52, 54, 53, 54, 54, 54, 55, 54, 56, 54, 57, 13, 4, 61, 11, 9, 55, 54, 77, 54, 97, 54, 116, 54, 104, 8, 55, 54, 102, 54, 108, 54, 111, 54, 111, 54, 114, 14, 55, 54, 77, 54, 97, 54, 116, 54, 104, 8, 55, 54, 114, 54, 97, 54, 110, 54, 100, 54, 111, 54, 109, 14, 25, 0, 3, 4, 9, 11, 3, 3, 9, 11, 39, 3, 1, 38, 40, 3, 3, 9, 11, 38, 25, 1, 13, 4, 61, 12, 9, 55, 13, 4, 61, 13, 9, 3, 0, 13, 4, 4, 3, 13, 9, 11, 3, 11, 9, 11, 66, 22, 306, 4, 21, 422, 24, 4, 3, 14, 9, 55, 54, 77, 54, 97, 54, 116, 54, 104, 8, 55, 54, 102, 54, 108, 54, 111, 54, 111, 54, 114, 14, 55, 54, 77, 54, 97, 54, 116, 54, 104, 8, 55, 54, 114, 54, 97, 54, 110, 54, 100, 54, 111, 54, 109, 14, 25, 0, 3, 10, 9, 55, 54, 108, 54, 101, 54, 110, 54, 103, 54, 116, 54, 104, 15, 10, 40, 25, 1, 13, 4, 61, 12, 9, 6, 11, 3, 10, 9, 3, 14, 9, 11, 15, 10, 38, 13, 4, 61, 13, 9, 6, 11, 6, 5, 1, 5, 0, 3, 1, 38, 13, 4, 61, 0, 5, 0, 43, 4, 21, 291, 61, 3, 12, 9, 11, 0, 3, 9, 9, 49, 72, 0, 2, 3, 4, 13, 4, 61, 8, 9, 21, 721, 3, 2, 8, 3, 2, 9, 48, 61, 3, 9, 48, 61, 4, 9, 48, 61, 5, 9, 48, 61, 6, 9, 48, 61, 7, 9, 48, 4, 55, 54, 115, 54, 101, 54, 108, 54, 102, 8, 10, 30, 55, 54, 117, 54, 110, 54, 100, 54, 101, 54, 102, 54, 105, 54, 110, 54, 101, 54, 100, 32, 28, 22, 510, 4, 21, 523, 22, 4, 55, 54, 115, 54, 101, 54, 108, 54, 102, 8, 10, 0, 55, 54, 119, 54, 105, 54, 110, 54, 100, 54, 111, 54, 119, 8, 10, 30, 55, 54, 117, 54, 110, 54, 100, 54, 101, 54, 102, 54, 105, 54, 110, 54, 101, 54, 100, 32, 28, 22, 566, 4, 21, 583, 3, 4, 55, 54, 119, 54, 105, 54, 110, 54, 100, 54, 111, 54, 119, 8, 10, 0, 55, 54, 103, 54, 108, 54, 111, 54, 98, 54, 97, 54, 108, 8, 10, 30, 55, 54, 117, 54, 110, 54, 100, 54, 101, 54, 102, 54, 105, 54, 110, 54, 101, 54, 100, 32, 28, 22, 626, 4, 21, 643, 25, 4, 55, 54, 103, 54, 108, 54, 111, 54, 98, 54, 97, 54, 108, 8, 10, 0, 55, 54, 69, 54, 114, 54, 114, 54, 111, 54, 114, 8, 55, 54, 117, 54, 110, 54, 97, 54, 98, 54, 108, 54, 101, 54, 32, 54, 116, 54, 111, 54, 32, 54, 108, 54, 111, 54, 99, 54, 97, 54, 116, 54, 101, 54, 32, 54, 103, 54, 108, 54, 111, 54, 98, 54, 97, 54, 108, 54, 32, 54, 111, 54, 98, 54, 106, 54, 101, 54, 99, 54, 116, 27, 1, 23, 56, 0, 49, 444, 0, 0, 24, 0, 13, 4, 61, 8, 9, 55, 54, 95, 54, 95, 54, 103, 54, 101, 54, 116, 54, 83, 54, 101, 54, 99, 54, 117, 54, 114, 54, 105, 54, 116, 54, 121, 54, 83, 54, 105, 54, 103, 54, 110, 15, 21, 1126, 49, 2, 14, 3, 2, 9, 48, 61, 3, 9, 48, 61, 4, 9, 48, 61, 5, 9, 48, 61, 6, 9, 48, 61, 7, 9, 48, 61, 8, 9, 48, 61, 9, 9, 48, 61, 10, 9, 48, 61, 11, 9, 48, 61, 9, 9, 55, 54, 108, 54, 111, 54, 99, 54, 97, 54, 116, 54, 105, 54, 111, 54, 110, 8, 10, 30, 55, 54, 117, 54, 110, 54, 100, 54, 101, 54, 102, 54, 105, 54, 110, 54, 101, 54, 100, 32, 28, 22, 862, 21, 932, 21, 4, 55, 54, 108, 54, 111, 54, 99, 54, 97, 54, 116, 54, 105, 54, 111, 54, 110, 8, 55, 54, 104, 54, 111, 54, 115, 54, 116, 14, 55, 54, 105, 54, 110, 54, 100, 54, 101, 54, 120, 54, 79, 54, 102, 14, 55, 54, 121, 54, 46, 54, 113, 54, 113, 54, 46, 54, 99, 54, 111, 54, 109, 25, 1, 3, 0, 3, 1, 39, 32, 22, 963, 4, 55, 54, 67, 54, 74, 54, 66, 54, 80, 54, 65, 54, 67, 54, 114, 54, 82, 54, 117, 54, 78, 54, 121, 54, 55, 21, 974, 50, 4, 3, 12, 9, 11, 3, 8, 3, 10, 24, 2, 13, 4, 61, 10, 9, 3, 13, 9, 55, 54, 95, 54, 95, 54, 115, 54, 105, 54, 103, 54, 110, 54, 95, 54, 104, 54, 97, 54, 115, 54, 104, 54, 95, 54, 50, 54, 48, 54, 50, 54, 48, 54, 48, 54, 51, 54, 48, 54, 53, 15, 10, 22, 1030, 21, 1087, 22, 4, 3, 13, 9, 55, 54, 95, 54, 95, 54, 115, 54, 105, 54, 103, 54, 110, 54, 95, 54, 104, 54, 97, 54, 115, 54, 104, 54, 95, 54, 50, 54, 48, 54, 50, 54, 48, 54, 48, 54, 51, 54, 48, 54, 53, 15, 3, 9, 9, 11, 3, 3, 9, 11, 38, 25, 1, 13, 4, 61, 11, 9, 3, 12, 9, 11, 3, 10, 3, 53, 3, 37, 39, 24, 2, 13, 4, 4, 55, 54, 122, 54, 122, 54, 97, 3, 11, 9, 11, 38, 3, 10, 9, 11, 38, 0, 49, 771, 2, 1, 12, 9, 13, 8, 3, 12, 4, 4, 56, 0], A);
		    var O, L, Q, z, U, N, F, B, J, W, V, H, G, X, Z, Y, K, ee, te, ne, oe, ie, re, ae, se, ce, le, ue, de, pe, me, fe, he, ge, _e, we, be, ve, ye, qe, xe, ke, Se, Te, Ce, Me, De, Ee, Ie, je, Re, Pe, Ae, Oe, Le = A.__getSecuritySign;
		    delete A.__getSecuritySign,
		    M.getSecuritySign = Le

			var g = ''
			var t = true
			var z = M
			var m = {}

    var data = {}
    data.csrfmiddlewaretoken = csrfmiddlewaretoken
    $('#musicurl').focus(function(){
        $(this).attr('placeholder','')
    })
    $('#musicurl').blur(function(){
        $(this).attr('placeholder','URL')
    })
    function fetchmurl(){
        $('#parse').html('正在解析...')
        $('#parse').unbind()
        var musicurln = $('#musicurl').val()
        data.musicurln = musicurln
        var mtypelist = $('[name="mtype"]')
        for (var i in mtypelist){
        if (mtypelist[i].checked){
        var mtype = mtypelist[i].value
        if (mtype === 'qqmusic'){
            var reg = /\/song\/(.*?).html/g
            var songmid = musicurln.match(reg)
            if (songmid){
                songmid = songmid[0].replace('/song/','').replace('.html','')
                var e = {"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"3428190121","songmid":[songmid],"songtype":[0],"uin":"0","loginflag":0,"platform":"23","h5to":"speed"}},"comm":{"g_tk":5381,"uin":0,"format":"json","platform":"h5"}}
            }else{
                reg = /songmid=(.*?)#/g
                songmid = musicurln.match(reg)
                if (!songmid){
                    data.errorwarn = '1'
                }else{
                    songmid = songmid[0].replace('songmid=','').replace('#','')
                }
                var e = {"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"3428190121","songmid":[songmid],"songtype":[0],"uin":"0","loginflag":0,"platform":"23","h5to":"speed"}},"comm":{"g_tk":5381,"uin":0,"format":"json","platform":"h5"}}
            }
            data.sekey = getsign(e)
        }
        data.mtype = mtype
        break
        }
        }
        $.ajax({
            type:'post',
            url:url,
            data:data,
            success:function(data){
              if (data.status === 'success'){
                $('#parse').html('解析成功,5s后可再次解析')
                window.location.href = data.url
              }else if ((data.status === 'please check your url whether you have songmid params') || (data.status === 'please check your url whether you have id params') || (data.status === 'check whether you mistake the music type')){
                $('#parse').html('解析失败,5s后可再次解析')
                var $span = $('<span>' + data.status + '</span>')
                $span.css('color','blanchedalmond')
                $span.css('font-size','18px')
                $('.form').append($span)
                setTimeout(function(){
                    $span.remove()
                },25000)
              }else{
                window.location.href = url403
              }
            },
            error:function(xhr){
                window.location.href = url500
            },
        })
        setTimeout(function(){
            $('#parse').html('解析')
            $('#parse').unbind()
            $('#parse').bind('click',fetchmurl)
        },5000)
    }
    $('#parse').bind('click',fetchmurl)

})







