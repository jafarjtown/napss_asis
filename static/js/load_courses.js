
var btn = document.querySelector("[get-m]")
const level = document.querySelector("[level]")
const department = document.querySelector("[department]")
const course = document.querySelector("[course]")

;(()=>{
    if(Number(level.value)) getCourse()
})()


course.addEventListener('change', ()=>{
  if(course.value == 'null') btn.classList.add('d-none')
  else{
    btn.classList.remove('d-none')
  }
})
level.addEventListener("change", getCourse) 
department.addEventListener("change", getCourse) 

async function getCourse(){
        let blankSelect = "--select--"
        if(department.value == 'null' || level.value == 'null'){
          btn.classList.add('d-none')
          return
        }else{
          if(course.value != 'null') btn.classList.remove('d-none')
        }
        let defaultOption = document.createElement("option")
        defaultOption.innerText = "--loading please wait--"
        defaultOption.value = "null"
        course.innerHTML=""
        course.appendChild(defaultOption)
    // fetch all courses in the level 
    
    const response = await fetch(`/api/rest/beta/courses/?department__id=${department.value}&level=${level.value}`)
    const data = await response.json()
    course.removeChild(defaultOption)
    for (let d of data) {
        let option = document.createElement("option")
        option.innerText = d.code.toUpperCase() +" - "+d.title
        option.value = d.code
        course.appendChild(option)
    }
    btn.classList.remove('d-none')
    
}


