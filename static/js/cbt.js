const questions = document.querySelectorAll("[question]");
questions[0].style.display="block"
const listOfInputClass = [];
let score = 0;
let indexBtn = 0
class InputClass {
    constructor(inputs, key, elem) {
        this.inputs = inputs;
        this.key = key + 1;
        this.elem = elem;
        this.b = null;
        this.createBox();
        this.addChangeListeners();
    }

    createBox() {
        this.b = document.createElement('button');
        const qs = document.querySelector("[questions]");
        this.b.innerText = this.key;
        this.b.style.backgroundColor = 'white';
        this.b.style.width = "30px";
        this.b.style.height = "30px";
        this.b.style.border = "2px solid lightgray";
        qs.appendChild(this.b);
        this.b.addEventListener("click", () => this.select());
    }

    addChangeListeners() {
        this.inputs.forEach(inp => {
            inp.addEventListener('change', () => {
                this.handleInputChange(inp);
            });
        });
    }

    handleInputChange(inp) {
        this.inputs.forEach(i => {
            i.parentElement.style.border = "none";
            i.disabled = true;
        });
        const correct = this.elem.querySelector("[correct_answer]");
        const p = this.elem.querySelector('[display_correct_answer]');
        const parent = inp.parentElement;
        p.style.display = 'block';
        parent.style.border = "1px solid lightgray";
        if (correct.value == inp.value) {
            parent.style.borderColor = 'green';
            score += 1;
        } else {
            parent.style.borderColor = 'red';
        }
        document.querySelector("[score]").innerText = `${score} out of ${questions.length}`;
    }

    select() {
        questions.forEach(el => el.style.display = "none");
        questions[this.key - 1].style.display = "flex";
        
        this.position();
    }

    checked() {
        const isAtLeastOneChecked = this.inputs.some(input => input.checked);
        this.b.style.backgroundColor = isAtLeastOneChecked ? "lightblue" : "#ff2b4ace";
        
    }

    position(b) {
        listOfInputClass.forEach(el => el.b.style.borderColor = "lightgray");
        if (b) {
            
            listOfInputClass[b].b.style.borderColor = "#816bff";
        } else {
            listOfInputClass[this.key - 1].b.style.borderColor = "#816bff";
        }
    }
}

questions.forEach((elem, key) => {
    const next = elem.querySelector("[next]");
    const prev = elem.querySelector("[prev]");
    const inputs = Array.from(elem.querySelectorAll("input[type='radio']"));

    const inputClass = new InputClass(inputs, key, elem);
    listOfInputClass.push(inputClass);

    next.addEventListener("click", () => {
        const nextElem = elem.nextElementSibling;
        nextElem.style.display = "flex";
        elem.style.display = "none";
        inputClass.position(Number.parseInt(elem.id));
        inputClass.checked();
        
    });

    prev.addEventListener("click", () => {
        const prevElem = elem.previousElementSibling;
        prevElem.style.display = "flex";
        elem.style.display = "none";
        inputClass.position(Number.parseInt(elem.id)-2);
        inputClass.checked();
        
    });
});
