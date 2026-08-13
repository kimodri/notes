let sales: number = 1234565789;
let course: string = "TypeScript";
let is_published: boolean = true;

// The Any type
let level;

function render(document: any){
    console.log(document);
}

// Arrays
let numbers: number[] = [1, 2, 3];

// Tuuples
let user: [number, string] = [1, "Kim"];

// Enums - list of related constants
const small = 1;
const medium = 2;
const large = 3;

enum Size { Small = 1, Medium = 2, Large = 3 } 

let mySize = Size.Medium;

console.log(mySize);

// Functions
function calculate_tax(income: number): number{
    if (income < 50_000)
        return income * 1.2
    return income *1.3
}

let income:number = calculate_tax(20000)

// Optional functions
function calculate_tax_with_optional(income: number, taxYear: number = 2022): number{
    if (taxYear < 2000)
        return income * 1.2
    return income *1.3
}

income = calculate_tax_with_optional(20000, 2023);

// objects
let employee: {
    readonly id: number,
    name: string,
    retire: (date: Date) => void
} = {
    id: 1, 
    name: '',
    retire: (date: Date)=>{
        console.log(date)
    }
}

// Type aliases


