// Form JS

const form = document.querySelector('.form'),
      formFileDiv = form.querySelector('.form__file-div'),
      formFileName = formFileDiv.querySelector('.form__file-name'),
      formFile = formFileDiv.querySelector('.form__file'),
      formSubmit = form.querySelector('.button-submit');

const ideaImprovement = form.querySelector('[name="idea_improvement"]'),
      ideaTitle = form.querySelector('[name="idea_title"]'),
      ideaDescription = form.querySelector('[name="idea_description"]'),
      ideaImpact = form.querySelector('[name="idea_impact"]'),
      csrf = form.querySelector('[name="csrfmiddlewaretoken"]');

formFile.addEventListener('change', () => {
    if(formFile.value){
        formFileName.textContent = formFile.value.slice(12, formFile.value.length);
        formFileName.classList.remove('form__file-placeholder');
        formFileName.classList.add('form__file-selected');
        formFile.parentElement.style = 'border-bottom-color: var(--glitch-2);';
    }else{
        formFile.parentElement.style = 'border-bottom-color: var(--header-base);';
        formFileName.textContent = 'Choose a file';
        formFileName.classList.add('form__file-placeholder');
        formFileName.classList.remove('form__file-selected');
    }
});


form.addEventListener('submit', (e) => {   
    e.preventDefault();

    formSubmit.innerHTML = '<i class="fas fa-circle-notch circle-notch mr-2"></i>Processing';

    const formData = new FormData();
    
    formData.append("csrfmiddlewaretoken", csrf.value);
    formData.append("idea_improvement", ideaImprovement.value);
    formData.append("idea_title", ideaTitle.value);
    formData.append("idea_description", ideaDescription.value);
    formData.append("idea_impact", ideaImpact.value);
    formData.append("idea_file", formFile.files[0]);

    fetch("/idea/submit/", {
        method: 'POST',
        body: formData
    }).then(res => {
        if(res.status === 200){
            formSubmit.innerHTML = '<i class="fas fa-check mr-2"></i></i>Submitted';
            setTimeout(() => {
                window.location.pathname = "/home/";
            }, 1000);
        }
    })
    .catch(console.log);

});
