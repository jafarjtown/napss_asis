const search_input = document.querySelector('[input]')
const search_btn = document.querySelector('[btn]')
let LAST_REQ 

function submitFormAfterKeyUpDelay(input, delay) {
  let timeoutId;
  // Add a keyup event listener to the input field
  input.addEventListener('keyup', () => {
    // Clear the previous timeout (if any)
    clearTimeout(timeoutId);

    // Set a new timeout to submit the form after the specified delay
    timeoutId = setTimeout(() => {
      console.log(`User stopped typing for ${delay}ms. Submitting form...`);
      loadMaterials(queries=`search=${input.value}`);
    }, delay);
  });
}



// Usage: Call the function with the form ID, input ID, and delay in milliseconds
submitFormAfterKeyUpDelay(search_input, 2000); // Submit form 2 seconds after user stops typing


search_btn.addEventListener('click', ()=>{
  if(LAST_REQ == search_input.value) return
  LAST_REQ = search_input.value
  list_dom.innerHTML = "<p>Loading ... Please wait</p>";
  loadMaterials(queries=`search=${search_input.value}`);
})