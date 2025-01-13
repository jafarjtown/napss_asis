const OpenAdvanceBtn = document.querySelector('[advance-search-btn]')
const ckas = document.querySelectorAll('[cka]')
const form = document.querySelector('[advance_form]')


function closeAdvanceSearchModal(){
  let dialog = document.querySelector('[advance-search-dialog]')
  dialog.close()
}
function openAdvanceSearchModal(){
  let dialog = document.querySelector('[advance-search-dialog]')
  dialog.style.position = "fixed"
  dialog.style.border = 'none'
  dialog.style.top = "40px"
  dialog.style.padding = "10px"
  dialog.style.margin = "40px auto"
  dialog.showModal()
  let CloseAdvanceBtn = document.querySelector('[close-advance-btn]')
  CloseAdvanceBtn.addEventListener('click', closeAdvanceSearchModal)
}
function preventInvalidSubmit(form){
  if(!document.querySelector('[cka]:checked')){
    form.preventDefault()
    alert('You must select at least one field to look for.')
  }
}
OpenAdvanceBtn.addEventListener('click', openAdvanceSearchModal)

form.addEventListener('submit', preventInvalidSubmit)

