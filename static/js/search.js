const search_input = document.querySelector('[input]')
const search_btn = document.querySelector('[btn]')
let LAST_REQ 
search_btn.addEventListener('click', ()=>{
  if(LAST_REQ == search_input.value) return
  LAST_REQ = search_input.value
  list_dom.innerHTML = "<p>Loading ... Please wait</p>";
  loadMaterials(queries=`search=${search_input.value}`);
})