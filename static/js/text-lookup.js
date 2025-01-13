
const textLookupForm = document.querySelector("[text-lookup-form]");
const lookupInput = document.querySelector("#lookup-text");
const pageContent = document.querySelector("#content"); // The area to search text in.

textLookupForm.addEventListener("submit", function (e) {
  e.preventDefault();
  const searchTerm = lookupInput.value.trim();
  if (!searchTerm) return;

  // Reset previous highlights
  pageContent.innerHTML = pageContent.innerHTML.replace(/<mark class='custommark'>(.*?)<\/mark>/g, "$1");

  const regex = new RegExp(`(${searchTerm})`, "gi");
  pageContent.innerHTML = pageContent.innerHTML.replace(regex, "<mark class='custommark'>$1</mark>");
});