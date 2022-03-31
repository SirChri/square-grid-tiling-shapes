module.exports = {
    /**
     * 
     * @param {Object} data 
     * @returns 
     */
    generateInputFileContent: function(data) {
        var n = data.n,
            l = data.l,
            r = data.r,
            s = data.s,
            forbidden = data.forbidden,
            out = "";
        
        out += "#const n = "+n+".\n"
        out += "#const l = "+l+".\n"
        out += "#const s = "+s+".\n"
        out += "#const r = "+r+".\n"
        out += "#const f = "+forbidden.length+".\n"

        for (const v of forbidden) {
            out += "val("+v.row+","+v.col+",xxx).\n"
        }

        return out;
    }
};