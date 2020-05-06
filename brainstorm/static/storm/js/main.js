// Tab Data
try{
    const tabList = document.querySelectorAll('.tab li');
    const tabSection = document.querySelectorAll('.tab_section');

    [...tabList].forEach(listItem => {
        listItem.addEventListener('click', () => {
            // Get Attribute of clicked tab
            const dataClass = listItem.getAttribute('data-class');
            
            // Make clicked tab active
            [...tabList].map(list => list.classList.remove('md:tab-active'))
            listItem.classList.add('md:tab-active');
            
            // Grab clicked tab associated section
            const selectedTab = document.querySelector(`.${dataClass}`);

            // Make all section hidden
            [...tabSection].map(sect => sect.classList.add('hidden'));

            // Unhine Selected section
            selectedTab.classList.remove('hidden');
        })
    })
}catch(err){console.log}
