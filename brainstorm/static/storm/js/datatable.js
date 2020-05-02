$(document).ready(function() {
    
    var table = $('#allIdeas').DataTable( {
            responsive: true,
            columnDefs: [
                { width: '80%', targets: 1 },
                { width: '80%', targets: 2 },
                { width: '80%', targets: 3 }
            ],
            "bLengthChange": false,
            dom: 'Bfrtip',
            buttons: [
                {
                    extend: 'csvHtml5',
                    text: 'Export CSV',
                    exportOptions: {
                        columns: 'th:not(:last-child)'
                    }
                }
            ],
            initComplete: function () {
                const th = document.querySelectorAll('#allIdeas > thead > tr > th');
                this.api().columns([5, 1, 4, 8, 10, 11]).every( function (i) {
                    var column = this;
                    let titleHead = [...th][i].innerHTML;
                    var label = $('<label class="text-gray-600 text-sm">'+ titleHead +'<br></label>')
                        .appendTo( $('#filters') );
                    var select = $('<select class="form__select px-2 py-1 rounded"><option value="">--select--</option></select>')
                        .appendTo( $(label))
                        .on( 'change', function () {
                            var val = $.fn.dataTable.util.escapeRegex(
                                $(this).val()
                            );

                            column
                                .search( val ? '^'+val+'$' : '', true, false )
                                .draw();
                        } );

                    column.data().unique().sort().each( function ( d, j ) {
                        select.append( '<option value="'+d+'">'+d+'</option>' )
                    } );
                } );
            },
        } )
        .columns.adjust()
        .responsive.recalc();

        // Export Button
        const allIdeasFilter = document.querySelector('#allIdeas_filter'),
              dtButtons = document.querySelector('.dt-buttons'),
              buttonsCSV = dtButtons.querySelector('.buttons-csv');

        allIdeasFilter.appendChild(dtButtons);
        allIdeasFilter.classList.add('w-full', 'flex', 'items-center', 'justify-center');
        dtButtons.classList.add('flex-1');
        buttonsCSV.classList.add('rounded', 'status', 'border', 'border-gray-500', 'text-gray-500', 'cursor-pointer', 'px-2', 'py-1')
});

// Filter Drop
const filterSection = document.querySelector('.filter_section'),
      filterIcon = filterSection.querySelector('span i'),
      filterAll = document.querySelector('.filter-all');
let filterDrop = false;
filterSection.addEventListener('click', () => {
    if(!filterDrop){
        filterAll.classList.remove('hidden');
        filterIcon.classList.remove('fa-caret-down');
        filterIcon.classList.add('fa-caret-up');
        filterDrop = true;
    }else{
        filterAll.classList.add('hidden');
        filterIcon.classList.add('fa-caret-down');
        filterIcon.classList.remove('fa-caret-up');
        filterDrop = false;
    }
})

// 3Date Range
$('#createDate').daterangepicker();

const dateForm = document.querySelector('#dateRange');
const applyBtn = document.querySelector('.applyBtn');

applyBtn.addEventListener('click', (e) => {
    setTimeout(() => {dateForm.submit();}, 500)
})