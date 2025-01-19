const btn = $("[get-m]");
const level = $(".js-select2[level]");
const department = $(".js-select2[department]");
const course = $(".js-select2[course]");

(() => {
  if (Number(level.val())) getCourse();
})();

course.on("change", () => {
  if (course.val() === "null") btn.addClass("d-none");
  else btn.removeClass("d-none");
});

level.on("change", getCourse);
department.on("change", getCourse);

async function getCourse() {
  const blankSelect = "--select--";

  if (department.val() === "null" || level.val() === "null") {
    btn.addClass("d-none");
    return;
  } else {
    if (course.val() !== "null") btn.removeClass("d-none");
  }

  // Add the loading option
  course.html('<option value="null">--loading please wait--</option>');

  // Fetch courses based on department and level
  const response = await fetch(`/api/rest/beta/courses/?department__id=${department.val()}&level=${level.val()}`);
  const data = await response.json();

  // Populate course options
  course.empty(); // Clear current options
  data.forEach(d => {
    course.append(`<option value="${d.code}">${d.code.toUpperCase()} - ${d.title}</option>`);
  });

  btn.removeClass("d-none");
}