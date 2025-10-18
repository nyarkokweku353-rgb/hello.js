console.log("Hello, World!")

function add(a, b){
    if(typeof a !== 'number' || typeof b !== 'number'){
        console.log('error')
    }
    return a+b;
}

console.log(add(29, '4'))