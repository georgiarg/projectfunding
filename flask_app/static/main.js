$(document).on("click", ".researcher-row", function() {
    var path   = window.location.href;
    id_num = $(this)[0].children[2].innerText 
    url = path + "/researcherform?researcher_id=" + id_num;
    window.location = url;
});