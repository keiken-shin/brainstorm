// Status Background
const statusBg = (status) => {
    if(status.textContent === 'Accepted'){
        status.classList.add('border-blue-500', 'text-blue-500');
    }else if(status.textContent === 'Rejected'){
        status.classList.add('border-red-500', 'text-red-500');
    }else if(status.textContent === 'Pending'){
        status.classList.add('border-orange-500', 'text-orange-500')
    }
}

// Tab Data

try{
    const allTab = document.querySelector('[data-class="all_ideas"]'),
          yourTab = document.querySelector('[data-class="your_ideas"]'),
          allSect = document.querySelector('.all_ideas'),
          yourSect = document.querySelector('.your_ideas'),
          ideaStatus = document.querySelectorAll('.idea_status');

    allTab.addEventListener('click', () => {
        allTab.classList.add('md:tab-active');
        yourTab.classList.remove('md:tab-active');

        allSect.classList.remove('hidden');
        yourSect.classList.add('hidden');
    });

    yourTab.addEventListener('click', () => {
        allTab.classList.remove('md:tab-active');
        yourTab.classList.add('md:tab-active');

        allSect.classList.add('hidden');
        yourSect.classList.remove('hidden');
    });

    [...ideaStatus].forEach(status => {
        statusBg(status);
    })

}catch(err){}


// Idea Accept Reject Script

try{
    // Changing status background
    const status = document.querySelector('.status');
    statusBg(status);

    // Idea Acceptance/Rejection Tab
    const judgeAction = document.querySelector('.judge-action'), 
          accept = judgeAction.querySelector('.button__accept'),
          reject = judgeAction.querySelector('.button__reject');

    const judgeForm = document.querySelector('.judge-form'),
          remarkLabel = judgeForm.querySelector('.remark-label'),
          remark = judgeForm.querySelector('[name="idea_remark"]'),
          statusSelect = judgeForm.querySelector('[name="idea_status"]'),
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

}catch(err){}