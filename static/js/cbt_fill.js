
const questions = document.querySelectorAll("[trs]")
const btn = document.querySelector("[btn]")

btn.addEventListener("click", ()=>{
    questions.forEach(q=>{
        let ans = q.querySelector("[ans]")
        let correct_answer = q.querySelector("[correct_answer]").innerText.split(",")
        let all_fills = q.querySelectorAll("input")
        
        
        for(let i = 0; i < all_fills.length; i++){
            let inp = all_fills[i]
            let v = inp.value
            let a = correct_answer[i]
            
            if(v.trim().toLowerCase()==a.trim().toLowerCase()){
                inp.style.backgroundColor = "green"
            }else{
                inp.style.backgroundColor = "red"
                ans.style.display = "block"
            }
            
        }
        
        all_fills.forEach(inp=>{
            inp.addEventListener("keydown", ()=>{
                ans.style.display = "none"
            })
        })
        
       
    })
 })