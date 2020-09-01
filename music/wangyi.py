import execjs
import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import requests,json,re
import os
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36"
}
def becomevalid(filename):
    changed_name = filename
    invalid_list = list('？?\*|“<>:/\'\" ')
    for invalid_word in invalid_list:
        if invalid_word in filename:
            changed_name = changed_name.replace(invalid_word,'')
    return changed_name

def getmusicurl(songid):
    os.environ["EXECJS_RUNTIME"] = "Node"
    class PrpCrypt(object):
        def __init__(self, key, iv):
            self.key = key.encode('utf-8')
            self.mode = AES.MODE_CBC
            self.iv = iv.encode('utf-8')

        def pad_byte(self, b):
            '''
            1 先计算所传入bytes类型文本与16的余数
            2 在将此余数转成bytes 当然用0补位也可以
            3 已知了 余数 那么就用余数*被转成的余数，就得到了需要补全的bytes
            4 拼接原有文本和补位
            :param b: bytes类型的文本
            :return: 返回补全后的bytes文本
            '''
            bytes_num_to_pad = AES.block_size - (len(b) % AES.block_size)
            # python3 中默认unicode转码
            # 实际上byte_to_pad 就已经 将 数字转成了unicode 对应的字符  即使你的入参正好是16的倍数，那么bytes也是把列表整体的转码也是有值的
            # 后边解密的匿名函数 拿到最后一个数字后，就知道应该截取的长度，在反着切片就行了
            # 这样保证了数据的完整性
            byte_to_pad = bytes([bytes_num_to_pad])
            padding = byte_to_pad * bytes_num_to_pad
            padded = b + padding
            return padded

        def encrypt(self, text):
            '''
            1 先生成aes实例
            2 对传入的text转成bytes
            3 对传入的text补全
            4 调用encrypt 加密 得到密文
            5 先将密文转16进制，在将16进制用base64转码，然后在将得到的base64解码
            其实在步骤4 就已经完成了aes加密，我所在的公司加密比较复杂 ，需要的可以直接返回步骤4的值

            :param text:
            :return:
            '''
            cryptor = AES.new(self.key, self.mode, self.iv)
            text = text.encode('utf-8')
            text = self.pad_byte(text)
            self.ciphertext = cryptor.encrypt(text)
            return base64.encodebytes(self.ciphertext)

        def decrypt(self, text):
            '''
            解密和加密的顺序是相反的
            1 定义匿名函数，去掉补位
            2 base64解码
            3 生成aes实例
            4 16进制转2进制
            5 使用decrypt解码  得到补全的bytes类型明文

            :param text:
            :return:  解密且去掉补位的明文
            '''
            unpad = lambda s: s[:-ord(s[len(s) - 1:])]
            base64Str = base64.b64decode(text.encode('utf8'))
            cryptor = AES.new(self.key, self.mode, self.iv)
            aesStr = cryptor.decrypt(a2b_hex(base64Str))
            aesStr = str(unpad(aesStr), encoding='utf8')
            return aesStr

    jscmd = '''var i3x = {csrf_token: ""};
    var Ya8S = {};
    var j3x = {};
    var bc4g = {}
    Ya8S.md = ["色", "流感", "这边", "弱", "嘴唇", "亲", "开心", "呲牙", "憨笑", "猫", "皱眉", "幽灵", "蛋糕", "发怒", "大哭", "兔子", "星星", "钟情", "牵手", "公鸡", "爱意", "禁止", "狗", "亲亲", "叉", "礼物", "晕", "呆", "生病", "钻石", "拜", "怒", "示爱", "汗", "小鸡", "痛苦", "撇嘴", "惶恐", "口罩", "吐舌", "心碎", "生气", "可爱", "鬼脸", "跳舞", "男孩", "奸笑", "猪", "圈", "便便", "外星", "圣诞"];
    Ya8S.emj = {
            "色": "00e0b",
            "流感": "509f6",
            "这边": "259df",
            "弱": "8642d",
            "嘴唇": "bc356",
            "亲": "62901",
            "开心": "477df",
            "呲牙": "22677",
            "憨笑": "ec152",
            "猫": "b5ff6",
            "皱眉": "8ace6",
            "幽灵": "15bb7",
            "蛋糕": "b7251",
            "发怒": "52b3a",
            "大哭": "b17a8",
            "兔子": "76aea",
            "星星": "8a5aa",
            "钟情": "76d2e",
            "牵手": "41762",
            "公鸡": "9ec4e",
            "爱意": "e341f",
            "禁止": "56135",
            "狗": "fccf6",
            "亲亲": "95280",
            "叉": "104e0",
            "礼物": "312ec",
            "晕": "bda92",
            "呆": "557c9",
            "生病": "38701",
            "钻石": "14af6",
            "拜": "c9d05",
            "怒": "c4f7f",
            "示爱": "0c368",
            "汗": "5b7a4",
            "小鸡": "6bee2",
            "痛苦": "55932",
            "撇嘴": "575cc",
            "惶恐": "e10b4",
            "口罩": "24d81",
            "吐舌": "3cfe4",
            "心碎": "875d3",
            "生气": "e8204",
            "可爱": "7b97d",
            "鬼脸": "def52",
            "跳舞": "741d5",
            "男孩": "46b8e",
            "奸笑": "289dc",
            "猪": "6935b",
            "圈": "3ece0",
            "便便": "462db",
            "外星": "0a22b",
            "圣诞": "8e7",
            "流泪": "01000",
            "强": "1",
            "爱心": "0CoJU",
            "女孩": "m6Qyw",
            "惊恐": "8W8ju",
            "大笑": "d"
        };
        var Is3x = function(i3x, u3x) {
            try {
                u3x = u3x.toLowerCase();
                if (i3x === null)
                    return u3x == "null";
                if (i3x === undefined)
                    return u3x == "undefined";
                return bc4g.toString.call(i3x).toLowerCase() == "[object " + u3x + "]"
            } catch (e) {
                return !1
            }
        };
        j3x.gR6L = function(i3x) {
            return Is3x(i3x, "function")
        }
      j3x.bf4j = function(k3x, cH4L, O3x) {
            if (!k3x || !k3x.length || !j3x.gR6L(cH4L))
                return this;
            if (!!k3x.forEach) {
                k3x.forEach(cH4L, O3x);
                return this
            }
            for (var i = 0, l = k3x.length; i < l; i++)
                cH4L.call(O3x, k3x[i], i, k3x);
            return this
        }
         function bqK4O(cyx8p) {
            var m3x = [];
            j3x.bf4j(cyx8p, function(cyw8o) {
                m3x.push(Ya8S.emj[cyw8o])
            });
            return m3x.join("")
        };
            function geti(a) {
            var d, e, b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", c = "";
            for (d = 0; a > d; d += 1)
                e = Math.random() * b.length,
                e = Math.floor(e),
                c += b.charAt(e);
            return c
        }
        function getaeskey(){
            return [bqK4O(["流泪", "强"]),bqK4O(Ya8S.md),bqK4O(["爱心", "女孩", "惊恐", "大笑"])]
        };'''

    string = r'{"ids":"['+ songid +']","level":"standard","encodeType":"aac","csrf_token":""}'
    jscmd1 = '''function setMaxDigits(a) {
                    maxDigits = a,
                    ZERO_ARRAY = new Array(maxDigits);
                    for (var b = 0; b < ZERO_ARRAY.length; b++)
                        ZERO_ARRAY[b] = 0;
                    bigZero = new BigInt,
                    bigOne = new BigInt,
                    bigOne.digits[0] = 1
                }
                function BigInt(a) {
                    this.digits = "boolean" == typeof a && 1 == a ? null : ZERO_ARRAY.slice(0),
                    this.isNeg = !1
                }
                 function c(a, b, c) {
                        var d, e;
                        return setMaxDigits(131),
                        d = new RSAKeyPair(b,"",c),
                        e = encryptedString(d, a)
                    }
                    function RSAKeyPair(a, b, c) {
                        this.e = biFromHex(a),
                        this.d = biFromHex(b),
                        this.m = biFromHex(c),
                        this.chunkSize = 2 * biHighIndex(this.m),
                        this.radix = 16,
                        this.barrett = new BarrettMu(this.m)
                    }
                    function biFromHex(a) {
                        var d, e, b = new BigInt, c = a.length;
                        for (d = c,
                        e = 0; d > 0; d -= 4,
                        ++e)
                            b.digits[e] = hexToDigit(a.substr(Math.max(d - 4, 0), Math.min(d, 4)));
                        return b
                    }
                    function hexToDigit(a) {
                        var d, b = 0, c = Math.min(a.length, 4);
                        for (d = 0; c > d; ++d)
                            b <<= 4,
                            b |= charToHex(a.charCodeAt(d));
                        return b
                    }
                    function charToHex(a) {
                        var h, b = 48, c = b + 9, d = 97, e = d + 25, f = 65, g = 90;
                        return h = a >= b && c >= a ? a - b : a >= f && g >= a ? 10 + a - f : a >= d && e >= a ? 10 + a - d : 0
                    }
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
                    function biCopy(a) {
                        var b = new BigInt(!0);
                        return b.digits = a.digits.slice(0),
                        b.isNeg = a.isNeg,
                        b
                    }
                    function biDivide(a, b) {
                        return biDivideModulo(a, b)[0]
                    }
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
                    function arrayCopy(a, b, c, d, e) {
                        var g, h, f = Math.min(b + e, a.length);
                        for (g = b,
                        h = d; f > g; ++g,
                        ++h)
                            c[h] = a[g]
                    }
                    function biMultiplyByRadixPower(a, b) {
                        var c = new BigInt;
                        return arrayCopy(a.digits, 0, c.digits, b, c.digits.length - b),
                        c
                    }
                    function biCompare(a, b) {
                        if (a.isNeg != b.isNeg)
                            return 1 - 2 * Number(a.isNeg);
                        for (var c = a.digits.length - 1; c >= 0; --c)
                            if (a.digits[c] != b.digits[c])
                                return a.isNeg ? 1 - 2 * Number(a.digits[c] > b.digits[c]) : 1 - 2 * Number(a.digits[c] < b.digits[c]);
                        return 0
                    }
                    function biMultiplyDigit(a, b) {
                        var c, d, e, f;
                        for (result = new BigInt,
                        c = biHighIndex(a),
                        d = 0,
                        f = 0; c >= f; ++f)
                            e = result.digits[f] + a.digits[f] * b + d,
                            result.digits[f] = e & maxDigitVal,
                            d = e >>> biRadixBits;
                        return result.digits[1 + c] = d,
                        result
                    }
                    function biSubtract(a, b) {
                        var c, d, e, f;
                        if (a.isNeg != b.isNeg)
                            b.isNeg = !b.isNeg,
                            c = biAdd(a, b),
                            b.isNeg = !b.isNeg;
                        else {
                            for (c = new BigInt,
                            e = 0,
                            f = 0; f < a.digits.length; ++f)
                                d = a.digits[f] - b.digits[f] + e,
                                c.digits[f] = 65535 & d,
                                c.digits[f] < 0 && (c.digits[f] += biRadix),
                                e = 0 - Number(0 > d);
                            if (-1 == e) {
                                for (e = 0,
                                f = 0; f < a.digits.length; ++f)
                                    d = 0 - c.digits[f] + e,
                                    c.digits[f] = 65535 & d,
                                    c.digits[f] < 0 && (c.digits[f] += biRadix),
                                    e = 0 - Number(0 > d);
                                c.isNeg = !a.isNeg
                            } else
                                c.isNeg = a.isNeg
                        }
                        return c
                    }
                    function biAdd(a, b) {
                        var c, d, e, f;
                        if (a.isNeg != b.isNeg)
                            b.isNeg = !b.isNeg,
                            c = biSubtract(a, b),
                            b.isNeg = !b.isNeg;
                        else {
                            for (c = new BigInt,
                            d = 0,
                            f = 0; f < a.digits.length; ++f)
                                e = a.digits[f] + b.digits[f] + d,
                                c.digits[f] = 65535 & e,
                                d = Number(e >= biRadix);
                            c.isNeg = a.isNeg
                        }
                        return c
                    }
                    function biShiftRight(a, b) {
                        var e, f, g, h, c = Math.floor(b / bitsPerDigit), d = new BigInt;
                        for (arrayCopy(a.digits, c, d.digits, 0, a.digits.length - c),
                        e = b % bitsPerDigit,
                        f = bitsPerDigit - e,
                        g = 0,
                        h = g + 1; g < d.digits.length - 1; ++g,
                        ++h)
                            d.digits[g] = d.digits[g] >>> e | (d.digits[h] & lowBitMasks[e]) << f;
                        return d.digits[d.digits.length - 1] >>>= e,
                        d.isNeg = a.isNeg,
                        d
                    }
                    function BarrettMu_modulo(a) {
                        var i, b = biDivideByRadixPower(a, this.k - 1), c = biMultiply(b, this.mu), d = biDivideByRadixPower(c, this.k + 1), e = biModuloByRadixPower(a, this.k + 1), f = biMultiply(d, this.modulus), g = biModuloByRadixPower(f, this.k + 1), h = biSubtract(e, g);
                        for (h.isNeg && (h = biAdd(h, this.bkplus1)),
                        i = biCompare(h, this.modulus) >= 0; i; )
                            h = biSubtract(h, this.modulus),
                            i = biCompare(h, this.modulus) >= 0;
                        return h
                    }
                    function biDivideByRadixPower(a, b) {
                        var c = new BigInt;
                        return arrayCopy(a.digits, b, c.digits, 0, c.digits.length - b),
                        c
                    }
                    function biMultiply(a, b) {
                        var d, h, i, k, c = new BigInt, e = biHighIndex(a), f = biHighIndex(b);
                        for (k = 0; f >= k; ++k) {
                            for (d = 0,
                            i = k,
                            j = 0; e >= j; ++j,
                            ++i)
                                h = c.digits[i] + a.digits[j] * b.digits[k] + d,
                                c.digits[i] = h & maxDigitVal,
                                d = h >>> biRadixBits;
                            c.digits[k + e + 1] = d
                        }
                        return c.isNeg = a.isNeg != b.isNeg,
                        c
                    }
                    function biModuloByRadixPower(a, b) {
                        var c = new BigInt;
                        return arrayCopy(a.digits, 0, c.digits, 0, b),
                        c
                    }
                    function BarrettMu_multiplyMod(a, b) {
                        var c = biMultiply(a, b);
                        return this.modulo(c)
                    }
                    function BarrettMu_powMod(a, b) {
                        var d, e, c = new BigInt;
                        for (c.digits[0] = 1,
                        d = a,
                        e = b; ; ) {
                            if (0 != (1 & e.digits[0]) && (c = this.multiplyMod(c, d)),
                            e = biShiftRight(e, 1),
                            0 == e.digits[0] && 0 == biHighIndex(e))
                                break;
                            d = this.multiplyMod(d, d)
                        }
                        return c
                    }
                    function encryptedString(a, b) {
                        for (var f, g, h, i, j, k, l, c = new Array, d = b.length, e = 0; d > e; )
                            c[e] = b.charCodeAt(e),
                            e++;
                        for (; 0 != c.length % a.chunkSize; )
                            c[e++] = 0;
                        for (f = c.length,
                        g = "",
                        e = 0; f > e; e += a.chunkSize) {
                            for (j = new BigInt,
                            h = 0,
                            i = e; i < e + a.chunkSize; ++h)
                                j.digits[h] = c[i++],
                                j.digits[h] += c[i++] << 8;
                            k = a.barrett.powMod(j, a.e),
                            l = 16 == a.radix ? biToHex(k) : biToString(k, a.radix),
                            g += l + " "
                        }
                        return g.substring(0, g.length - 1)
                    }
                    function biToHex(a) {
                        var d, b = "";
                        for (biHighIndex(a),
                        d = biHighIndex(a); d > -1; --d)
                            b += digitToHex(a.digits[d]);
                        return b
                    }
                    function digitToHex(a) {
                        var b = 15
                          , c = "";
                        for (i = 0; 4 > i; ++i)
                            c += hexToChar[a & b],
                            a >>>= 4;
                        return reverseStr(c)
                    }
                    function reverseStr(a) {
                        var c, b = "";
                        for (c = a.length - 1; c > -1; --c)
                            b += a.charAt(c);
                        return b
                    }
                    function biToString(a, b) {
                        var d, e, c = new BigInt;
                        for (c.digits[0] = b,
                        d = biDivideModulo(a, c),
                        e = hexatrigesimalToChar[d[1].digits[0]]; 1 == biCompare(d[0], bigZero); )
                            d = biDivideModulo(d[0], c),
                            digit = d[1].digits[0],
                            e += hexatrigesimalToChar[d[1].digits[0]];
                        return (a.isNeg ? "-" : "") + reverseStr(e)
                    }
                    
                    var maxDigits, ZERO_ARRAY, bigZero, bigOne, dpl10, lr10, hexatrigesimalToChar, hexToChar, highBitMasks, lowBitMasks, biRadixBase = 2, biRadixBits = 16, bitsPerDigit = biRadixBits, biRadix = 65536, biHalfRadix = biRadix >>> 1, biRadixSquared = biRadix * biRadix, maxDigitVal = biRadix - 1, maxInteger = 9999999999999998;
                    setMaxDigits(20),
                    dpl10 = 15,
    
                    hexatrigesimalToChar = new Array("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"),
                    hexToChar = new Array("0","1","2","3","4","5","6","7","8","9","a","b","c","d","e","f"),
                    highBitMasks = new Array(0,32768,49152,57344,61440,63488,64512,65024,65280,65408,65472,65504,65520,65528,65532,65534,65535),
                    lowBitMasks = new Array(0,1,3,7,15,31,63,127,255,511,1023,2047,4095,8191,16383,32767,65535);
                    setMaxDigits(131)'''
    node = execjs.get(execjs.runtime_names.Node)
    aeskey = node.compile(jscmd)
    rsaencrypt = node.compile(jscmd1)
    paramslist = aeskey.call("getaeskey")
    i = aeskey.call("geti",16)
    paramslist.append(i)
    iv = '0102030405060708'
    encryptor = PrpCrypt(paramslist[2],iv)
    crypttext1 = encryptor.encrypt(string).decode().replace('\n','')
    realaescrypt = PrpCrypt(paramslist[3],iv)
    encparams = realaescrypt.encrypt(crypttext1).decode().replace('\n',"")
    encSeckey = rsaencrypt.call("c",i,paramslist[0],paramslist[1])
    url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
    data = {
        'params':encparams,
        'encSecKey':encSeckey,
    }
    session = requests.session()
    res = session.post(url,headers=headers,data=data)
    title_res = requests.get('https://music.163.com/song?id=' + songid,headers=headers)
    try:
        title = re.findall(r'<title>(.*?)</title>',title_res.text)[0].replace(' - 单曲 - 网易云音乐','')
    except:
        title = '未获取到标题'
    title = becomevalid(title)
    jsondata = json.loads(res.text)
    mpath = f'./static_all/file/{title}.mp3'
    if os.path.exists(mpath):
        os.remove(mpath)
    murl = jsondata['data'][0]['url']
    mcontent = requests.get(murl,headers=headers)
    with open(mpath,'wb') as f:
        f.write(mcontent.content)
    return (mpath,title)

if __name__ == '__main__':
    jsondata = getmusicurl('493735012')
    title_res = requests.get('https://music.163.com/song?id=' + '436514312')
    print(jsondata)
    # musiccontent = requests.get(jsondata['data'][0]['url'],headers=headers).content
    # with open('../../music.mp3','wb') as f:
    #     f.write(musiccontent)


