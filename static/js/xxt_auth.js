$(function(){
        function RSAKeyPair(a, b, c) {
                        this.e = biFromHex(a),
                        this.d = biFromHex(b),
                        this.m = biFromHex(c),
                        this.chunkSize = 2 * biHighIndex(this.m),
                        this.radix = 16,
                        this.barrett = new BarrettMu(this.m)
                    }
                    	    var $mybutton = $("#mybutton");
                    function biFromHex(a) {
                        var d, e, b = new BigInt, c = a.length;
                        for (d = c,
                        e = 0; d > 0; d -= 4,
                        ++e)
                            b.digits[e] = hexToDigit(a.substr(Math.max(d - 4, 0), Math.min(d, 4)));
                        return b
                    }
                                    var base_str = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#%&()*+-./:<=>?@[]^_`{|}~"; var s_num = [5,9,16]
                    function hexToDigit(a) {
                        var d, b = 0, c = Math.min(a.length, 4);
                        for (d = 0; c > d; ++d)
                            b <<= 4,
                            b |= charToHex(a.charCodeAt(d));
                        return b
                    }
                            var base_1 = base_str[35];
                    function charToHex(a) {
                        var h, b = 48, c = b + 9, d = 97, e = d + 25, f = 65, g = 90;
                        return h = a >= b && c >= a ? a - b : a >= f && g >= a ? 10 + a - f : a >= d && e >= a ? 10 + a - d : 0
                    }
                                                var base_2 = base_str[34];      var base_3 = base_str[17];
                    var data = {};
                    function biHighIndex(a) {
                        for (var b = a.digits.length - 1; b > 0 && 0 == a.digits[b]; )
                            --b;
                        return b
                    }
                    function BarrettMu(a) {
                        this.modulus = biCopy(a),
                        this.k = biHighIndex(this.modulus) + 1;
                        var b = new BigInt;
                        b.digits[2 * this.k] = 1,
                        this.mu = biDivide(b, this.modulus),
                        this.bkplus1 = new BigInt,
                        this.bkplus1.digits[this.k + 1] = 1,
                        this.modulo = BarrettMu_modulo,
                        this.multiplyMod = BarrettMu_multiplyMod,
                        this.powMod = BarrettMu_powMod
                    }
                    function a_key(){
                        var key_num = random_int(30,50);
                        var a = ""
                        for (var i = 0;i < key_num;i++){
                             i == s_num[0] ? a += base_1 : (i == s_num[1] ? a += base_2 : (i == s_num[2] ? a += base_3 : a += base_str[random_int(0,base_str.length)]));

                        }
                        return a
                    }
                    function biCopy(a) {
                        var b = new BigInt(!0);
                        return b.digits = a.digits.slice(0),
                        b.isNeg = a.isNeg,
                        b
                    }
                                        var b = base_1 + base_2 + base_3
                    function biDivide(a, b) {
                        return biDivideModulo(a, b)[0]
                    }
                    function random_int(m,n){
                        return Math.floor(Math.random()*(m-n+1)+n);
                    }
                                    data.a = a_key()
                    function biDivideModulo(a, b) {
                        var f, g, h, i, j, k, l, m, n, o, p, q, r, s, c = biNumBits(a), d = biNumBits(b), e = b.isNeg;
                        if (d > c)
                            return a.isNeg ? (f = biCopy(bigOne),
                            f.isNeg = !b.isNeg,
                            a.isNeg = !1,
                            b.isNeg = !1,
                            g = biSubtract(b, a),
                            a.isNeg = !0,
                            b.isNeg = e) : (f = new BigInt,
                            g = biCopy(a)),
                            new Array(f,g);
                        for (f = new BigInt,
                        g = a,
                        h = Math.ceil(d / bitsPerDigit) - 1,
                        i = 0; b.digits[h] < biHalfRadix; )
                            b = biShiftLeft(b, 1),
                            ++i,
                            ++d,
                            h = Math.ceil(d / bitsPerDigit) - 1;
                        for (g = biShiftLeft(g, i),
                        c += i,
                        j = Math.ceil(c / bitsPerDigit) - 1,
                        k = biMultiplyByRadixPower(b, j - h); -1 != biCompare(g, k); )
                            ++f.digits[j - h],
                            g = biSubtract(g, k);
                        for (l = j; l > h; --l) {
                            for (m = l >= g.digits.length ? 0 : g.digits[l],
                            n = l - 1 >= g.digits.length ? 0 : g.digits[l - 1],
                            o = l - 2 >= g.digits.length ? 0 : g.digits[l - 2],
                            p = h >= b.digits.length ? 0 : b.digits[h],
                            q = h - 1 >= b.digits.length ? 0 : b.digits[h - 1],
                            f.digits[l - h - 1] = m == p ? maxDigitVal : Math.floor((m * biRadix + n) / p),
                            r = f.digits[l - h - 1] * (p * biRadix + q),
                            s = m * biRadixSquared + (n * biRadix + o); r > s; )
                                --f.digits[l - h - 1],
                                r = f.digits[l - h - 1] * (p * biRadix | q),
                                s = m * biRadix * biRadix + (n * biRadix + o);
                            k = biMultiplyByRadixPower(b, l - h - 1),
                            g = biSubtract(g, biMultiplyDigit(k, f.digits[l - h - 1])),
                            g.isNeg && (g = biAdd(g, k),
                            --f.digits[l - h - 1])
                        }
                        return g = biShiftRight(g, i),
                        f.isNeg = a.isNeg != e,
                        a.isNeg && (f = e ? biAdd(f, bigOne) : biSubtract(f, bigOne),
                        b = biShiftRight(b, i),
                        g = biSubtract(b, g)),
                        0 == g.digits[0] && 0 == biHighIndex(g) && (g.isNeg = !1),
                        new Array(f,g)
                    }
                    function b_key(){
                        var key_num = random_int(30,60);
                        var b = ""
                        for (var i = 0;i < key_num;i++){
                           i == s_num[0] ? b += base_1 : (i == s_num[1] ? b += base_2 : (i == s_num[2] ? b += base_3 : b += base_str[random_int(0,base_str.length)]));
                        }
                        return b
                    }
                    function biNumBits(a) {
                        var e, b = biHighIndex(a), c = a.digits[b], d = (b + 1) * bitsPerDigit;
                        for (e = d; e > d - bitsPerDigit && 0 == (32768 & c); --e)
                            c <<= 1;
                        return e
                    }
                    function biShiftLeft(a, b) {
                        var e, f, g, h, c = Math.floor(b / bitsPerDigit), d = new BigInt;
                        for (arrayCopy(a.digits, 0, d.digits, c, d.digits.length - c),
                        e = b % bitsPerDigit,
                        f = bitsPerDigit - e,
                        g = d.digits.length - 1,
                        h = g - 1; g > 0; --g,
                        --h)
                            d.digits[g] = d.digits[g] << e & maxDigitVal | (d.digits[h] & highBitMasks[e]) >>> f;
                        return d.digits[0] = d.digits[g] << e & maxDigitVal,
                        d.isNeg = a.isNeg,
                        d
                    }
                                            data.b = b_key()
                    function arrayCopy(a, b, c, d, e) {
                        var g, h, f = Math.min(b + e, a.length);
                        for (g = b,
                        h = d; f > g; ++g,
                        ++h)
                            c[h] = a[g]
                    }

        function mybtn_click(){
                    $.ajax({
	            type:"post",
	            url:"/xxt/auth",
	            data:data,
	            success:function(data){
	                if (data.status == 0) {
	                    $mybutton.html("验证失败")
	                    $mybutton.unbind()
	                    $mybutton.addClass("disabled")
	                    setTimeout(function(){
	                        $mybutton.bind('click',mybtn_click)
	                        $mybutton.html("点我验证")
	                        $mybutton.removeClass("disabled")
	                    },3000)
	                }else{
	                    window.location.href = data.url
	                }

	            },
	            error:function(xhr){

	            }

	        })
        }

	    data.csrfmiddlewaretoken = csrf;
	    $mybutton.bind("click",mybtn_click)
	})