"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
let sales = 1234565789;
let course = "TypeScript";
let is_published = true;
// The Any type
let level;
function render(document) {
    console.log(document);
}
// Arrays
let numbers = [1, 2, 3];
// Tuuples
let user = [1, "Kim"];
// Enums - list of related constants
const small = 1;
const medium = 2;
const large = 3;
var Size;
(function (Size) {
    Size[Size["Small"] = 1] = "Small";
    Size[Size["Medium"] = 2] = "Medium";
    Size[Size["Large"] = 3] = "Large";
})(Size || (Size = {}));
let mySize = Size.Medium;
console.log(mySize);
//# sourceMappingURL=index.js.map