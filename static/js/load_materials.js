

const get_m = document.querySelector("[get-m]");
const list_dom = document.querySelector("[list]");

const URL_STR = '/api/rest/beta/materials/'
const PAGING_MAX = 1
let LAST_REQUEST

if(get_m){
  get_m.addEventListener('click', () => {
    let department = document.querySelector("[department]");
    let course = document.querySelector("[course]");
    let level = document.querySelector("[level]");

    const d = department.value;
    const c = course.value;
    const l = level.value;
    const q = [];

    if (c !== 'null') {
        q.push(`course__code=${c}`);
    }
    if (l !== 'null') {
        q.push(`course__level=${l}`);
    }
    if (d !== 'null') {
        q.push(`course__department__id=${d}`);
    }

    if(LAST_REQUEST == q.join('-')) return
    LAST_REQUEST = q.join('-')
    list_dom.innerHTML = "<p>Loading ... Please wait</p>";
    loadMaterials(queries=q.join("&"));
});
}
async function loadMaterials(queries = null, u=null) {
    let url;
    if (u && u !== "null") {
        url = u
    }else{
        url = URL_STR + "?"
    }
  
    url += queries ? queries : '';
    const response = await fetch(url);
    const data = await response.json();
    // if(data.results.length == 0)
    populate_dom(data);
    //pagination(data)
}

function createMaterialElement(obj) {
    const material = document.createElement("div");
    material.className = "material";
    const material_card = document.createElement("div");
    material_card.className = "material-card bg-lightgray";
    const material_info = document.createElement("div");
    material_info.className = "material-info";
    const btns = document.createElement("div");
    btns.className = "btns";
    material_card.append(material_info, btns);
    material.appendChild(material_card);
    
    const fileIconDiv = document.createElement("div");
    fileIconDiv.classList.add("nk-file-icon");

    const spanIcon = document.createElement("span");
    spanIcon.classList.add("nk-file-icon-type");

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    svg.setAttribute("viewBox", "0 0 90 90");
    // Add the rest of your SVG code here...

    spanIcon.innerHTML =
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 90"><rect x="15" y="5" width="56" height="70" rx="6" ry="6" fill="#e3e7fe" stroke="#6576ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><path d="M69.88,85H30.12A6.06,6.06,0,0,1,24,79V21a6.06,6.06,0,0,1,6.12-6H59.66L76,30.47V79A6.06,6.06,0,0,1,69.88,85Z" fill="#fff" stroke="#6576ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><polyline points="60 16 60 31 75 31.07" fill="none" stroke="#6576ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="58" y1="50" x2="32" y2="50" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="46" y1="38" x2="32" y2="38" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="68" y1="44" x2="32" y2="44" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="68" y1="56" x2="32" y2="56" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="58" y1="62" x2="32" y2="62" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="68" y1="68" x2="32" y2="68" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="58" y1="75" x2="32" y2="75" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /></svg>';
    fileIconDiv.appendChild(spanIcon);
    
    const info = document.createElement('div');
    info.className = "info";
    info.innerHTML = `
        <span>${obj.code}</span>
        <span>${obj.title}</span>
        <span>${obj.department_name}</span>
    `;
    material_info.append(fileIconDiv, info);
    
    let dialog = document.createElement('dialog')
    let dialog_actions = document.createElement("div")
    dialog_actions.style.borderTop = "1px solid"
    dialog_actions.style.padding = "5px"
    let dialog_close = document.createElement("button")
    dialog_close.innerText = "close"
    dialog_close.style.padding="4px"
    dialog_actions.appendChild(dialog_close)
    dialog.append(obj.comment, dialog_actions)
    dialog.style.position = "fixed"
    dialog.style.top = "40px"
    dialog.style.padding = "10px"
    dialog.style.margin = "40px auto"
    const createButton = (text, iconSrc, url) => {
        const button = document.createElement("a");
        button.href = url;
        button.style.textAlign = 'center';
        button.innerHTML = `
            <em class="${iconSrc}"></em>
            <span>${text}</span>
        `;
        return button;
    };

    const download = createButton("Download", 'icon ni ni-download', obj.file);
    const view = createButton("View", 'icon ni ni-view', obj.file);
    const report = createButton("Report", 'icon ni ni-report', obj.flag_url);

    btns.append(download, report, dialog);
    
    // event listeners
    
    fileIconDiv.addEventListener("click", ()=>dialog.showModal())
    dialog_close.addEventListener("click", ()=>dialog.close())
    return material;
}

function populate_dom(arr) {
    list_dom.innerHTML = "";

    if (arr.length === 0) {
        list_dom.innerHTML = "<p>Ops, nothing is returned, try again</p>";
    }

    for (let obj of arr) {
        const materialElement = createMaterialElement(obj);
        list_dom.appendChild(materialElement);
    }
}


function pagination(data) {
    if(data.next == null & data.previous == null){
      document.querySelectorAll("[pagination]").forEach(pg=>{
        pg.innerHTML = "";
      })
      return
    }
    const next = data.next;
    const previous = data.previous;
    const count = Number.parseInt(data.count);
    let current_page = 1
    if (next !== null) {
        const url_r = new URL(next);
        const params = new URLSearchParams(url_r.search);
        current_page = Number.parseInt(params.get("page"))-1
    }else if (previous !== null) {
        const url_r = new URL(previous);
        const params = new URLSearchParams(url_r.search);
        current_page = Number.parseInt(params.get("page"))+1 | 2
    }

    const createBtn = (text, url) => {
        const btn = document.createElement('button');
        btn.innerText = text;
        //btn.className = "submit-btn";
        btn.addEventListener("click", () => loadMaterials(null, url));
        return btn;
    }
    
    const createPagination=()=>{
        const next_btn = createPageItem("Next", next);
        const prev_btn = createPageItem("Prev", previous);
        if (current_page == 1) {
            prev_btn[1].disabled = true
        }
        if(current_page == Math.ceil(count / PAGING_MAX)){
          next_btn[1].disabled = true
        }
        
        const createArr = () => {
            let arr = [];
            let l = Math.ceil(count / PAGING_MAX)+1
            for (let i = 1; i < l; i++) {
                let [li, a] = createPageItem('null')
                // let a = document.createElement('button');
                a.innerText = i;
                a.id = i
                if (current_page === i) {
                    a.disabled = true;
                    a.style.color = "red"
                }
                a.addEventListener("click", () => loadMaterials(`page=${i}`));
                arr.push(li);
            }
            let p,s,e;
            e = 7
            if (current_page>4) {
                s = ccurrent_page-4
                e = current_page+3
            }
            if (current_page>l-7) {
                s = l-8
                e = arr.length
            }
            p = arr.slice(s,e)
            return arr;
        }
        const pageButtons = createArr();
        return [prev_btn[0], ...pageButtons, next_btn[0]]
    }
    document.querySelectorAll("[pagination]").forEach(pg=>{
    pg.innerHTML = "";
    pg.append( ...createPagination());
    })
  
}
//loadMaterials();

function createPageItem(word,link, disabled=false) {
    // Create the <li> element with classes
    const li = document.createElement('li');
    li.className = `page-item ${disabled ?'disabled' : ''}`;
    // Create the <a> element with classes and attributes
    const a = document.createElement('a');
    a.className = 'page-link';
    a.addEventListener("click", () =>{
      a.classList.toggle('active')
      loadMaterials(null, link)
    });
    
    a.setAttribute('aria-disabled', disabled);
    a.textContent = word;
    li.appendChild(a);
    
    return [li, a];
}
function createFileItem(fileData) {
    const div = document.createElement("div");
    div.classList.add("nk-file-item", "nk-file");
    div.id = "file" + fileData.id;

    const fileInfoDiv = document.createElement("div");
    fileInfoDiv.classList.add("nk-file-info");

    const fileTitleDiv = document.createElement("div");
    fileTitleDiv.classList.add("nk-file-title");

    const fileIconDiv = document.createElement("div");
    fileIconDiv.classList.add("nk-file-icon");

    const spanIcon = document.createElement("span");
    spanIcon.classList.add("nk-file-icon-type");

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("xmlns", "http://www.w3.org/2000/svg");
    svg.setAttribute("viewBox", "0 0 90 90");
    // Add the rest of your SVG code here...

    spanIcon.innerHTML =
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 90"><rect x="15" y="5" width="56" height="70" rx="6" ry="6" fill="#e3e7fe" stroke="#6576ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><path d="M69.88,85H30.12A6.06,6.06,0,0,1,24,79V21a6.06,6.06,0,0,1,6.12-6H59.66L76,30.47V79A6.06,6.06,0,0,1,69.88,85Z" fill="#fff" stroke="#6576ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><polyline points="60 16 60 31 75 31.07" fill="none" stroke="#6576ff" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="58" y1="50" x2="32" y2="50" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="46" y1="38" x2="32" y2="38" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="68" y1="44" x2="32" y2="44" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="68" y1="56" x2="32" y2="56" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="58" y1="62" x2="32" y2="62" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="68" y1="68" x2="32" y2="68" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /><line x1="58" y1="75" x2="32" y2="75" fill="none" stroke="#c4cefe" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" /></svg>';
    fileIconDiv.appendChild(spanIcon);

    const fileNameDiv = document.createElement("div");
    fileNameDiv.classList.add("nk-file-name");

    const fileNameTextDiv = document.createElement("div");
    fileNameTextDiv.classList.add("nk-file-name-text");

    const anchor = document.createElement("a");
    anchor.href = fileData.file;
    anchor.setAttribute("download", "");
    anchor.classList.add("title");
    anchor.textContent = fileData.title;

    fileNameTextDiv.appendChild(anchor);
    fileNameDiv.appendChild(fileNameTextDiv);
    fileTitleDiv.appendChild(fileIconDiv);
    fileTitleDiv.appendChild(fileNameDiv);

    const ul = document.createElement("ul");
    ul.classList.add("nk-file-desc");

    const liDate = document.createElement("li");
    liDate.classList.add("date");
    liDate.textContent = fileData.uploaded_on;

    const liSize = document.createElement("li");
    liSize.classList.add("size");
    liSize.textContent = fileData.size[0];

    ul.appendChild(liDate);
    ul.appendChild(liSize);

    fileInfoDiv.appendChild(fileTitleDiv);
    fileInfoDiv.appendChild(ul);
    div.appendChild(fileInfoDiv);

    return div;
}

