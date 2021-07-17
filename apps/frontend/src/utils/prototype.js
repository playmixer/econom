String.prototype.capitalize = function() {
    return this.charAt(0).toUpperCase() + this.slice(1);
}

String.prototype.strftime = function(format = '%D.%M.%Y') {
    let d = new Date(this)
    let day = d.getDate()
    let month = d.getMonth() + 1
    let year = d.getFullYear()

    day = day < 10 ? '0' + day : day
    month = month < 10 ? '0' + month : month

    return format.replace('%D', day)
        .replace('%M', month)
        .replace('%Y', year)

    // return `${day}.${month}.${year}`
}
