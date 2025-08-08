/*
  بسم الله الرحمن الرحيم
  الحمد لله رب العالمين
  والصلاة والسلام على أشرف المرسلين -- صلى الله عليه وسلم
  Image Classification App - Clinet Side 
*/

// Variables & HTML Elements

// DropZone
const dropZone = document.getElementById("dropZone");
const imgInput = document.getElementById("imgInput");


// Buttons
const classifyBtn = document.getElementById("classifyBtn");
const detailsBtn = document.getElementById("detailsBtn");
const resetBtn = document.getElementById("resetBtn");


// Prediction Container Area
const notes = document.getElementById("notes");
const info = document.getElementById("info");
const nameArea = document.getElementById("name");
const detailsArea = document.getElementById("details");

// ----------------------------------------------------------------------------


// Helpful Functions


function activate(elem) {
  console.log(elem)
  elem.classList.add('active');
}

function deActivate(elem) {
  elem.classList.remove('active');
}


function removeContent(elem) {
  elem.textContent = "";
}

function addContent(elem, content) {
  elem.textContent = content;
}



function getImgName(src) {
  const parts = src.split("/");
  return parts[parts.length - 1];
}


// ----------------------------------------------------------------------------


// Dropzone area 


// Preview the Image in the Drop
// zone
function previewImg(imgName) {
  const img  = document.createElement("img");
  img.id = "imgPreview";
  img.src = `static/test_images/${imgName}`;
  img.alt = imgName;
  dropZone.append(img);
}



// Inputting an Image
dropZone.addEventListener("click", () => {
  imgInput.click();
});


imgInput.addEventListener("change", () => {

  let img = document.getElementById("imgPreview");
  console.log(img);
  if (img) {
    img.remove();
  }

  img = imgInput.files[0];
  console.log(img);
  if (!img) {
    displayErrorMessage("رجاء، اختر صورة أولاً", 'CLIENT');
    return;
  }

  previewImg(img.name);
});


// ----------------------------------------------------------------------------


// Image Classification

classifyBtn.addEventListener("click", async (e) => {
  // Deactivate the Btn
  deActivate(e.target);

  // Disable the Input
  imgInput.disabled = true;
  dropZone.style.cursor = 'default';

  // Check Image
  const img = document.getElementById("imgPreview");
  if (!img) {
    displayErrorMessage("رجاء، اختر صورة أولاً");
    return;
  }

  // Get the Image
  const imgSrc = String(img.src);
  const imgName = getImgName(imgSrc);

  // send to backend
  const result = await sendImg(imgSrc);
  console.log(result)
  
  // SUCCESS
  if (result['error'] === 0) {
    addContent(nameArea, result['prediction']);

    activate(info);
    deActivate(notes);

    activate(detailsBtn);
    activate(resetBtn);

  }
  
  // ERROR
  else {
    activate(resetBtn);
    displayErrorMessage(result['message']);
  }

});




// Sending Img to Server
async function sendImg(img) {

  // Constructing the Message
  const payload = {
    img: img
  };

  try {
    // Sending
    const response = await fetch("/api/on-receive-img", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const result = await response.json();
  

    // Response ERR (Classification - No Img)
    if (result['status'] !== 'SUCCESS') {
      return {
        error : 1,
        message: result['message']
      }
    }


    // SUCCESS
    return {
      error: 0,
      prediction : result['prediction']
    };


  } 
    
  // Network/Unexpected ERR
  catch (err) {
    // For debugging
    console.log(err);

    return {
      error: 1,
      message : 'حدث خطأ ما، يرجى المحاولة مرة أخرى'
    };
  }
}

// ----------------------------------------------------------------------------

// Get Details from LLM

detailsBtn.addEventListener('click', async (e) => {
  // Deactivate the Btn
  deActivate(e.target);
  addContent(detailsArea, 'يرجى الانتظار');

  // Get the Name
  const shikhName = nameArea.textContent;

  // Send to Backend
  result = await getDetails(shikhName);
  console.log(result);


  // SUCCESS
  if (result['error'] === 0) {
    addContent(detailsArea, result['details']);
  }

  // ERROR
  else {
    displayErrorMessage(result['message']);
  }

});


async function getDetails(name) {
  // Constructing the Message
  const payload = {
    prompt: `أعطني نبذة بسيطة عن الشيخ ${name}.
    الشيخ قد يكون قارئ أو داعية مصري، وهناك احتمال أن يكون قارئ خليجي
    كون الجمل في فقرة واحدة او اثنتين بشكل منتظم.
    لا تستخدم أرقام أو علامات غير الحروف والفاصلة والنقاط.
    `
  };


  try {
    // Sending
    const response = await fetch("/api/llm-get-details", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const result = await response.json();
    
    // Response ERR (LLM - No Prompt)
    if (result['status'] !== 'SUCCESS') {
      return {
        error : 1,
        message : result['message']
      }
    }

    // SUCCESS
    return {
      error: 0,
      details : result['details']
    };


  } 

  // Network/Unexpected ERR
  catch (err) {

    // For debugging
    console.log(err);

    return {
      error: 1,
      message : 'حدث خطأ ما، يرجى المحاولة مرة أخرى'
    };
  }

}





// ----------------------------------------------------------------------------


// Resetting & Handling ERRs


// ERR Display Function
function displayErrorMessage(message) {
  // Handle the Prediction Container
  deActivate(info);
  activate(notes);
  addContent(notes, message);

  // Handle BTNs
  deActivate(classifyBtn);
  deActivate(detailsBtn);
  activate(resetBtn);

  // Handle the Dropzone Area
  dropZone.style.cursor = 'default';
  imgInput.disabled = true;
}



function resetDropzone() {
  const img = document.getElementById("imgPreview");
  if (img) {
    img.remove();
  }
  dropZone.style.cursor = 'pointer'
  imgInput.disabled = false;
}


resetBtn.addEventListener('click', e => {
  deActivate(e.target);
  deActivate(detailsBtn);

  activate(classifyBtn);

  // Reset the Dropzone
  resetDropzone();
  
  // Deactivate the Info Area
  deActivate(info);
  removeContent(nameArea);
  removeContent(detailsArea);


  // Activate the Notes
  activate(notes);
  addContent(notes, "لم يتم اختيار صورة");
});


// ----------------------------------------------------------------------------
