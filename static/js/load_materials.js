const get_m = $("[get-m]");
const list_dom = $("[list]");
const URL_STR = '/api/rest/beta/materials/';
const PAGING_MAX = 1;
let LAST_REQUEST;

if (get_m.length) {
  get_m.on('click', () => {
    const department = $(".js-select2[department]");
    const course = $(".js-select2[course]");
    const level = $(".js-select2[level]");

    const d = department.val();
    const c = course.val();
    const l = level.val();
    const q = [];

    if (c !== 'null') q.push(`course__code=${c}`);
    if (l !== 'null') q.push(`course__level=${l}`);
    if (d !== 'null') q.push(`course__department__id=${d}`);

    if (LAST_REQUEST === q.join('-')) return;
    LAST_REQUEST = q.join('-');

    list_dom.html("<p>Loading ... Please wait</p>");
    loadMaterials(q.join("&"));
  });
}

async function loadMaterials(queries = null, u = null) {
  let url = u && u !== "null" ? u : `${URL_STR}?`;
  url += queries || '';

  const response = await fetch(url);
  const data = await response.json();
  populate_dom(data);
  // pagination(data); // Uncomment if pagination is needed
}

function createMaterialElement(obj) {
  const material = $("<div>", { class: "material" });
  const material_card = $("<div>", { class: "material-card bg-lightgray" });
  const material_info = $("<div>", { class: "material-info" });
  const btns = $("<div>", { class: "btns" });

  const fileIconDiv = $("<div>", { class: "nk-file-icon fs-2" });
  const spanIcon = $("<span>", { class: "nk-file-icon-type" });
  spanIcon.html(`
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 90">
      <rect x="15" y="5" width="56" height="70" rx="6" ry="6" fill="#e3e7fe" stroke="#6576ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
      <path d="M69.88,85H30.12A6.06,6.06,0,0,1,24,79V21a6.06,6.06,0,0,1,6.12-6H59.66L76,30.47V79A6.06,6.06,0,0,1,69.88,85Z" fill="#fff" stroke="#6576ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
      <polyline points="60 16 60 31 75 31.07" fill="none" stroke="#6576ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" />
    </svg>
  `);
  fileIconDiv.append(spanIcon);

  const info = $("<div>", { class: "info" }).html(`
    <span>${obj.code}</span>
    <span>${obj.title}</span>
    <span>${obj.department_name}</span>
  `);

  const dialog = $("<dialog>").html(obj.comment);
  const dialog_actions = $("<div>").css({ borderTop: "1px solid", padding: "5px" });
  const dialog_close = $("<button>", { text: "close", css: { padding: "4px" } });
  dialog_actions.append(dialog_close);
  dialog.append(dialog_actions);

  dialog_close.on("click", () => dialog.get(0).close());

  const createButton = (text, iconSrc, url) => {
    return $("<a>", { href: url, css: { textAlign: "center" } }).html(`
      <em class="${iconSrc}"></em>
      <span>${text}</span>
    `);
  };

  const download = createButton("Download", "icon ni ni-download", obj.download_url);
  const view = createButton("View", "icon ni ni-view", obj.file);
  const report = createButton("Report", "icon ni ni-report", obj.flag_url);

  btns.append(download, report, dialog);
  fileIconDiv.on("click", () => dialog.get(0).showModal());
  material_info.append(fileIconDiv, info);
  material_card.append(material_info, btns);
  material.append(material_card);

  return material;
}

function populate_dom(data) {
  list_dom.empty();

  if (data.length === 0) {
    list_dom.html("<p>Ops, nothing is returned, try again</p>");
    return;
  }

  data.forEach(obj => {
    const materialElement = createMaterialElement(obj);
    list_dom.append(materialElement);
  });
}

// Uncomment the following functions if pagination is needed
/*
function pagination(data) {
  // Pagination logic here...
}
*/