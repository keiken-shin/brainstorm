const ideaID = document.querySelector('.idea_id');

// Status Update
try{
    const statusForm = document.querySelector('.status_form'),
          ideaStatus = statusForm.querySelector('[name="idea_status"]'),
          dialog = document.querySelector('.dialog'),
          dialogP = dialog.querySelector('.dialog__p'),
          ideaYes = dialog.querySelector('#idea_status_yes'),
          ideaNo = dialog.querySelector('#idea_status_no'),
          statusCsrf = statusForm.querySelector('[name="csrfmiddlewaretoken"]');
          
    const statusData = new FormData();
    ideaStatus.value = statusValue;

    ideaStatus.addEventListener('change', () => {
        statusData.append('csrfmiddlewaretoken', statusCsrf.value);
        statusData.append('idea_status', ideaStatus.value);

        if(ideaStatus.value !== 'Close' && ideaStatus.value !== 'Cancel'){
            fetch(`/status/${ideaID.textContent}/`, {
                method: 'POST',
                body: statusData
            }).then(res => {
                if(ideaStatus.value === 'Close'){
                    ideaStatus.classList.add('hidden');
                    statusForm.insertAdjacentHTML('beforeend', '<span class="bg-blue-900 px-2 py-1 rounded">Close</span>')
                }else if(ideaStatus.value === 'Cancel'){
                    ideaStatus.classList.add('hidden');
                    statusForm.insertAdjacentHTML('beforeend', '<span class="bg-red-900 px-2 py-1 rounded">Cancel</span>')
                }
            })
        }else{
            dialog.classList.remove('hidden');
            if(ideaStatus.value == 'Cancel'){
                dialogP.textContent = 'Do you really want to cancel this idea?';
            }else{
                dialogP.textContent = 'Do you really want to close this idea?';
            }
        }
    });

    // Idea Yes
    ideaYes.addEventListener('click', () => {
        statusData.append('csrfmiddlewaretoken', statusCsrf.value);
        statusData.append('idea_status', ideaStatus.value);

        fetch(`/status/${ideaID.textContent}/`, {
            method: 'POST',
            body: statusData
        }).then(res => {
            dialog.classList.add('hidden');
            if(ideaStatus.value === 'Close'){
                ideaStatus.classList.add('hidden');
                statusForm.insertAdjacentHTML('beforeend', '<span class="bg-blue-900 px-2 py-1 rounded">Close</span>')
            }else if(ideaStatus.value === 'Cancel'){
                ideaStatus.classList.add('hidden');
                statusForm.insertAdjacentHTML('beforeend', '<span class="bg-red-900 px-2 py-1 rounded">Cancel</span>')
            }
        })
    })

    // Idea No
    ideaNo.addEventListener('click', () => location.reload());
}catch(err){console.log}


// Idea Accept Reject Script
try{
    // Idea Acceptance/Rejection Tab
    const judgeAction = document.querySelector('.judge-action'), 
          accept = judgeAction.querySelector('.button__accept'),
          reject = judgeAction.querySelector('.button__reject');

    const judgeForm = document.querySelector('.judge-form'),
          remarkLabel = judgeForm.querySelector('.remark-label'),
          remark = judgeForm.querySelector('[name="idea_qc_remark"]'),
          statusSelect = judgeForm.querySelector('[name="idea_qc_status"]'),
          csrf = judgeForm.querySelector('[name="csrfmiddlewaretoken"]');

    accept.addEventListener('click', () => {
        judgeAction.classList.add('hidden');
        judgeForm.classList.remove('hidden')
    });

    reject.addEventListener('click', () => {
        judgeAction.classList.add('hidden');
        judgeForm.classList.remove('hidden');

        remarkLabel.textContent = 'Reason for rejection';
        statusSelect.selectedIndex = '1';
    });
}catch(err){console.log}

// Document Detail
try{
    const documentCaret = document.querySelector('.document-caret'),
          caretIcon = documentCaret.querySelector('span i'),
          dropCaret = document.querySelector('.drop-caret');
    
    let drop = false;

    documentCaret.addEventListener('click', () => {
        if(!drop){
            dropCaret.classList.remove('hidden');
            caretIcon.classList.remove('fa-caret-down');
            caretIcon.classList.add('fa-caret-up');
            drop = true;
        }else{
            dropCaret.classList.add('hidden');
            caretIcon.classList.remove('fa-caret-up');
            caretIcon.classList.add('fa-caret-down');
            drop = false;
        }
    })
}catch(err){console.log}

// Comment Form
try{
    const commentForm = document.querySelector('.comment-form'),
          comment = commentForm.querySelector('[name="comment"]'),
          comment_csrf = commentForm.querySelector('[name="csrfmiddlewaretoken"]');

    const commentData = new FormData();

    
    commentForm.addEventListener('submit', (e) => {
        e.preventDefault();

        commentData.append('csrfmiddlewaretoken', comment_csrf.value);
        commentData.append('comment', comment.value);

        fetch(`/comment/${ideaID.textContent}/`, {
            method: 'POST',
            body: commentData
        }).then(res => {
            getCommentData(comment);
            commentForm.reset();
        }).catch(err => console.log);
    })
}catch(err){console.log}

// Month Name
const monthName = ["Jan", "Feb", "March", "April", "May", "June", "July", "Aug", "Sept", "Oct", "Nov", "Dec"];

// Getting Comment Data
const getCommentData = (comment) => {
    const commentList = document.querySelector('.comment-list');
    const commentDate = new Date();

    const finalDate = `${monthName[commentDate.getMonth()]} ${commentDate.getDate()}, ${commentDate.getFullYear()}`;
    const finalTime = formatAMPM(commentDate);

    const commentTemplate = `
        <div class="border-r-4 px-4 py-2 bg-teal-900 mb-2">
            <p class="text-sm flex flex-row-reverse">
                <span class="text-gray-400">${userName}</span>
                <span class="text-gray-500 flex-1">${finalDate}, ${finalTime}</span>
            </p>
            <p class="text-right">${comment.value}</p>
        </div>
    `;

    commentList.insertAdjacentHTML('beforebegin', commentTemplate);
}

// Get Time formatted A.M. & P.M.
function formatAMPM(date) {
  let hours = date.getHours();
  let minutes = date.getMinutes();
  let ampm = hours >= 12 ? 'p.m.' : 'a.m.';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  const finalTime = hours + ':' + minutes + ' ' + ampm;
  return finalTime;
}