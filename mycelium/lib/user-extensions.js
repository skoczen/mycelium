function eval_css(locator, inDocument) {
    var results = [];
    window.Sizzle(locator, inDocument, results);
    return results
}
