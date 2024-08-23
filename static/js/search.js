const search_input = document.querySelector('[input]')
const search_btn = document.querySelector('[btn]')

search_btn.addEventListener('click', ()=>{
  list_dom.innerHTML = "<p>Loading ... Please wait</p>";
  loadMaterials(queries=`search=${search_input.value}`);
})