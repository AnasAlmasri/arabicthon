function showOrHideSearchFields(action, fieldList) {
    for (let i = 0; i < fieldList.length; i++) {
        if (action == 'show') $('#' + fieldList[i]).show();
        if (action == 'hide') $('#' + fieldList[i]).hide();
    }
}
function renderSearchForm(mode) {
    switch (mode) {
        case 'poet':
            $("#radio_poet").prop("checked", true);
            $("#radio_bayt").prop("checked", false);
            showOrHideSearchFields('show', ['poet_name_div']);
            showOrHideSearchFields('hide', ['keyword_div', 'bahr_div', 'age_div']);
            break;
        case 'bayt':
            $("#radio_poet").prop("checked", false);
            $("#radio_bayt").prop("checked", true);
            showOrHideSearchFields('show', ['keyword_div', 'bahr_div', 'age_div']);
            showOrHideSearchFields('hide', ['poet_name_div']);
            break;
        default:
            renderSearchForm('bayt');
    }
}
