let fs = require("fs");

let move_1 = [];
for(let i = 0; i <= 7; i++){
    for(let j = 0; j <= 7; j++){
        if(i === j || i === 5 || j === 5){
            continue;
        }
        a = ["0", "0", "0", "0", "0", "0", "0", "0"];
        a[i] = "+1";
        a[j] = "-1";
        move_1.push(a);
    }
}
for(let i = 0; i <= 7; i++){
    if(i === 5){
        continue;
    }
    a = ["0", "0", "0", "0", "0", "0", "0", "0"];
    a[i] = "=1";
    move_1.push(a);
}


let move_2 = [];
let indexList = [0, 1, 2, 3, 4 ,6, 7];
// +1 +1 -1 -1
indexList.forEach(i => {
    indexList.forEach(j => {
        indexList.forEach(k => {
            indexList.forEach(l => {
                if(i === j || i === k || i === l || j === k || j === l || k === l){
                    return;
                }
                if( j <= i || l <= k){
                    return;
                }
                a = ["0", "0", "0", "0", "0", "0", "0", "0"];
                a[i] = "+1";
                a[j] = "+1";
                a[k] = "-1";
                a[l] = "-1";
                move_2.push(a);
            });
        });
    });
});
console.log(move_2.length);

// +2 -1 -1
indexList.forEach(i => {
    indexList.forEach(j => {
        indexList.forEach(k => {
            if(i === j || i === k || j === k){
                return;
            }
            if( j <= k){
                return;
            }
            a = ["0", "0", "0", "0", "0", "0", "0", "0"];
            a[i] = "+2";
            a[j] = "-1";
            a[k] = "-1";
            move_2.push(a);
        });
    });
});
console.log(move_2.length);

// -2 +1 +1
indexList.forEach(i => {
    indexList.forEach(j => {
        indexList.forEach(k => {
            if(i === j || i === k || j === k){
                return;
            }
            if( j <= k){
                return;
            }
            a = ["0", "0", "0", "0", "0", "0", "0", "0"];
            a[i] = "-2";
            a[j] = "+1";
            a[k] = "+1";
            move_2.push(a);
        });
    });
});
console.log(move_2.length);

// =1 +1 -1
indexList.forEach(i => {
    indexList.forEach(j => {
        indexList.forEach(k => {
            if(i === j || i === k || j === k){
                return;
            }
            a = ["0", "0", "0", "0", "0", "0", "0", "0"];
            a[i] = "=1";
            a[j] = "-1";
            a[k] = "+1";
            move_2.push(a);
        });
    });
});
console.log(move_2.length);

// +2 -2
indexList.forEach(i => {
    indexList.forEach(j => {
        if(i === j){
            return;
        }
        a = ["0", "0", "0", "0", "0", "0", "0", "0"];
        a[i] = "+2";
        a[j] = "-2";
        move_2.push(a);
    });
});
console.log(move_2.length);

// +=1 -1
indexList.forEach(i => {
    indexList.forEach(j => {
        if(i === j){
            return;
        }
        a = ["0", "0", "0", "0", "0", "0", "0", "0"];
        a[i] = "+=1";
        a[j] = "-1";
        move_2.push(a);
    });
});
console.log(move_2.length);

// -=1 +1
indexList.forEach(i => {
    indexList.forEach(j => {
        if(i === j){
            return;
        }
        a = ["0", "0", "0", "0", "0", "0", "0", "0"];
        a[i] = "-=1";
        a[j] = "+1";
        move_2.push(a);
    });
});
console.log(move_2.length);

// =1 =1
indexList.forEach(i => {
    indexList.forEach(j => {
        if(j >= i){
            return;
        }
        a = ["0", "0", "0", "0", "0", "0", "0", "0"];
        a[i] = "=1";
        a[j] = "=1";
        move_2.push(a);
    });
});
console.log(move_2.length);


// =2
indexList.forEach(i => {
    a = ["0", "0", "0", "0", "0", "0", "0", "0"];
    a[i] = "=2";
    move_2.push(a);
});
console.log(move_2.length);

// write to file
let re = {
    move1: move_1,
    move2: move_2
}
fs.writeFile('./move.json', JSON.stringify(re),  err => {
   if (err) {
       return console.error(err);
   }
   console.log("finished!");
});

